import json, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.time import Time


def plot_synlc_vsfilter(data, exposure_list,
                        mode, filtername_list,
                        filename,
                        ymax, ymin, save=True):
    """
    <<input>>
    data            : dictionary ; synthetic light curve data            ; generated from LC_syn_tk.py
    exposure_list   : list       ; different exposure time list 
    mode            : string     ; which type of mode will be plotted    ; consider "whole tranist time"/"observable time"
    filtername_list : list(str)  ; different filter name                 ;
    filename        : string     ; the figure saving path and name
    ymax            : float      ; the y-axis max
    ymin            : float      ; the y-axis min
    save            : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    if mode=='obs':
        figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
    
    elif mode=='mod':
        figure          : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    # check the filename and its path
    pathcheck_index  = filename.split('/').index("light_curve")
    pathcheck_length = len(filename.split('/')[pathcheck_index+1:])
    
    if mode=="mod" and pathcheck_length==1:
        title   = "model"
    elif mode=="obs" and pathcheck_length==2:
        title   = "observable"
    else:
        print("The filename has something wrong!")
        """
        if mode=='obs':
            figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
        elif mode=='mod':
            figure          : figure     ; under path: Result/{target_name}/light_curve/
        """
        return
    
    target_name  = data["planet_object"].name
    stellar_name = '-'.join(target_name.split('-')[:-1])
    target_date  = data["target_date"]
    
    # get the available transit date (by the stardrive datebase)  ; generated from Twinkle Stardrive tool(orbit)
    f = open(f"Data_tk/stardrive/{stellar_name}/{target_name}/transit-results.json")
    tk_avail_time = json.load(f)
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df["Mid_date"][df["Mid_date"]==target_date].keys()[0]
        
    
    # plot !!!
    fs=28

    # generate the empty figure
    fig = plt.figure(figsize=(30,6), dpi=200, constrained_layout=True)
    if mode=="mod" and pathcheck_length==1:
        fig.suptitle(f"{target_name} transit light curve in ({title})",fontsize=fs)
    elif mode=="obs" and pathcheck_length==2:
        fig.suptitle(f"{target_name} on {target_date} transit in ({title})",fontsize=fs)
    fig.patch.set_facecolor('white')

    for i in range(len(filtername_list)):
        
        ax = fig.add_subplot(1, len(filtername_list), i+1)

        exp_label = str(exposure_list[i][0])
        
        # using "mode" parameter to determine which type
        # (mod=whole time / obs=consider earth blocked) of information is the giving data
        if mode=="mod":
            xdata   = data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            ydata_l = data["tr_mod_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            ydata_s = data["mod_noise_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"]

        elif mode=='obs':
            xdata_l = data['time_array'][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            xdata_s = data['observable_array'][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            ydata_l = data['tr_mod_array'][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            ydata_s = data['obs_noise_array'][filtername_list[i]][f"exp_t{exp_label} [sec]"]
            
            
        
        ax.set_title(f"exp_time={exp_label}s filter:{filtername_list[i]}",fontsize=fs*0.8)
        
        if mode=="obs":           
            ax.plot((xdata_l-data["mid_time"])*24,
                     ydata_l,
                     label=filtername_list[i],
                     c='k', lw=4.0)
            ax.scatter((xdata_s-data["mid_time"])*24,
                        ydata_s,
                        label=f"exp_time:{exp_label}(s) / Photon noise:"+str(data["err_per_exp [ppm]"][filtername_list[i]][f"exp_t{exp_label} [sec]"])+"(ppm)",
                        c='C'+str(i), marker='o')
            
            # because the figure x axis is detemined as -time ~ mid_time=0 ~ +time
            # we should transform the orbit windows information in the same information type
            # (i.e. use the mid_time to be the base of each orbit window)
            t_start  = Time(tk_avail_time["transit"][target_lc_num]["start_time"])
            t_end    = Time(tk_avail_time["transit"][target_lc_num]["end_time"])

            t_mid    = Time((t_start.jd + t_end.jd)/2., format='jd')

            for ii in range(len(tk_avail_time["transit"][target_lc_num]["viewing_times"])):
                view_start  = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][0])
                view_end    = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][1])

                view_start  = (view_start.jd - t_mid.jd)*24
                view_end    = (view_end.jd   - t_mid.jd)*24

                if ii == len(tk_avail_time["transit"][target_lc_num]["viewing_times"])-1:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1,
                                     label="channel converage="+round(tk_avail_time["transit"][target_lc_num]["coverage"]*100,3)+"%")
                else:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1)
        
        elif mode=="mod":
            ax.plot((xdata-data["mid_time"])*24,
                     ydata_l,
                     label=filtername_list[i],
                     c='k', lw=4.0)
            ax.scatter((xdata-data["mid_time"])*24,
                        ydata_s,
                        label=f"exp_time:{exp_label}(s) / Photon noise:"+str(data["err_per_exp [ppm]"][filtername_list[i]][f"exp_t{exp_label} [sec]"])+"(ppm)",
                        c='C'+str(i), marker='o')

        ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
        ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
        ax.tick_params(axis='x', labelsize= fs*0.6)
        ax.tick_params(axis='y', labelsize= fs*0.6)
        ax.set_xlim((min(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05,
                    (max(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05)
        ax.set_ylim(ymin, ymax)

        ax.legend(loc = 'lower right', prop={'size': fs*0.5})
    
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve/{target_date}"):
        print(f"create the folder under path:Result/{target_name}/light_curve/{target_date}")
        os.makedirs(f"Result/{target_name}/light_curve/{target_date}")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return


def plot_synlc_vsexp(data, exposure_list,
                     mode, filtername,
                     filename,
                     ymax, ymin, save=True):
    """
    <<input>>
    data            : dictionary ; synthetic light curve data            ; generated from LC_syn_tk.py
    exposure_list   : list       ; different exposure time list 
    mode            : string     ; which type of mode will be plotted    ; consider "whole tranist time"/"observable time"
    filtername      : string     ; the filter you want to compare its exposure time
    filename        : string     ; the figure saving path and name
    ymax            : float      ; the y-axis max
    ymin            : float      ; the y-axis min
    save            : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    if mode=='obs':
        figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
    
    elif mode=='mod':
        figure          : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    # check the filename and its path
    pathcheck_index  = filename.split('/').index("light_curve")
    pathcheck_length = len(filename.split('/')[pathcheck_index+1:])
    
    if mode=="mod" and pathcheck_length==1:
        title   = "model"
    elif mode=="obs" and pathcheck_length==2:
        title   = "observable"
    else:
        print("The filename has something wrong!")
        """
        if mode=="obs":
            figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
        elif mode=="mod":
            figure          : figure     ; under path: Result/{target_name}/light_curve/
        """
        return
    
    target_name = data["planet_object"].name
    stellar_name = '-'.join(target_name.split('-')[:-1])
    target_date = data["target_date"]
    
    # get the available transit date (by the stardrive datebase)  ; generated from Twinkle Stardrive tool(orbit)
    f = open(f"Data_tk/stardrive/{stellar_name}/{target_name}/transit-results.json")
    tk_avail_time = json.load(f)
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df["Mid_date"][df["Mid_date"]==target_date].keys()[0]
    
    # plot !!!
    fs=28

    # generate the empty figure
    filtername_list = data["filtername_list"]
    i = filtername_list.index(filtername)
    fig = plt.figure(figsize=(int(10*len(exposure_list[i])/2),12), dpi=200, constrained_layout=True)
    fig.suptitle(f"{target_name} on {target_date} transit in ({title})",fontsize=fs)
    fig.patch.set_facecolor('white')
    
    for j in range(len(exposure_list[i])):
        
        ax = fig.add_subplot(2, int(len(exposure_list[i])/2), j+1)

        exp_label = str(exposure_list[i][j])
        
        # using "mode" parameter to determine which type
        # (mod=whole time / obs=consider earth blocked) of information is the giving data
        if mode=="mod":
            xdata   = data["time_array"][filtername][f"exp_t{exp_label} [sec]"]
            ydata_l = data["tr_mod_array"][filtername][f"exp_t{exp_label} [sec]"]
            ydata_s = data["mod_noise_array"][filtername][f"exp_t{exp_label} [sec]"]

        elif mode=="obs":
            xdata_l = data["time_array"][filtername][str(exposure_list[i][0])]
            xdata_s = data["observable_array"][filtername][f"exp_t{exp_label} [sec]"]
        #     ydata_l = data['tr_obs_array']
            ydata_l = data["tr_mod_array"][filtername][str(exposure_list[i][0])]
            ydata_s = data["obs_noise_array"][filtername][f"exp_t{exp_label} [sec]"]
            
            
        
        ax.set_title(f"exp_time={exp_label}s filter:{filtername}",fontsize=fs*0.8)
        
        if mode=="obs":           
            ax.plot((xdata_l-data["mid_time"])*24,
                     ydata_l,
                     label=filtername,
                     c='k', lw=4.0)
            ax.scatter((xdata_s-data["mid_time"])*24,
                        ydata_s,
                        label=f"exp_time:{exp_label}(s) / Photon noise:"+str(data["err_per_exp [ppm]"][filtername][f"exp_t{exp_label} [sec]"])+"(ppm)",
                        c='C'+str(i), marker='o', s=100)
            
            # because the figure x axis is detemined as -time ~ mid_time=0 ~ +time
            # we should transform the orbit windows information in the same information type
            # (i.e. use the mid_time to be the base of each orbit window)
            t_start  = Time(tk_avail_time["transit"][target_lc_num]["start_time"])
            t_end    = Time(tk_avail_time["transit"][target_lc_num]["end_time"])

            t_mid    = Time((t_start.jd + t_end.jd)/2., format='jd')

            for ii in range(len(tk_avail_time["transit"][target_lc_num]["viewing_times"])):
                view_start  = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][0])
                view_end    = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][1])

                view_start  = (view_start.jd - t_mid.jd)*24
                view_end    = (view_end.jd   - t_mid.jd)*24

                if ii == len(tk_avail_time["transit"][target_lc_num]["viewing_times"])-1:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1,
                                     label="channel converage="+round(tk_avail_time["transit"][target_lc_num]["coverage"]*100,3)+"%")
                else:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1)
        
        elif mode=='mod':
            ax.plot((xdata-data["mid_time"])*24,
                     ydata_l,
                     label=filtername,
                     c='k', lw=4.0)
            ax.scatter((xdata-data["mid_time"])*24,
                        ydata_s,
                        label=f"exp_time:{exp_label}(s) / Photon noise:"+str(data["err_per_exp [ppm]"][filtername][f"exp_t{exp_label} [sec]"])+"(ppm)",
                        c='C'+str(i), marker='o')

        ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
        ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
        ax.tick_params(axis='x', labelsize= fs*0.6)
        ax.tick_params(axis='y', labelsize= fs*0.6)
        ax.set_xlim((min(data["time_array"][filtername][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05,
                    (max(data["time_array"][filtername][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05)
        ax.set_ylim(ymin, ymax)

        ax.legend(loc = 'lower right', prop={'size': fs*0.5})
    
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve/{target_date}"):
        print(f"create the folder under path:Result/{target_name}/light_curve/{target_date}")
        os.makedirs(f"Result/{target_name}/light_curve/{target_date}")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return
    
    
    
def plot_synlc_vsbin(data, data_bin, binsize_list,
                     mode, filtername, exp_t,
                     filename,
                     ymax, ymin, save=True):
    
    """
    <<input>>
    data            : dictionary ; synthetic light curve data                    ; generated from LC_syn_tk.py
    data_bin        : dictionary ; synthetic light curve data with data binning  ; generated from LC_syn_tk.py
    binsize_list    : list       ; different binsize list 
    mode            : string     ; which type of mode will be plotted    ; consider "whole tranist time"/"observable time"
    filtername      : string     ; the filter you want to compare its exposure time
    exp_t           : float      ; the exopsure time we want to consider
    filename        : string     ; the figure saving path and name
    ymax            : float      ; the y-axis max
    ymin            : float      ; the y-axis min
    save            : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    if mode=='obs':
        figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
    
    elif mode=='mod':
        figure          : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    # check the filename and its path
    pathcheck_index  = filename.split('/').index("light_curve")
    pathcheck_length = len(filename.split('/')[pathcheck_index+1:])
    
    if mode=="mod" and pathcheck_length==1:
        title   = "model" 
    elif mode=="obs" and pathcheck_length==2:
        title   = "observable"
    else:
        print("The filename has something wrong!")
        """
        if mode=="obs":
            figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
        elif mode=="mod":
            figure          : figure     ; under path: Result/{target_name}/light_curve/
        """
        return
    
    target_name = data["planet_object"].name
    target_date = data["target_date"]
    
    # get the available transit date (by the stardrive datebase)  ; generated from Twinkle Stardrive tool(orbit)
    f = open(f"Data_tk/stardrive/{target_name}/transit-results.json")
    tk_avail_time = json.load(f)
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df["Mid_date"][df["Mid_date"]==target_date].keys()[0]
    
    # plot !!!
    fs=28

    # generate the empty figure
    filtername_list = data["filtername_list"]
    exposure_list   = data["exposure_list"]
    
    filter_index = filtername_list.index(filtername)
    exp_label = str(exp_t)

    fig = plt.figure(figsize=(int(10*len(binsize_list)/2),12), dpi=200, constrained_layout=True)
    fig.suptitle(f"{target_name} on {target_date} in ({title}) transit with {filtername} in exposure time:{exp_t}(s) \n using differnt data binning size",fontsize=fs)
    fig.patch.set_facecolor('white')
    
    xdata_l = data["time_array"][filtername][str(exposure_list[filter_index][0])]
    ydata_l = data["tr_mod_array"][filtername][str(exposure_list[filter_index][0])]
    
    
    if mode=="mod": 
        xdata_s = data["time_array"][filtername][f"exp_t{exp_label} [sec]"]
        ydata_s = data["mod_noise_array"][filtername][f"exp_t{exp_label} [sec]"]
        
    elif mode=="obs":
        xdata_s = data["observable_array"][filtername][f"exp_t{exp_label} [sec]"]
        ydata_s = data["obs_noise_array"][filtername][f"exp_t{exp_label} [sec]"]
    
    
    for i in range(len(binsize_list)):
        ax = fig.add_subplot(2, int(len(binsize_list)/2), i+1)
        
        
        # using "mode" parameter to determine which type
        # (mod=whole time / obs=consider earth blocked) of information is the giving data
        if mode=="mod":
            xdata   = data["time_array"][filtername][f"exp_t{exp_label} [sec]"]
            ydata_l = data["tr_mod_array"][filtername][f"exp_t{exp_label} [sec]"]
            ydata_b = data["mod_noise_array"][filtername][f"exp_t{exp_label} [sec]"]

        elif mode=="obs":
            if data_bin[str(binsize_list[i])][filtername][f"exp_t{exp_label} [sec]"]:
                xdata_b = data["observable_array"][filtername][f"exp_t{exp_label} [sec]"]
                ydata_b = data["obs_noise_array"][filtername][f"exp_t{exp_label} [sec]"]
            else:
                xdata_b = data_bin[f"lc_b{binsize_list[i]}_obs"][filtername][f"exp_t{exp_label} [sec]"].time.value
                ydata_b = data_bin[f"lc_b{binsize_list[i]}_obs"][filtername][f"exp_t{exp_label} [sec]"].flux.value
        
        ax.set_title(f"data binning size={binsize_list[i]}(min) in exp_time={exp_label}s",fontsize=fs*0.8)
        
        if mode=="obs":           
            ax.plot((xdata_l-data["mid_time"])*24,
                     ydata_l,
                     label="model light curve",
                     c='k', lw=4.0)
            
            ax.scatter((xdata_s-data["mid_time"])*24,
                        ydata_s,
                        label=f"origin data / exp_time:{exp_label}(s)",
                        c='grey', marker='o')
            
            ax.scatter((xdata_b-data["mid_time"])*24,
                        ydata_b,
                        label=f"data binning size={binsize_list[i]}(min)",
                        c='red', marker='o', s=200)
            
            # because the figure x axis is detemined as -time ~ mid_time=0 ~ +time
            # we should transform the orbit windows information in the same information type
            # (i.e. use the mid_time to be the base of each orbit window)
            t_start  = Time(tk_avail_time["transit"][target_lc_num]["start_time"])
            t_end    = Time(tk_avail_time["transit"][target_lc_num]["end_time"])

            t_mid    = Time((t_start.jd + t_end.jd)/2., format='jd')

            for ii in range(len(tk_avail_time["transit"][target_lc_num]["viewing_times"])):
                view_start  = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][0])
                view_end    = Time(tk_avail_time["transit"][target_lc_num]["viewing_times"][ii][1])

                view_start  = (view_start.jd - t_mid.jd)*24
                view_end    = (view_end.jd   - t_mid.jd)*24

                if ii == len(tk_avail_time["transit"][target_lc_num]["viewing_times"])-1:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1,
                                     label="channel converage="+round(tk_avail_time["transit"][target_lc_num]["coverage"]*100,3)+"%")
                else:
                    ax.fill_between([view_start,view_end],[0.1,0.1],[1.5,1.5],color='b',alpha=0.1)
        
        elif mode=="mod":
            ax.plot((xdata-data["mid_time"])*24,
                     ydata_l,
                     label=filtername,
                     c='k', lw=4.0)
            ax.scatter((xdata-data["mid_time"])*24,
                        ydata_s,
                        label=f"exp_time:{exp_label}(s) / Photon noise:"+str(data["err_per_exp [ppm]"][filtername][f"exp_t{exp_label} [sec]"])+"(ppm)",
                        c="red", marker='o', s=200)

        ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
        ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
        ax.tick_params(axis='x', labelsize= fs*0.6)
        ax.tick_params(axis='y', labelsize= fs*0.6)
        ax.set_xlim((min(data["time_array"][filtername][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05,
                    (max(data["time_array"][filtername][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05)
        ax.set_ylim(ymin, ymax)

        ax.legend(loc = "lower right", prop={"size": fs*0.5})
    
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve/{target_date}"):
        print(f"create the folder under path:Result/{target_name}/light_curve/{target_date}")
        os.makedirs(f"Result/{target_name}/light_curve/{target_date}")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return

def plot_lc_channel_vsfilter(data, exposure_list, target_date,
                             filtername_list,
                             filtername_allchannellist,
                             filterchannelnum_list,
                             filename,
                             ymax, ymin, save=True):
    """
    <<input>>
    data                      : dictionary ; synthetic light curve data            ; generated from LC_syn_tk.py
    exposure_list             : list       ; different exposure time list 
    target_date               : string     ; the date of available observation     ; determined by LC_syn_tk.py
    filtername_list           : list(str)  ; different filter (original) name
    filtername_allchannellist : list(str)  ; different filter (+channel) name
    filterchannelnum_list     : list(int)  ; the numbers of filter channel
    filename                  : string     ; the figure saving path and name
    ymax                      : float      ; the y-axis max
    ymin                      : float      ; the y-axis min
    save                      : boolen     ; whether save the figure or not        ; default = True
    
    <<output>>
    if mode=="obs":
        figure          : figure     ; under path: Result/{target_name}/light_curve/{target_date}/
    
    elif mode=="mod":
        figure          : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    target_name = data["planet_object"].name
    stellar_name= '-'.join(target_name.split('-')[:-1])
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df['Mid_date'][df['Mid_date']==target_date].keys()[0]
    
    # plot !!!
    fs=28

    # generate the empty figure
    fig = plt.figure(figsize=(30,6), dpi=200, constrained_layout=True)
    fig.suptitle(f"{target_name} on {target_date} transit",fontsize=fs)
    fig.patch.set_facecolor('white')

    for i in range(len(filtername_list)):
        ax = fig.add_subplot(1, len(filtername_list), i+1)
        
        if filterchannelnum_list[i] == "default" and filtername_list[i] == "Twinkle_ch0_filter":
            # the color map with gradually change (.jet is one kind of cmap)
            colors = plt.cm.jet(np.linspace(0,1,59))  
            
        elif  filterchannelnum_list[i] == "default" and filtername_list[i] == "Twinkle_ch1_filter":
            # the color map with gradually change (.jet is one kind of cmap)
            colors = plt.cm.jet(np.linspace(0,1,24))
            
        else:
            colors = plt.cm.jet(np.linspace(0,1,filterchannelnum_list[i]))
        
        color_index = -1
        for j in range(len(filtername_allchannellist)):
            filtername_now     = filtername_list[i]
            filter_channel_now = filtername_allchannellist[j].split('-')

            if not filtername_now == filter_channel_now[0]:
                continue
            
            exp_label = str(exposure_list[i][0])

            # using "mode" parameter to determine which type
            # (mod=whole time / obs=consider earth blocked) of information is the giving data
            xdata   = data["time_array"][filtername_allchannellist[j]][f"exp_t{exp_label} [sec]"]
            ydata_l = data["tr_mod_array"][filtername_allchannellist[j]][f"exp_t{exp_label} [sec]"]   

            ax.set_title(f"exp_time={exp_label}s filter:{filtername_list[i]}",fontsize=fs*0.8)

            if not len(filtername_allchannellist[j].split('-'))==1:
                low_wv  = round(float(filter_channel_now[1].split('_')[0])/1e4,2)
                high_wv = round(float(filter_channel_now[1].split('_')[1])/1e4,2)
                
                ax.plot((xdata-data["mid_time"])*24, ydata_l,
                         label=f"{low_wv}-{high_wv}(um)",
                         c=colors[color_index], lw=1.0)
            
            else:
                ax.plot((xdata-data["mid_time"])*24, ydata_l,
                         label="white band", ls='--',
                         c='k', lw=3.0, zorder=100)
            
            color_index = color_index+1

            ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
            ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
            ax.tick_params(axis='x', labelsize= fs*0.6)
            ax.tick_params(axis='y', labelsize= fs*0.6)
            ax.set_xlim((min(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05,
                        (max(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05)
            ax.set_ylim(ymin, ymax)

            ax.legend(loc = 'lower right', prop={'size': fs*0.25}, ncol=2)
            
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve"):
        print(f"create the folder under path:Result/{target_name}/light_curve")
        os.makedirs(f"Result/{target_name}/light_curve")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return


def plot_lc_channel_vsexp(data, exposure_list, target_date,
                         filtername_list,
                         filtername_allchannellist,
                         filterchannelnum_list,
                         filename,
                         ymax, ymin, save=True):
    """
    <<input>>
    data                      : dictionary ; synthetic light curve data            ; generated from LC_syn_tk.py
    exposure_list             : list       ; different exposure time list 
    target_date               : string     ; the date of available observation     ; determined by LC_syn_tk.py
    filtername_list           : list(str)  ; different filter (original) name
    filtername_allchannellist : list(str)  ; different filter (+channel) name
    filterchannelnum_list     : list(int)  ; the numbers of filter channel
    filename                  : string     ; the figure saving path and name
    ymax                      : float      ; the y-axis max
    ymin                      : float      ; the y-axis min
    save                      : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    figure          : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    target_name = data["planet_object"].name
    stellar_name= '-'.join(target_name.split('-')[:-1])
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df['Mid_date'][df['Mid_date']==target_date].keys()[0]
    
    # plot !!!
    fs=28

    # generate the empty figure
    fig = plt.figure(figsize=(30,6), dpi=200, constrained_layout=True)
    fig.suptitle(f"{target_name} on {target_date} transit",fontsize=fs)
    fig.patch.set_facecolor('white')

    for i in range(len(filtername_list)):
        ax = fig.add_subplot(1, len(filtername_list), i+1)
        
        if filterchannelnum_list[i] == "default" and filtername_list[i] == "Twinkle_ch0_filter":
            # the color map with gradually change (.jet is one kind of cmap)
            colors = plt.cm.jet(np.linspace(0,1,59))  
            
        elif  filterchannelnum_list[i] == "default" and filtername_list[i] == "Twinkle_ch1_filter":
            # the color map with gradually change (.jet is one kind of cmap)
            colors = plt.cm.jet(np.linspace(0,1,24))
            
        else:
            colors = plt.cm.jet(np.linspace(0,1,filterchannelnum_list[i]))
        
        color_index = -1
        exp_label = str(exposure_list[i][0])
        
        for j in range(len(filtername_allchannellist)):
            filtername_now     = filtername_list[i]
            filter_channel_now = filtername_allchannellist[j].split('-')

            if not filtername_now == filter_channel_now[0]:
                continue
            
            # using "mode" parameter to determine which type
            # (mod=whole time / obs=consider earth blocked) of information is the giving data
            xdata   = data["time_array"][filtername_allchannellist[j]][f"exp_t{exp_label} [sec]"]
            ydata_l = data["tr_mod_array"][filtername_allchannellist[j]][f"exp_t{exp_label} [sec]"]   

            ax.set_title(f"exp_time={exp_label}s filter:{filtername_list[i]}",fontsize=fs*0.8)

            if not len(filtername_allchannellist[j].split('-'))==1:
                low_wv  = round(float(filter_channel_now[1].split('_')[0])/1e4,2)
                high_wv = round(float(filter_channel_now[1].split('_')[1])/1e4,2)
                
                ax.plot((xdata-data["mid_time"])*24, ydata_l,
                         label=f"{low_wv}-{high_wv}[um]",
                         c=colors[color_index], lw=1.0)
            
            else:
                ax.plot((xdata-data["mid_time"])*24, ydata_l,
                         label="White Band", ls='--',
                         c='k', lw=3.0, zorder=100)
            
            color_index = color_index+1

            ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
            ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
            ax.tick_params(axis='x', labelsize= fs*0.6)
            ax.tick_params(axis='y', labelsize= fs*0.6)
            ax.set_xlim((min(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05,
                        (max(data["time_array"][filtername_list[i]][f"exp_t{exp_label} [sec]"])-data["mid_time"])*24*1.05)
            ax.set_ylim(ymin, ymax)

            ax.legend(loc = 'lower right', prop={'size': fs*0.25}, ncol=2)
            
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve"):
        print(f"create the folder under path:Result/{target_name}/light_curve")
        os.makedirs(f"Result/{target_name}/light_curve")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return


def plot_lc_channel_offset(data, target_date, exp_t,
                           filtername,
                           filtername_list,
                           filtername_allchannellist,
                           filterchannelnum_list,
                           filename,
                           offset,
                           save=True):
    """
    <<input>>
    data                      : dictionary ; synthetic light curve data            ; generated from LC_syn_tk.py
    target_date               : string     ; the date of available observation     ; determined by LC_syn_tk.py
    exp_t                     : float      ; the exposure time we want to do plot
    filtername                : string     ; filter (original) name
    filtername_list           : list(str)  ; different filter (original) name
    filtername_allchannellist : list(str)  ; different filter (+channel) name
    filterchannelnum_list     : list(int)  ; the numbers of filter channel for each filter
    filename                  : string     ; the figure saving path and name
    offset                    : float      ; 
    save                      : boolen     ; whether save the figure or not        ; default= True
    
    <<output>>
    figure                    : figure     ; under path: Result/{target_name}/light_curve/
    """
    
    target_name   = data["planet_object"].name
    stellar_name  = '-'.join(target_name.split('-')[:-1])
    
    # the index of target_date in tk_avail_time
    df = pd.read_csv(f"Data_tk/stardrive/{stellar_name}/{target_name}/{target_name}_transit-date.csv")
    target_lc_num = df['Mid_date'][df['Mid_date']==target_date].keys()[0]
    
    # plot !!!
    fs=24

    # generate the empty figure
    i = filtername_list.index(filtername)

    if filterchannelnum_list[i] == "default" and filtername == "Twinkle_ch0_filter":
        # the color map with gradually change (.jet is one kind of cmap)
        colors       = plt.cm.jet(np.linspace(0,1,59))

    elif  filterchannelnum_list[i] == "default" and filtername == "Twinkle_ch1_filter":
        # the color map with gradually change (.jet is one kind of cmap)
        colors       = plt.cm.jet(np.linspace(0,1,24))
            
    else:
        colors       = plt.cm.jet(np.linspace(0,1,filterchannelnum_list[i]))
    
    fig = plt.figure(figsize=(12,1*len(colors)), dpi=200, constrained_layout=True)
    fig.suptitle(f"{target_name} in smaller wavelength interval",fontsize=fs)
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(1, 1, 1)    
    
        
    color_index  = -1
    offset_index = 0
    ymin         = 1
    yticks       = list()
    yticks_yaxis = list()
    
    for j in range(len(filtername_allchannellist)):
        filter_channel_now = filtername_allchannellist[j].split('-')

        if not filtername == filter_channel_now[0]:
            continue

        # using "mode" parameter to determine which type
        # (mod=whole time / obs=consider earth blocked) of information is the giving data
        xdata_s = data["time_array"][filtername_allchannellist[j]][f"exp_t{exp_t} [sec]"]
        ydata_s = data["mod_noise_array"][filtername_allchannellist[j]][f"exp_t{exp_t} [sec]"]-offset_index*offset
        xdata_l = data["time_array"][filtername_allchannellist[j]][f"exp_t60 [sec]"]
        ydata_l = data["tr_mod_array"][filtername_allchannellist[j]][f"exp_t60 [sec]"]-offset_index*offset
        
        ax.set_title(f"Exp_time={exp_t} [sec] / filter:{filtername} dividing into {len(colors)} channels",fontsize=fs*0.8)

        if not len(filtername_allchannellist[j].split('-'))==1:
            low_wv  = round(float(filter_channel_now[1].split('_')[0])/1e4,2)
            high_wv = round(float(filter_channel_now[1].split('_')[1])/1e4,2)

            ax.scatter((xdata_s-data["mid_time"])*24, ydata_s,
                     label=f"{low_wv}-{high_wv}[um]",
                     color=colors[color_index])
            
            ax.plot((xdata_l-data["mid_time"])*24, ydata_l,
                     ls='-', color=colors[color_index])
            yticks.append(f"{low_wv}-{high_wv}[um]")
            yticks_yaxis.append(ydata_l[0])

        else:
            ax.scatter((xdata_s-data["mid_time"])*24, ydata_s,
                     label="White Band", color='k')
            ax.plot((xdata_l-data["mid_time"])*24, ydata_l,
                     ls='-', color='k')
            yticks.append("White Band")
            yticks_yaxis.append(ydata_l[0])

        color_index  = color_index+1
        offset_index = offset_index+1
        ymin_each    = np.min(ydata_s)
        ymin         = min(ymin_each, ymin)

    ax.set_xlabel("Time Since Mid Transit [hours]",fontsize=fs*0.8)
    ax.set_ylabel("Relative Flux",fontsize=fs*0.8)
    ax.tick_params(axis='x', labelsize= fs*0.6)
    ax.tick_params(axis='y', labelsize= fs*0.6)
    ax.set_xlim((min(data["time_array"][filtername][f"exp_t{exp_t} [sec]"])-data["mid_time"])*24*1.05,
                (max(data["time_array"][filtername][f"exp_t{exp_t} [sec]"])-data["mid_time"])*24*1.05)
    ax.set_ylim(ymin-0.005, 1.005)
        
    secax = ax.secondary_yaxis("right")
    secax.set_ylabel("Wavelength [um]",fontsize=fs*0.8)
    secax.set_yticks(yticks_yaxis, labels=yticks, fontsize=fs*0.6)
    # ax.secondary_yaxis(yticks_yaxis, labels=yticks, fontsize=fs*0.6, secondary_y=True)
            
    # check if there is the save folder
    if not os.path.isdir(f"Result/{target_name}/light_curve"):
        print(f"create the folder under path:Result/{target_name}/light_curve")
        os.makedirs(f"Result/{target_name}/light_curve")
    
    if save:
        plt.savefig(f"{filename}.png")
        
    plt.show()
    
    return