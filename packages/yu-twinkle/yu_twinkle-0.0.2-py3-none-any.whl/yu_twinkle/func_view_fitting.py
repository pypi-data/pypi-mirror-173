import pickle, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time


def get_fitting_result(target_name, target_date, binsize_list, filtername_list, exposure_list):
    """
    <<input>>
    target_name     : string     ; the target name
    target_date     : string     ; the date of available observation     ; determined by LC_syn_tk.py
    binsize_list    : list(int)  ; the binsize list for all binsize
    filtername_list : list(str)  ; different filter name 
    exposure_list   : list(int)  ; different exposure time list 
    
    <<output>>
    fitting result  : dictionary ; getting the fitting result form each fitting result's folder
    """
    
    stellar_name= '-'.join(target_name.split('-')[:-1])
    data_bin = pickle.load(open(f"Savefile/{stellar_name}/{target_name}/{target_date}/time_flux/{target_name}_bin_{target_date}.pickle",'rb'))
    
    data_fitting = {}
    
    # data_fitting["rp"]        = {}
    # data_fitting["rp_low"]    = {}
    # data_fitting["rp_high"]   = {}
    data_fitting["tmid"]      = {}
    data_fitting["tmid_low"]  = {}
    data_fitting["tmid_high"] = {}
    data_fitting["rechi"]     = {}
    
    # for mode in ['mod', 'obs']:
    for mode in ["obs"]:
        # data_fitting["rp"][mode]        = {}
        # data_fitting["rp_low"][mode]    = {}
        # data_fitting["rp_high"][mode]   = {}
        data_fitting["tmid"][mode]      = {}
        data_fitting["tmid_low"][mode]  = {}
        data_fitting["tmid_high"][mode] = {}
        data_fitting["rechi"][mode]     = {}

        for bin_t in binsize_list:  
            # for finding the path of the fitting result
            if bin_t == 0:
                bin_name = "non-binned"
            else:
                bin_name = f"bin{bin_t}"
            # data_fitting["rp'][mode][bin_t]        = {}
            # data_fitting["rp_low'][mode][bin_t]    = {}
            # data_fitting["rp_high"][mode][bin_t]   = {}
            data_fitting["tmid"][mode][bin_t]      = {}
            data_fitting["tmid_low"][mode][bin_t]  = {}
            data_fitting["tmid_high"][mode][bin_t] = {}
            data_fitting["rechi"][mode][bin_t]     = {}

            index = 0
            for filtername in filtername_list:
                # the list to save the information of each exposure time
                # in the same filter/ bin_t
                # rp_t        = []
                # rp_low_t    = []
                # rp_high_t   = []
                tmid_t      = []
                tmid_low_t  = []
                tmid_high_t = []
                rechi_t     = []

                # data_fitting["rp"][mode][bin_t][filtername]        = {}
                # data_fitting["rp_low"][mode][bin_t][filtername]    = {}
                # data_fitting["rp_high"][mode][bin_t][filtername]   = {}
                data_fitting["tmid"][mode][bin_t][filtername]      = {}
                data_fitting["tmid_low"][mode][bin_t][filtername]  = {}
                data_fitting["tmid_high"][mode][bin_t][filtername] = {}
                data_fitting["rechi"][mode][bin_t][filtername]     = {}

                # search the rp/rs&t_mid we want from each exposure time's fitting result               
                for exp_t in exposure_list[index]:
                    if not bin_name == "non-binned":             
                        if data_bin[f"check_expvsbin_t{bin_t} [min]"][filtername][f"exp_t{exp_t} [sec]"]:
                            continue
                    
                    path = f"Savefile/{stellar_name}/{target_name}/{target_date}/fitting/{bin_name}/{bin_name}_t{exp_t}_{mode}_{filtername}_fit/results.txt"
                    df = pd.read_csv(path , sep='\s+')    # the .txt result file

                    # row_rp    = df.loc[df['#'] == 'rp_'+filtername]
                    row_tmid  = df.loc[df['#'] == "T_mid_0"]
                    row_rechi = df.loc[df['#'] == "#Reduced"]

                    # data_fitting['rp'][mode][bin_t][filtername][exp_t]        = float(row_rp['variable'].values)
                    # data_fitting['rp_low'][mode][bin_t][filtername][exp_t]    = float(row_rp['result'].values)
                    # data_fitting['rp_high'][mode][bin_t][filtername][exp_t]   = float(row_rp['uncertainty'].values)
                    data_fitting["tmid"][mode][bin_t][filtername][exp_t]      = float(row_tmid["variable"].values)
                    data_fitting["tmid_low"][mode][bin_t][filtername][exp_t]  = float(row_tmid["result"].values)
                    data_fitting["tmid_high"][mode][bin_t][filtername][exp_t] = float(row_tmid["uncertainty"].values)
                    data_fitting["rechi"][mode][bin_t][filtername][exp_t]     = float(row_rechi["uncertainty"].values)


                index = index + 1
    
    return data_fitting


def gen_fitresult_csv(data_dict, binsize_list, filtername_list, exposure_list, target_name, target_date, real_mid_time):
    """
    <<input>>
    data_dict       : dtaframe   ; the csv file of fthe fitting result   ; generated func:gen_fitresult_csv=
    binsize_list    : list(int)  ; the binsize list for all binsize
    filtername_list : list(str)  ; different filter name 
    exposure_list   : list(int)  ; different exposure time list 
    target_name     : string     ; the target name
    target_date     : string     ; the date of available observation     ; determined by LC_syn_tk.py
    real_mid_time   : float      ; the real mid_time time we given in the Twinkle data
    
    <<output>>
    csv file        : csv dataframe ; under path: Result/{target_name}/fitting/{target_date}/fitting_result_bin_{target_name}_{target_date}.csv
    """

    data_csv = {}
    data_csv = pd.DataFrame(data_csv)

    for mode in ["obs"]:
    # for mode in ['mod', 'obs']:

        # for bin_element in [0]:
        for bin_t in binsize_list:
            for filtername in filtername_list:
                filter_index = filtername_list.index(filtername)

                data_csv_ = {
                    "time_mode"          : "",
                    "binsize [min]"      : "",
                    "exp_t [sec]"        : "",
                    "filtername"         : "",
                    "$\Delta$tmid [min]" : data_dict["tmid"][mode][bin_t][filtername],
                    "tmid_errorbar [min]": "",
                    "tmid_low [min]"     : data_dict["tmid_low"][mode][bin_t][filtername],
                    "tmid_high [min]"    : data_dict["tmid_high"][mode][bin_t][filtername],
                    "tmid [BJD]"         : data_dict["tmid"][mode][bin_t][filtername],
                    # "$\Delta$rp [%]"    : data_dict['rp'][mode][bin_t][filtername],
                    # "rp_errorbar [%]"   : "",
                    # "rp_low [%]"        : data_dict['rp_low'][mode][bin_t][filtername],
                    # "rp_high [%]"       : data_dict['rp_high'][mode][bin_t][filtername],
                    # "rp [rp/rs]"         : data_dict['rp'][mode][bin_t][filtername],
                    "rechi"              : data_dict["rechi"][mode][bin_t][filtername]
                }

                data_csv_ = pd.DataFrame(data_csv_)
                
                
                data_csv_["binsize [min]"] = [bin_t]*len(data_csv_.index)
                data_csv_["exp_t [sec]"]   = data_csv_.index
                data_csv_["time_mode"]     = [mode]*len(data_csv_.index)
                data_csv_["filtername"]    = [filtername]*len(data_csv_.index)


                data_csv_["$\Delta$tmid [min]"]  = round((data_csv_["$\Delta$tmid [min]"]-real_mid_time)*24*60, 3)
                data_csv_["tmid_errorbar [min]"] = round((data_csv_["tmid_high [min]"]+(-data_csv_["tmid_low [min]"]))*24*60, 2)
                data_csv_["tmid_low [min]"]      = round(data_csv_["tmid_low [min]"]*24*60, 2)
                data_csv_["tmid_high [min]"]     = round(data_csv_["tmid_high [min]"]*24*60, 2)
                data_csv_["tmid [BJD]"]          = round(data_csv_["tmid [BJD]"], 5)


                # data_csv_["$\Delta$rp [%]"]     = round(((data_csv_["$\Delta$rp [%]"]-real_rp)/real_rp)*100, 3)
                # data_csv_["rp_errorbar [%]"]    = round(((data_csv_["rp_high [%]"]+(-data_csv_["rp_low [%]"]))/real_rp)*100, 2)
                # data_csv_["rp_low [%]"]         = round((data_csv_["rp_low [%]"]/real_rp)*100, 2)
                # data_csv_["rp_high [%]"]        = round((data_csv_["rp_high [%]"]/real_rp)*100, 2)
                # data_csv_["rp [rp/rs]"]         = round(data_csv_["rp [rp/rs]"], 3)

                data_csv_["rechi"]              = round(data_csv_["rechi"], 3)


                data_csv = pd.concat([data_csv, data_csv_])


    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/fitting/{target_date}"):
        print(f"create the folder under path:Result/{target_name}/fitting/{target_date}")
        os.makedirs(f"Result/{target_name}/fitting/{target_date}")

    data_csv.to_csv(f"Result/{target_name}/fitting/{target_date}/fitting_result_bin_{target_name}_{target_date}.csv", index=False)
    
    return data_csv


def plot_midt_fitting_result(df, target_name, target_date, binsize_list,
                             mode, filtername, real_mid_time,
                             filename,
                             save=True):
    """
    <<input>>
    df              : dtaframe   ; the csv file of fthe fitting result   ; generated func:gen_fitresult_csv
    target_name     : string     ; the target name
    target_date     : string     ; the date of available observation     ; determined by LC_syn_tk.py
    binsize_list    : list(int)  ; the binsize list for all binsize
    mode            : string     ; which type of mode will be plotted    ; consider "whole tranist time"/"observable time"
    filtername      : string     ; the filtername that you want to generate its fitting result figure
    real_mid_time   : float      ; the real mid_time time we given in the Twinkle data
    filename        : string     ; the figure saving path and name
    save            : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    figure          : figure     ; under path: Result/{target_name}/fitting/{target_date}/
    """
    
    fs=20

    expt_list   = [60, 120, 240, 480]
    marker_list = ['o', 'X', '^', 's']
    ls_list     = ['-', '--', '-.', ':']
    colors_list = ['C0', 'C1', 'C2', 'C3']

    fig1 = plt.figure(figsize=(10,6), dpi=200, tight_layout=True)
    fig1.suptitle(target_name+" with "+filtername+": compare different parameters\n"+\
                  "Mid_Time="+Time(real_mid_time, format='jd').iso ,fontsize=fs)
    fig1.patch.set_facecolor('white')


    # plot !!!
    ax = fig1.add_subplot(1, 1, 1)
    ax.set_title(f"\"Mid_Time\" ({mode})",fontsize=fs*0.8)

    ax.plot([1,2,3,4,5,6,7],
        np.full(7, 0.0),
        color='k')     

    yt_max = 0
    yt_min = 0

    # ==========================================================================================================
    for exp_t in expt_list:
        for filtername in ["Twinkle_ch0_filter"]:
            df_exp   = df[df["exp_t [sec]"]==exp_t]

            df_filter_bool = df_exp["filtername"]==filtername

            tmid_obs      = df_exp[df_filter_bool]["$\Delta$tmid [min]"].values
            tmid_low_obs  = df_exp[df_filter_bool]["tmid_low [min]"].values
            tmid_high_obs = df_exp[df_filter_bool]["tmid_high [min]"].values

            yt_max = max(yt_max, max(tmid_obs + tmid_high_obs))
            yt_min = min(yt_min, min(tmid_obs + tmid_low_obs))

            # 檢查這一個binsize缺少了哪一些 要挑哪一些
            x_list = []
            bin_list_df   = df_exp[df_filter_bool]["binsize [min]"].values
            for bin_t_thisbinlist in bin_list_df:
                x_index = binsize_list.index(bin_t_thisbinlist)
                x_list.append(x_index)
            x_list = np.array(x_list)
    # ==========================================================================================================

        ax.errorbar(x_list+1, tmid_obs,
                    yerr = [-tmid_low_obs, tmid_high_obs],
                    fmt = '', markersize=8, capsize=8, lw=2,
                    color=colors_list[expt_list.index(exp_t)],
                    marker = marker_list[expt_list.index(exp_t)],
                    ls = ls_list[expt_list.index(exp_t)],
                    zorder = 7-expt_list.index(exp_t), alpha=1,
                    label = f"exp_t={exp_t}[sec]")

        ax.set_xlabel("Data binning [min]",fontsize=fs*0.6)
        ax.set_ylabel("$\Delta$Mid_T [min]",fontsize=fs*0.6)
        ax.tick_params(axis='y', labelsize= fs*0.5)

        xticks = ["non-binned", "bin5", "bin10", "bin15", "bin20", "bin25", "bin30"]
        # xticks = df[df['exp_t [sec]']==60][df[df['exp_t [sec]']==60]['filtername']==filtername]['binsize [min]'].values
        ax.set_xticks(np.arange(7)+1, labels=xticks, fontsize=fs*0.6)
        ax.axis(ymin=yt_min*1.5,ymax=yt_max*1.2)
        ax.legend(loc = 'lower right', prop={'size': fs*0.5}, ncol=4)

    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/fitting/{target_date}"):
        print(f"create the folder under path:Result/{target_name}/fitting/{target_date}")
        os.makedirs(f"Result/{target_name}/fitting/{target_date}")

    if save:
        plt.savefig(f"{filename}.png")
    plt.show()
    
    return


