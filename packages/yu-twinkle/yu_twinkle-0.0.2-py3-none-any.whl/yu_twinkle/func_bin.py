import pickle, json
import numpy as np
import pandas as pd
import lightkurve as lk


def binning(data, binsize_list, exposure_list, filtername_list):
    """
    <<input>>
    data            : dictionary   ; synthetic light curve data   ; generated from LC_syn_tk.py
    binsize_list    : list(int)    ; different bin size 
    exposure_list   : list(int)    ; different exposure time list 
    filtername_list : list(string) ; different filter name 
    
    <<output>>
    data            : dictionary ; synthetic light curve data   ; generated from LC_syn_tk.py
                      structure  : data_bin[
                                            lc_b5_mod,
                                            lc_b5_obs,
                                            syn_b5_mod,
                                            syn_b5_obs[
                                                       10,
                                                       20,
                                                       30[
                                                          filter1,
                                                          filter2[
                                                                  Lightkurve object
                                                                 ],
                                                          ],
                                                       ...
                                                      ],
                                            ...
                                           ]
    """
    target_name = data["planet_object"].name
    stellar_name= '-'.join(target_name.split('-')[:-1])
    
    target_date = data["target_date"]
    mid_time    = data["mid_time"]
    time        = data["time_array"]
    obs_time    = data["observable_array"]
    orbit_time  = data["orbit_array"]
    err_per_exp = data["err_per_exp [ppm]"]

    tr_mod      = data["tr_mod_array"]
    tr_obs      = data["tr_obs_array"]
    mod_noise   = data["mod_noise_array"]
    obs_noise   = data["obs_noise_array"]

    lc_mod  = {}
    lc_obs  = {}
    syn_mod = {}
    syn_obs = {}


    # get the num of observable channel on the certain date of this target
    #############################################################################
    # get the available transit date (by the stardrive datebase)  ; generated from Twinkle Stardrive tool(orbit)
    f = open(f"Data_tk/stardrive/{stellar_name}/{target_name}/transit-results.json")
    tk_avail_time = json.load(f)

    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df["Mid_date"][df["Mid_date"]==target_date].keys()[0]

    num_orbits = tk_avail_time["transit"][target_lc_num]["num_views"]
    #############################################################################

    filter_index = 0
    # let data become lightkurve object of lightkcurve package
    for filtername in filtername_list:
        lc_mod[filtername]  = []
        syn_mod[filtername] = []

        lc_obs[filtername]  = {}
        syn_obs[filtername] = {}

        for i in range(len(exposure_list[filter_index])):
            exp_t = str(exposure_list[filter_index][i])

            lc_mod[filtername].append(lk.LightCurve(time = time[filtername][f"exp_t{exp_t} [sec]"],
                                                    flux = mod_noise[filtername][f"exp_t{exp_t} [sec]"],
                                                    flux_err = np.full((len(time[filtername][f"exp_t{exp_t} [sec]"]),),
                                                                       err_per_exp[filtername][f"exp_t{exp_t} [sec]"])))
            
            syn_mod[filtername].append(lk.LightCurve(time = time[filtername][f"exp_t{exp_t} [sec]"],
                                                     flux = tr_mod[filtername][f"exp_t{exp_t} [sec]"],
                                                     flux_err = np.full((len(tr_mod[filtername][f"exp_t{exp_t} [sec]"]),),
                                                                        err_per_exp[filtername][f"exp_t{exp_t} [sec]"])))

            lc_obs[filtername][f"exp_t{exp_t} [sec]"]  = {}
            syn_obs[filtername][f"exp_t{exp_t} [sec]"] = {}

            start_point = 0
            for ii in range(int(num_orbits)):
                point_num = len(orbit_time[filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"])
                end_point = start_point + point_num

                lc_obs[filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"] = \
                lk.LightCurve(time = orbit_time[filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"],
                              flux = obs_noise[filtername][f"exp_t{exp_t} [sec]"][start_point:end_point],
                              flux_err = np.full((point_num,), err_per_exp[filtername][f"exp_t{exp_t} [sec]"]))

                syn_obs[filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"] = \
                lk.LightCurve(time = orbit_time[filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"],
                              flux = tr_obs[filtername][f"exp_t{exp_t} [sec]"][start_point:end_point],
                              flux_err = np.full((point_num,),  err_per_exp[filtername][f"exp_t{exp_t} [sec]"]))

                start_point = end_point

        filter_index = filter_index + 1
    
    data_bin = {}
    data_bin["binsize_list [min]"] = binsize_list

    # binning
    for bin_t in binsize_list:  # binning time size is in unit : [min]  
        data_bin[f"check_expvsbin_t{bin_t} [min]"] = {}
        data_bin[f"lc_b{bin_t}_mod [min]"]         = {}
        data_bin[f"lc_b{bin_t}_obs [min]"]         = {}
        data_bin[f"syn_b{bin_t}_mod [min]"]        = {}
        data_bin[f"syn_b{bin_t}_obs [min]"]        = {}       
            
        filter_index = 0
        for filtername in filtername_list:
            data_bin[f"check_expvsbin_t{bin_t} [min]"][filtername] = {}
            data_bin[f"lc_b{bin_t}_mod [min]"][filtername]         = {}    
            data_bin[f"lc_b{bin_t}_obs [min]"][filtername]         = {} 
            data_bin[f"syn_b{bin_t}_mod [min]"][filtername]        = {} 
            data_bin[f"syn_b{bin_t}_obs [min]"][filtername]        = {}
        
            for i in range(len(exposure_list[filter_index])):
                exp_t = str(exposure_list[filter_index][i])
                
                if float(exp_t)/60 > bin_t:
                    data_bin[f"check_expvsbin_t{bin_t} [min]"][filtername][f"exp_t{exp_t} [sec]"] = True
                    continue
                
                else:
                    data_bin[f"check_expvsbin_t{bin_t} [min]"][filtername][f"exp_t{exp_t} [sec]"] = False
                    
                    data_bin[f"lc_b{bin_t}_mod [min]"][filtername][f"exp_t{exp_t} [sec]"]  \
                            = lc_mod[filtername][i].bin(time_bin_size=bin_t/60/24)
                    data_bin[f"syn_b{bin_t}_mod [min]"][filtername][f"exp_t{exp_t} [sec]"] \
                            = syn_mod[filtername][i].bin(time_bin_size=bin_t/60/24)
                    
                    data_bin[f"lc_b{bin_t}_obs [min]"][filtername][f"exp_t{exp_t} [sec]"]   \
                            = lc_combine(lc_obs[filtername][f"exp_t{exp_t} [sec]"],
                                         orbit_time[filtername][f"exp_t{exp_t} [sec]"],
                                         num_orbits, bin_t)
                    data_bin[f"syn_b{bin_t}_obs [min]"][filtername][f"exp_t{exp_t} [sec]"]  \
                            = lc_combine(syn_obs[filtername][f"exp_t{exp_t} [sec]"],
                                         orbit_time[filtername][f"exp_t{exp_t} [sec]"],
                                         num_orbits, bin_t)
                    
                
            filter_index = filter_index + 1
            
    return data_bin

def lc_combine(lc_obs, orbit_time, num_orbits, bin_t):
    time  = np.array([])
    flux  = np.array([])
    error = np.array([])
    
    for ii in range(int(num_orbits)):
        if len(lc_obs[f"orbit_{ii}"])<=1:
            continue
        bin_lc_element = lc_obs[f"orbit_{ii}"].bin(time_bin_size=bin_t/60/24)
        
        orbit_time_check = orbit_time[f"orbit_{ii}"]
        
        flux_time_ckeck_i = np.array(bin_lc_element.time.value)
        flux_flux_ckeck_i = np.array(bin_lc_element.flux.value)
        flux_err_ckeck_i  = np.array(bin_lc_element.flux_err.value)
        
        flux_time_ckeck_f = flux_time_ckeck_i[flux_time_ckeck_i<max(orbit_time_check)]
        flux_flux_ckeck_f = flux_flux_ckeck_i[flux_time_ckeck_i<max(orbit_time_check)]
        flux_err_ckeck_f  = flux_err_ckeck_i[flux_time_ckeck_i<max(orbit_time_check)]
        
        time  = np.append(time, flux_time_ckeck_f)
        flux  = np.append(flux, flux_flux_ckeck_f)
        error = np.append(error, flux_err_ckeck_f)
        
    return lk.LightCurve(time = time, flux = flux, flux_err = error)