#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, copy, pickle
import numpy as np
import pandas as pd
# import pylightcurve as plc
from pylightcurve_master import pylightcurve_self as plc

# The package for parallel computing
import multiprocessing

# In[ ]:


def add_observation(planet,
                    exp_t,
                    time_array,
                    flux_array,
                    flux_unc_array,
                    filtername):
    
    planet.add_observation(time = time_array,
                    time_format = 'BJD_TDB',   
                    exp_time = exp_t,
                    time_stamp = 'mid', 
                    flux = flux_array, 
                    flux_unc = flux_unc_array,   
                    flux_format = 'flux',
                    filter_name = filtername)


# In[ ]:


def run_fitting(planet, date, exp_t, bin_size, filtername, mode):
    
    """
    <<input>>
    planet     : pylightcurve planet object ; synthetic light curve data ; generated from func:create_planet_tkdata
    date       : string                     ; observation date           ; the chosen date of available observation by Starfrive tool
    exp_t      : int                        ; exposure time              ; will be determined in LC_fitting.py
    binsize    : int                        ; bin size
    filtername : string                     ; filter name 
    mode       : string                     ; consider "whole time"/"observable time" ; 'mod' / 'obs']
    
    <<output>>
    **         : running                    ; execute the fitting code   ; generated the mcmc_fitting
    """
    
    save_planet  = planet.name
    save_stellar = '-'.join(save_planet.split('-')[:-1])
    # check if there is the save folder
    if not os.path.isdir(f"Savefile/{save_stellar}/{save_planet}/{date}/fitting/{bin_size}"):
        os.makedirs(f"Savefile/{save_stellar}/{save_planet}/{date}/fitting/{bin_size}")
        
    # path of saving file
    save_path = f"Savefile/{save_stellar}/{save_planet}/{date}/fitting/{bin_size}/{bin_size}_t{exp_t}_{mode}_{filtername}_fit"
    
    print("Fitting result save in:")
    print(save_path)
    
#     planet.transit_fitting(save_path,
#                       detrending_order=1,
#                       iterations=50000,
#                       burn_in = 25000,
#                       walkers=50,
#                       fit_rp_over_rs=True,
#                       fit_mid_time=True)
    
    planet.transit_fitting(save_path,
                      detrending_order=1,
                      iterations=100000,
                      burn_in = 50000,
                      walkers=50,
                      fit_mid_time=True)


def lc_fitting(target_name, target_date,
               mode_list         = ["mod", "obs"],
               run_nonbinned_fit = True,
               run_binning_fit   = True,
               multiple_process  = False,
               avail_cpus        = int(os.cpu_count()/2)):

    """
    <<input>>
    target_name       : string       ; target planet_name                      
    planet_date       : string       ; target planet_date                        ; list in LC_syn_tk.ipynb
    mode_list         : list(string) ; consider "whole time"/"observable time"   ; default = ['mod', 'obs']
    run_nonbinned_fit : bool         ; whether run non-binned_fit fitting or not ; default = True
    run_binning_fit   : bool         ; whether run binning fitting or not        ; default = True
    multiple_process  : bool         ; whether simultaneously run differnt exp_t ; default = False 
    
    <<output>>
    **              : running      ; execute the fitting code                ; define in same file func_fitv2.py
    """

    stellar_name = '-'.join(target_name.split('-')[:-1])
    
    data     = pickle.load(open(f"Savefile/{stellar_name}/{target_name}/{target_date}/time_flux/{target_name}_{target_date}.pickle",'rb'))
    data_bin = pickle.load(open(f"Savefile/{stellar_name}/{target_name}/{target_date}/time_flux/{target_name}_bin_{target_date}.pickle",'rb'))

    date            = data["target_date"]
    planet_tk       = data["planet_object"]
    exposure_list   = data["exposure_list [sec]"]
    filtername_list = data["filtername_list"]   # 'Twinkle_ch0_filter','Twinkle_ch1_filter'
    print(f"The filter list is: {filtername_list}")
    
    binsize_list    = data_bin["binsize_list [min]"]
    
    # check the date from the saving path is the same as the synthetic object
    if not target_date==date:
        print("Something go wrong QQ")
        return
    
    for mode in mode_list:
        index = 0
        for filtername in filtername_list:
            for exp_t in exposure_list[index]:
                planet = copy.deepcopy(planet_tk)

                if mode == "mod":
                    time_array     = data["time_array"][filtername][f"exp_t{exp_t} [sec]"]
                    flux_array     = data["mod_noise_array"][filtername][f"exp_t{exp_t} [sec]"]
                    flux_unc_array = np.full((len(data["mod_noise_array"][filtername][f"exp_t{exp_t} [sec]"]),),
                                             data["err_per_exp [ppm]"][filtername][f"exp_t{exp_t} [sec]"]/1e6)

                elif mode == "obs":
                    time_array     = data["observable_array"][filtername][f"exp_t{exp_t} [sec]"]
                    flux_array     = data["obs_noise_array"][filtername][f"exp_t{exp_t} [sec]"]
                    flux_unc_array = np.full((len(data["obs_noise_array"][filtername][f"exp_t{exp_t} [sec]"]),),
                                             data["err_per_exp [ppm]"][filtername][f"exp_t{exp_t} [sec]"]/1e6)

                add_observation(planet,
                                exp_t,
                                time_array,
                                flux_array,
                                flux_unc_array,
                                filtername)

                print("Do fitting of non-binning data in date:")
                print(f"{date} exp_t:{exp_t} datatype:{mode} filter:{filtername}")

                if run_nonbinned_fit:
                    # For parallel computing
                    # We use the function of "multiprocessing.Process" to let our function "run_fitting" become one of the task.
                    # Then, we use .start() to let the CPU start to execute the task, and continue to do other tasks if we need.
                    # We can also use .join to let CPU wait for the previous tasks finish.
                    if multiple_process:
                        pool =  multiprocessing.Pool(processes = avail_cpus)
                        pool.apply_async(run_fitting, args=(planet, date, exp_t, "non-binned", filtername, mode))
                    else:
                        run_fitting(planet, date, exp_t, "non-binned", filtername, mode)
            
            index = index + 1
            
    # for multiple_process, wait until the non-binned data finish
    if run_nonbinned_fit and multiple_process:
        pool.close()
        pool.join()

    for bin_size in binsize_list:

        for mode in mode_list:
            index = 0
            for filtername in filtername_list:
                for exp_t in exposure_list[index]:
                    planet_b = copy.deepcopy(planet_tk)

                    if data_bin[f"check_expvsbin_t{bin_size} [min]"][filtername][f"exp_t{exp_t} [sec]"]:
                        print(f"The bin_size{bin_size}(min) > exposure_time{exp_t}(sec), skip binning fitting")
                        continue

                    if mode == "mod":
                        time_array     = data_bin[f"lc_b{bin_size}_mod [min]"][filtername][f"exp_t{exp_t} [sec]"].time.value
                        flux_array     = data_bin[f"lc_b{bin_size}_mod [min]"][filtername][f"exp_t{exp_t} [sec]"].flux.value
                        flux_unc_array = data_bin[f"lc_b{bin_size}_mod [min]"][filtername][f"exp_t{exp_t} [sec]"].flux_err.value/1e6

                    elif mode == "obs":
                        time_array     = data_bin[f"lc_b{bin_size}_obs [min]"][filtername][f"exp_t{exp_t} [sec]"].time.value
                        flux_array     = data_bin[f"lc_b{bin_size}_obs [min]"][filtername][f"exp_t{exp_t} [sec]"].flux.value
                        flux_unc_array = data_bin[f"lc_b{bin_size}_obs [min]"][filtername][f"exp_t{exp_t} [sec]"].flux_err.value/1e6

                        time_array     = time_array[np.isfinite(flux_array)]
                        flux_array     = flux_array[np.isfinite(flux_array)]
                        flux_unc_array = flux_unc_array[np.isfinite(flux_unc_array)]             

                    add_observation(planet_b,
                                    exp_t,
                                    time_array,
                                    flux_array,
                                    flux_unc_array,
                                    filtername)

                    print(f"Do fitting of {bin_size}bin data in date:")
                    print(f"{date} exp_t:{exp_t} datatype:{mode} filter:{filtername}")

                    if run_binning_fit:
                        # For parallel computing
                        # We use the function of "multiprocessing.Process" to let our function "run_fitting" become one of the task.
                        # Then, we use .start() to let the CPU start to execute the task, and continue to do other tasks if we need.
                        # We can also use .join to let CPU wait for the previous tasks finish.
                        if multiple_process:
                            pool =  multiprocessing.Pool(processes = avail_cpus)
                            pool.apply_async(run_fitting, args=(planet_b, date, exp_t, 'bin'+str(bin_size), filtername, mode))
                        else:
                            run_fitting(planet_b, date, exp_t, 'bin'+str(bin_size), filtername, mode)
                    
                index = index + 1
        
    # for multiple_process, wait until the previos task become finish.
    if run_binning_fit and multiple_process:
        pool.close()
        pool.join()
