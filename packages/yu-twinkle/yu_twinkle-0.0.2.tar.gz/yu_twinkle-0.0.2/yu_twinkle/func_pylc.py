import os, copy, math, json
import numpy as np
import pandas as pd
from pylightcurve_master import pylightcurve_self as plc
# import pylightcurve as plc
import matplotlib.pyplot as plt
from astropy.time import Time


# This function is copied from pylight curve siurce code
# The main usage od this function is to generated the fp_over_fs of target planet,
# and can use this result to add new filter information

def self_fp_over_fs(rp_over_rs, sma_over_rs, albedo, emissivity, stellar_temperature, filter_name, filter_wave):
    # here, the self_fp_over_fs need the filter name to load the "transmission rate"
    
    def _black_body(w, t):
        # w in mu
        w = w / (10 ** 6)
        h = 6.62607004 * (10 ** (-34))
        c = 3 * (10 ** 8)
        w5 = w ** 5
        k = 1.38064852 * (10 ** (-23))
        return (2 * h * c * c / w5) / (np.exp(h * c / w / k / t) - 1)

    planet_temperature = stellar_temperature * np.sqrt(0.5 / sma_over_rs) * (((1 - albedo) / emissivity) ** 0.25)

    if filter_wave=='':
        wavelength_array, band = np.loadtxt(os.path.join("Data_tk/passband", f"{filter_name}.pass"), unpack=True)
    
    else:
        # getting the lower and upper bound of each channel
        low_wave  = int(float(filter_wave.split("_")[0]))
        high_wave = int(float(filter_wave.split("_")[1]))

        wavelength_array, band = np.loadtxt(os.path.join("Data_tk/passband", f"{filter_name}.pass"), unpack=True)

        # using the lower and upper bound to get the range information
        wavelength_array_filter = copy.copy(wavelength_array)
        wavelength_array = wavelength_array[wavelength_array>=low_wave]
        band             = band[wavelength_array_filter>=low_wave]
        wavelength_array_filter = copy.copy(wavelength_array)
        wavelength_array = wavelength_array[wavelength_array<=high_wave]
        band             = band[wavelength_array_filter<=high_wave]
    
    binsedge = 0.5 * (wavelength_array[:-1] + wavelength_array[1:])
    binsedge1 = np.append(wavelength_array[0] - (binsedge[0] - wavelength_array[0]), binsedge)
    binsedge2 = np.append(binsedge, wavelength_array[-1] + (wavelength_array[-1] - binsedge[-1]))
    binswidth = binsedge2 - binsedge1

    weights = band * binswidth / 10000
    emission = ((rp_over_rs ** 2) *
                _black_body(wavelength_array / 10000, planet_temperature) /
                _black_body(wavelength_array / 10000, stellar_temperature))

    emission = np.sum(emission * weights) / np.sum(weights)

    reflection = albedo * (rp_over_rs ** 2) / (sma_over_rs ** 2)

    return reflection + emission


def get_noise(planet, filtername, exp_t, time, observable, filter_channelornot, filterchannelnum, verbose):
    """
    <<input>>
    planet              : pylightcurve planet object ; the inforamtion of planet parameter       ; generated from func:create_planet_tkdata
    filtername          : string                     ; filtername by given to get the error information
    exp_t               : float                      ; the exposure time
    time                : np.array(float)            ; the time array "without" considering Earth block 
    observable          : np.array(float)            ; the time array "with" considering Earth block
    filter_channelornot : boolen                     ; the current filter is channeled or not
    filterchannelnum    : int                        ; the number of channeling filter if the current filter is channeled
    verbose             : boolen                     ; print details or not
    
    <<output>>
    scatter_mod     : np.array(float)            ; the flux array points (not yet add noise) "without" considering Earth block
    scatter_obs     : np.array(float)            ; the flux array points (not yet add noise) "with" considering Earth block
    err_per_exp     : float                      ; the error(noise) of each exposure time    ; unit:[ppm]
    """
    
    # Loading the information from .csv data base
    stellar_name    = '-'.join(planet.name.split('-')[:-1])
    errcsv_CHEOPS   = pd.read_csv(f"Data_tk/error/{stellar_name}/{stellar_name}_CHEOPS-error.csv")
    errcsv_Twinkle  = pd.read_csv(f"Data_tk/error/{stellar_name}/{stellar_name}_Twinkle-error.csv") 
    
    # CHEOPS will use the url: Exposure Time Calculator to get the error information
    #############################################################################
    if filtername.split("_")[0] == "CHEOPS":
        if filter_channelornot:
            print("CHEOPS can not apply error for channeling filter now.")
            print("Beacuse we don't have CHEOPS error source of channeling filter.")
            print("You can use the not add noise option!!!")
            print("")
            return np.zeros(len(time)), np.zeros(len(observable)), 0.
        
        expt_column  = pd.Index(errcsv_CHEOPS["exposure time(s)"])       # get the column of exposure time(s)
        expt_index   = expt_column.get_loc(exp_t)                        # get the index of target exp_t
        err_per_exp  = errcsv_CHEOPS.loc[expt_index,"photon noise[ppm]"]

        if verbose:
            print(f"The exp_t for CHEOPS filter is {exp_t} [sec]")
            print(f"The err_per_exp is {err_per_exp} [ppm]")
            print("")
    #############################################################################

    # Twinkle will use the url: Stardrive-Radiometric tool to get the error information
    #############################################################################
    elif filtername.split("_")[0] == "Twinkle":
        if filter_channelornot and filterchannelnum!="default":
            print("Twinkle can not apply error for self-divided channeling filter now.")
            print("You can use the not add noise option!!!")
            print("")
            return np.zeros(len(time)), np.zeros(len(observable)), 0.
        
        filter_column  = pd.Index(errcsv_Twinkle["filtername"])           # get the column of error_per_exposure
        filter_index   = filter_column.get_loc(filtername)                # get the index (which filter)
        err_per_exp_tk = errcsv_Twinkle.loc[filter_index, "error_per_exposure"]

        # Beacause the Stardrive-Radiometric tool can not modify the exposure time by user
        # (exposure time was calculated by tool and give an appropriate exposure time.)
        # We will check if the user enter the same exposure time as tool gave us,
        # or recalculate the error by the relation of error proportional to 1/(exp_t)^0.5
        if exp_t == errcsv_Twinkle.loc[filter_index, "exposure_time"]:
            err_per_exp = err_per_exp_tk
            if verbose:
                print(f"The self-define exp_t {exp_t} [sec] for {filtername} is the same as Twinkle tool given")
                print(f"The err_per_exp is {err_per_exp} [ppm]")
                print("")

        else:
            exp_t_tk = errcsv_Twinkle.loc[filter_index, "exposure_time"]
            err_per_exp = round(err_per_exp_tk*math.sqrt(exp_t_tk/exp_t), 3)
            if verbose:
                print(f"The self-define exp_t {exp_t} [sec] for {filtername} is the different from Twinkle tool given {exp_t_tk} [sec]")
                print(f"The Twinkle given err_per_exp is {err_per_exp_tk} [ppm]")
                print(f"The self-define err_per_exp after transform is {err_per_exp} [ppm]")
                print("")
    #############################################################################

    scatter_mod = np.random.normal(0,err_per_exp/1e6,len(time))
    scatter_obs = np.random.normal(0,err_per_exp/1e6,len(observable))
    
    return scatter_mod, scatter_obs, err_per_exp



def model_transit(planet, exposure_list,
                  target_lc_num, tk_avail_time,
                  filtername_list,
                  filterchannelnum_list,
                  filtername_allchannellist,
                  add_noise=True,
                  verbose=True):
    """
    <<input>>
    planet                    : pylightcurve planet object ; the inforamtion of planet parameter                   ; generated from func:create_planet_tkdata
    exposure_list             : list(int)                  ; different exposure time list 
    target_lc_num             : int                        ; the index of target_date in tk_avail_time
    tk_avail_time             : dictionary                 ; available observation infromation                     ; generated from Twinkle Stardrive orbit tool
    filtername_list           : list(str)                  ; different filter name 
    filterchannelnum_list     : list(int)                  ; the number of channels in each filter                 ; determined in LC_syn_tk.ipynb
    filtername_allchannellist : list(string)               ; the name list of all including origin/channel filters ; generated from LC_syn_tk.ipynb
    add_noise                 : boolen                     ; whether adding noise to model light curve or not
    verbose                   : boolen                     ; print details or not
    
    <<output>>
    data            : dictionary                 ; synthetic light curve data                ; generated from LC_syn_tk.py
    """
    
    # create the dictionary to save the syntheic light curve
    mid_time    = planet.mid_time
    target_date = Time(mid_time, format='jd')
    target_date = Time(target_date.iso, out_subfmt='date').iso
    start_time  = Time(tk_avail_time["transit"][target_lc_num]["start_time"]).jd

    data = {}
    data["mid_time"]            = mid_time
    data["target_date"]         = target_date
    data["exposure_list [sec]"] = exposure_list
    data["filtername_list"]     = filtername_list
    data["planet_object"]       = planet
    data["time_array"]          = {}
    data["observable_array"]    = {}
    data["orbit_array"]         = {}
    data["err_per_exp [ppm]"]   = {}
    
    data["tr_mod_array"]        = {}
    data["tr_obs_array"]        = {}
    data["mod_noise_array"]     = {}
    data["obs_noise_array"]     = {}
    
    
    filter_index_check = -1
    for filtername in filtername_allchannellist:
        # check which filter is the channeling filter belong.
        #############################################################################
        filter_channel_now = filtername.split('-')[0]                   # the belong's original filter of the channeled filter
        filter_index       = filtername_list.index(filter_channel_now)  # the index of this belong's original filter
        
        # also check if filter have channel or not (determine by check the white filter)
        if len(filtername.split('-'))==1:
            if not filterchannelnum_list[filter_index]==0:
                filter_channelornot = True 
                print(f"Check for {filtername} channeling: True")  

            else:
                filter_channelornot = False
        
        # check if this channeling filter is the same as the belong's original filter
        # case1(>): this channeling filter is belong to belong's original filter (In general, will be the )     
        # case2(==): this channeling filter is belong to next filter, update belong's original filter
        if filter_index>=filter_index_check: 
            filter_index_check = filter_index
        
        # case3(<): belong's original filter is the next filter,
        #           so channeling filter should skip those filters until round to the next belong's filter
        else:
            continue
        #############################################################################
        
        data["time_array"][filtername]        = {}
        data["observable_array"][filtername]  = {}
        data["orbit_array"][filtername]       = {}
        data["err_per_exp [ppm]"][filtername] = {}
        
        data["tr_mod_array"][filtername]      = {}
        data["tr_obs_array"][filtername]      = {}
        data["mod_noise_array"][filtername]   = {}
        data["obs_noise_array"][filtername]   = {}
        
        # the channeling filters will use all the same exposure time in the exposure_list
        for exp_t in exposure_list[filter_index]:        
            # create a time array that is based on the exposure time
            masknum = int((mid_time - start_time)*24*60*60/exp_t)

            time    = np.linspace(mid_time-masknum*exp_t/60/60/24,
                                  mid_time+masknum*exp_t/60/60/24,
                                  2*masknum+1)
            
            # create a time array that can do observation (consider shading from earth)
            #############################################################################
            observable = []
            num_orbits = tk_avail_time["transit"][target_lc_num]["num_views"]
            data["orbit_array"][filtername][f"exp_t{exp_t} [sec]"] = {}
            
            for ii in range(int(num_orbits)):
                orbit_start    = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][0]).jd
                orbit_end      = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][1]).jd

                filterdata = list(filter(lambda x: x>=orbit_start and x<=orbit_end, time))
                observable = np.append(observable, filterdata)
                
                data["orbit_array"][filtername][f"exp_t{exp_t} [sec]"][f"orbit_{ii}"] = np.array(filterdata)
            #############################################################################
                
            data["time_array"][filtername][f"exp_t{exp_t} [sec]"]        = time
            data["observable_array"][filtername][f"exp_t{exp_t} [sec]"]  = observable
                 
            # create the error array based on the information from the telescope .csv file
            #############################################################################
            if add_noise:            
                scatter_mod, scatter_obs, err_per_exp = get_noise(planet, filtername, exp_t, time, observable,
                                                                  filter_channelornot, filterchannelnum_list[filter_index], verbose)
                data["err_per_exp [ppm]"][filtername][f"exp_t{exp_t} [sec]"] = err_per_exp
                
                if scatter_mod.all()==0 or scatter_obs.all()==0 or err_per_exp==0.:
                    # belong's original filter is the next filter,
                    # so channeling filter should skip those filters until round to the next belong's filter
                    filter_index_check = filter_index_check + 1
                    break
            #############################################################################


            # the model of whole transit with "no shaded" by earth
            tr_mod = planet.transit_integrated(time, time_format="BJD_TDB", 
                                               exp_time=exp_t, time_stamp = "mid", 
                                               filter_name = filtername, 
                                               max_sub_exp_time=1)

            # the model of whole transit with "shaded" by earth
            tr_obs = planet.transit_integrated(observable, time_format="BJD_TDB", 
                                               exp_time=exp_t, time_stamp = "mid", 
                                               filter_name = filtername, 
                                               max_sub_exp_time=1)

            data["tr_mod_array"][filtername][f"exp_t{exp_t} [sec]"]      = tr_mod
            data["tr_obs_array"][filtername][f"exp_t{exp_t} [sec]"]      = tr_obs

            if add_noise:
                data["mod_noise_array"][filtername][f"exp_t{exp_t} [sec]"]   = tr_mod+scatter_mod
                data["obs_noise_array"][filtername][f"exp_t{exp_t} [sec]"]   = tr_obs+scatter_obs
                
    return data


def create_planet_tkdata(tk_datacat, tk_avail_time, target_lc_num,
                         ldc_stellar_model = "phoenix"):
    """
    <<input>>
    tk_datacat       : dictionary ; the information of planet on Twinkle catalogue      ; generated from Twinkle Stardrive database
    tk_avail_time    : dictionary ; available observation infromation                   ; generated from Twinkle Stardrive tool(orbit)
    target_lc_num    : int        ; the index of target_date in tk_avail_time
    ldc_stellar_model: string     ; the model to generate the stellar intensity profile ; default = phoenix
    
    <<output>>
    planet        : pylightcurve planet object ; synthetic light curve data     ; generated from func:create_planet_tkdata
    """
    
    # save useful variable from "Stardrive orbital tool"  
    start_time = Time(tk_avail_time["transit"][target_lc_num]["start_time"]).jd
    end_time   = Time(tk_avail_time["transit"][target_lc_num]["end_time"]).jd
    mid_time   = Time((start_time+end_time)/2., format='jd').jd 

    
    # create a plc.planet object by using "Stardrive database"
    planet = plc.Planet(name = tk_datacat["planet_name"].split(" ")[0]+"-"+tk_datacat["planet_name"].split(" ")[1], 

                ra = plc.Degrees(str(tk_datacat["star_ra"])),     # float values are assumed to be in degrees,
                                                                  # alternatively, you can provide a plc.Hours or plc.Degrees object
                                                                  # here it would be plc.Hours('22:03:10.7729')

                dec =  plc.Degrees(str(tk_datacat["star_dec"])),  # float values are assumed to be in degrees,
                                                                  # alternatively, you can provide a plc.Hours or plc.Degrees object
                                                                  # here it would be plc.Degrees('+18:53:03.548')

                stellar_logg = tk_datacat["star_logg"],               # float, in log(cm/s^2) 
                stellar_temperature = tk_datacat["star_temperature"], # float, in Kelvin
                stellar_metallicity = tk_datacat["star_metallicity"], # float, in dex(Fe/H) or dex(M/H)
                rp_over_rs = tk_datacat["rp_over_rs"],                # float, no units
                period = tk_datacat["planet_period"],                 # float, in days
                sma_over_rs = tk_datacat["sma_over_rs"],              # float, no units
                eccentricity = tk_datacat["eccentricity"],            # float, no units
                inclination = tk_datacat["inclination"],              # float values are assumed to be in degrees,
                                                                      # alternatively, you can provide a plc.Hours or plc.Degrees object
                                                                      # here it would be plc.Degrees(86.71)           

                periastron = tk_datacat["periastron"],                # float values are assumed to be in degrees,
                                                                      # alternatively, you can provide a plc.Hours or plc.Degrees object
                                                                      # here it would be plc.Degrees(0.0)

                mid_time = mid_time,                                  # float, in days
                mid_time_format = "BJD_TDB",                          # str, available formats are 
                                                                      #      JD_UTC, MJD_UTC, HJD_UTC, HJD_TDB, BJD_UTC, BJD_TDB    
                ldc_method = "claret",                                # str, default = claret, the other methods are: linear, quad, sqrt
                ldc_stellar_model = ldc_stellar_model,                # str, default = phoenix, the other model is atlas
                albedo = tk_datacat["planet_albedo"],                 # float, default = 0.15, no units 
                emissivity = 1.0                                      # float, default = 1.0, no units
                ) 
    return planet
