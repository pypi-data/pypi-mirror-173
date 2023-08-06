import exotethys
import os, pickle, shutil
import numpy as np
import pandas as pd
# import pylightcurve as plc
from pylightcurve_master import pylightcurve_self as plc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.interpolate import interp1d

from func_pylc import self_fp_over_fs


def update_limbfile(file_path, planet_object, filtername_list, filterchannelnum_list):
    """
    Repalce the string list int the 'sail.txt' file
    <<input>>
    file_path             : string                     ;
    planet_object         : pylightcurve planet object ; synthetic light curve data       ; generated from func:create_planet_tkdata
    filtername_list       : list(str)                  ; different filter name            ;
    filterchannelnum_list : list(int)                  ; the numbers of filter channel    ;
    
    <<output>>
    **                    : running                    ; execute the update code
    """
    
    file_data=""         # the written infromation for each line
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # the following if-else func. is to replace the parameter which we what to use in exotethys files 
            if "output_path" in line:
                stellar_name = '-'.join(planet_object.name.split("-")[:-1])
                line = line.replace(line, f"output_path\t\t\t\t\tData_tk/limb/{stellar_name}\n")
            
            # stellar model will be selected by the diven model and its temperature.
            if "stellar_models_grid" in line:
                stellar_temperature = planet_object.stellar_temperature
                ldc_model           = planet_object.ldc_stellar_model
                if ldc_model == "atlas":
                    model_name = "!Phoenix_2018\t!Phoenix_2012_13\t!Phoenix_drift_2012\tAtlas_2000\t!Stagger_2015"
                    print("Exotethys will use model:Atlas_2000")
                    
                elif ldc_model == "phoenix":
                    if stellar_temperature<10000 and stellar_temperature>3000:
                        model_name = "!Phoenix_2018\tPhoenix_2012_13\t!Phoenix_drift_2012\t!Atlas_2000\t!Stagger_2015"
                        print("Exotethys will use model:Phoenix_2012_13")
                        
                    elif stellar_temperature<3000 and stellar_temperature>1500:
                        model_name = "!Phoenix_2018\t!Phoenix_2012_13\tPhoenix_drift_2012\t!Atlas_2000\t!Stagger_2015"
                        print("Exotethys will use model:Phoenix_drift_2012")
                        
                    else:
                        print("Please check the stellar temperature range!")
                        
                line = line.replace(line, f"stellar_models_grid\t\t\t{model_name}\n")
                
            # passband file need wavelength unit: A(10^-10m)
            if "passbands\t" in line:
                # add multiple filters
                passband_line = "passbands\t\t\t\t\t"
                for filtername in filtername_list:
                    passband_line = passband_line+filtername+".pass\t"
                passband_line = passband_line+"\n"
                line = line.replace(line,passband_line)
            if "wavelength_bins_files" in line:
                wavelength_bins_line = "wavelength_bins_files\t\t"
                index = 0
                for filterchannelnum in filterchannelnum_list:
                    # not need to bin
                    if filterchannelnum == 0:
                        wavelength_bins_line = wavelength_bins_line+"no_bins\t"
                        index = index+1
                        continue
                        
                    # need to pick up the filtername without "filter" inside the string
                    filter_pickname = '_'.join(filtername_list[index].split("_")[:-1])
                    wavelength_bins_line = wavelength_bins_line+filter_pickname+'_channel_'+str(filterchannelnum)+'.txt\t'
                    index = index+1
                    
                wavelength_bins_line = wavelength_bins_line+"\n"
                line = line.replace(line,wavelength_bins_line)
                    
            if "target_names" in line:
                line = line.replace(line,"target_names\t\t\t\t"+('-'.join(planet_object.name.split("-")[:-1]))+"\n")
            if "star_effective_temperature" in line:
                line = line.replace(line,"star_effective_temperature\t\t"+str(planet_object.stellar_temperature)+"\n")
            if "star_log_gravity" in line:
                line = line.replace(line,"star_log_gravity\t\t\t"+str(planet_object.stellar_logg)+"\n")
            if "star_metallicity" in line:
                if planet_object.ldc_stellar_model == 'phoenix':
                    line = line.replace(line,"star_metallicity\t\t\t0.\n")
                    print("PHOENIX models are only computed for solar metallicity stars. Setting stellar_metallicity = 0.")
                else:
                    line = line.replace(line,"star_metallicity\t\t\t"+str(planet_object.stellar_metallicity)+"\n")
            file_data += line

    with open(file_path,"w",encoding="utf-8") as f:
        f.write(file_data)
    
    return


# calculate the limb darkening coefficient by given .txt file
def run_exotethys(planet_object,
                  filtername_list, filterchannelnum_list,
                  re_exotethys=True, re_channel=True, verbose=True):
    """
    <<input>>
    planet_object         : pylightcurve planet object ; the inforamtion of planet parameter ; generated from func:create_planet_tkdata
    filtername_list       : list(string)               ; different filter name               ;
    filterchannelnum_list : list(int)                  ; the numbers of filter channel       ;
    re_exotethys          : boolen                     ; whether to re_exotethys or not
    re_channel            : boolen                     ; whether to re_channel or not
    verbose               : boolen                     ; print details or not
    
    <<progress>>
    **                    : running                    ; execute the ldc calculation code 
    
    <<output>>
    ldc['passbands']      : dict                       ; the limb darkening coefficents dict ; result calculated by Exotethys package
    """
    
    # check whether the filter need to be channeled or not
    filter_channel(filterchannelnum_list, filtername_list, re_channel, verbose)
    
    # because the planet name is HAT-P-xx-b  
    #                            HAT-P-xx-c
    #                            HAT-P-xx-...
    # the name will split into a list with "-"
    # need to merge list element
    stellar_name = '-'.join(planet_object.name.split("-")[:-1])
    path_save = 'Data_tk/limb/'+stellar_name
    
    # check if it already have file
    if not os.path.isfile(path_save+'/'+stellar_name+'_ldc.pickle'):
        print("Don't find the limb darkening coefficient file!!!")
        print("Start to call \"exotethys\" to calculate ")
        
        # check if there is the save folder
        if not os.path.isdir(path_save):
            os.makedirs(path_save)
        
        # update the file.txt exotethys need 
        shutil.copy("Data_tk/limb/sail_example.txt" , f"Data_tk/limb/{stellar_name}/sail.txt") 
        update_limbfile(f"Data_tk/limb/{stellar_name}/sail.txt", planet_object, filtername_list, filterchannelnum_list)

        # do the limb darkening coefficient calculation
        # (it will "interpolate the stellar profile" with different parameter)
        exotethys.sail.ldc_calculate(f"Data_tk/limb/{stellar_name}/sail.txt")
        
    # re_exotethys
    elif re_exotethys == True:
        print("Need to recalculate the limb darkening coefficient file!!!")
        print("Start to call \"exotethys\" to calculate ")
        
        # update the file.txt exotethys need
        shutil.copy("Data_tk/limb/sail_example.txt" , f"Data_tk/limb/{stellar_name}/sail.txt") 
        update_limbfile(f"Data_tk/limb/{stellar_name}/sail.txt",planet_object, filtername_list, filterchannelnum_list)
        
        # check if there is the save folder
        if not os.path.isdir(path_save):
            os.makedirs(path_save)

        # do the limb darkening coefficient calculation
        exotethys.sail.ldc_calculate(f"Data_tk/limb/{stellar_name}/sail.txt")  # it will "interpolate the stellar profile" with different parameter
    
    # load the result data and get coefficient
    print("Get the limb darkening coefficient file!!!")
    ldc = pickle.load(open(f"Data_tk/limb/{stellar_name}/{stellar_name}_ldc.pickle",'rb'),encoding='latin1')
    
    return ldc['passbands']



def filter_channel(filterchannelnum_list, filtername_list, re_channel, verbose):
    """
    <<input>>
    filterchannelnum_list : list(int) ; the numbers of filter channel
    filtername_list       : list(str) ; different filter name 
    re_channel            : boolen    ; whether to re_channel or not
    verbose               : boolen    ; print details or not
    
    <<output>>
    **                    : running   ; execute the update code
    """
    if not len(filterchannelnum_list)==len(filtername_list):
        print("filterchannelnum_list should have same len as filtername_list")
        return
    
    index = 0
    for filterchannelnum in filterchannelnum_list:
        
        filtername = filtername_list[index]    
        filter_pickname = '_'.join(filtername.split("_")[:-1])  # need to pick up the filtername without "filter" inside the string
        
        # if nobins, we do not need to generate the additional channel filter files
        if filterchannelnum == 0:
            print(f"The filter {filter_pickname} don't need to do filter channeling")
            index = index+1
            continue
            
        # if there was the default channel data, just pick the information and print them
        elif filterchannelnum == 'default' and not re_channel:
            print(f"The filter {filter_pickname} use the default filter channeling")
            
            df_filter  = pd.read_csv(f"Data_tk/passband/channel/{filter_pickname}_channel_default.txt",
                         sep='\t', header=None, names=['low', 'high'])    # load the filter data
            
            print(f"Divide {filter_pickname} into {len(df_filter)} wavelength channels")
            if verbose:
                print(df_filter)
                        
            fig = plt.figure(figsize=(8,6), dpi=100)
            channelplot = mpimg.imread(f'Data_tk/passband/channel/{filter_pickname}_channel_default'+'.png')
            plt.imshow(channelplot, aspect='auto')
            plt.axis('off')
            plt.show()
            
            index = index+1
            continue
            
        # if there was the channel data generated before, just pick the information and print them
        elif os.path.isfile(f"Data_tk/passband/channel/{filter_pickname}_channel_{filterchannelnum}.txt") and not re_channel:
            print(f"The {filter_pickname} filter channel file with {filterchannelnum} channel was generated before!")

            df_filter  = pd.read_csv(f"Data_tk/passband/channel/{filter_pickname}_channel_{filterchannelnum}.txt",
                                     sep='\t', header=None, names=['low', 'high'])    # load the filter data
            
            print(f"Divide {filter_pickname} into {filterchannelnum} wavelength channels")
            print(f"Each channel has a {(df_filter.loc[0]['high']-df_filter.loc[0]['low'])}(A) wavelength interval.")
            if verbose:
                print(df_filter)
            
            fig = plt.figure(figsize=(8,6), dpi=100)
            channelplot = mpimg.imread(f"Data_tk/passband/channel/{filter_pickname}_channel_{filterchannelnum}.png")
            plt.imshow(channelplot, aspect='auto')
            plt.axis('off')
            plt.show()
            
            index = index+1
            continue
            
        index     = index+1
        
        print(f"run/re_channel the filter channeling process of {filtername} in {filterchannelnum} number of channeling")
        
        if filterchannelnum == 'default':
            print(f"The filter {filter_pickname} use the default filter channeling")
            df_filter  = pd.read_csv(f"Data_tk/passband/{filtername}.pass", sep='\t',
                         header=None, names=['Wavelength(A)', 'tranmission rate'])    # load the filter data
            wavelength = df_filter['Wavelength(A)'].to_numpy()
            
            df  = pd.read_csv(f"Data_tk/passband/channel/{filter_pickname}_channel_default.txt",
                                sep='\t', header=None, names=['low', 'high'])    # load the filter data
            
            print(f"Divide {filter_pickname} into {len(df)} wavelength channels")
            print(df)
            
            # plot the channeling filter
            [df['low'].to_list()[0]-1]+df['high'].to_list()
            channel_point_df = np.array([df['low'].to_list()[0]-1]+df['high'].to_list())
            # beacuse the first interval will be left limit < interval <= right limit,
            # the first left limit will be missed, so we apprend one more point
            
            filterchannelnum_savefig = filterchannelnum
            filterchannelnum = len(df)
        
        else:
            df_filter  = pd.read_csv(f"Data_tk/passband/{filtername}.pass", sep='\t',
                                     header=None, names=['Wavelength(A)', 'tranmission rate'])    # load the filter data

            wavelength = df_filter['Wavelength(A)'].to_numpy()
            channel_point = np.linspace(wavelength.min(),wavelength.max(), filterchannelnum+1)

            df = pd.DataFrame()
            df['low']  = channel_point[:-1]
            df['high'] = channel_point[1:]

            df.to_csv(f"Data_tk/passband/channel/{filter_pickname}_channel_{filterchannelnum}.txt", sep='\t', index=False, header=False)

            print(f"Divide {filter_pickname} into {filterchannelnum} wavelength channels")
            print(f"Each channel has a {(channel_point[1]-channel_point[0])}(A) wavelength interval.")
            print(df)
        
            # plot the channeling filter
            channel_point_df = np.append(channel_point[0]-1, channel_point[1:])
            # beacuse the first interval will be left limit < interval <= right limit,
            # the first left limit will be missed, so we apprend one more point
            
            filterchannelnum_savefig = filterchannelnum
        
        # add the label of belonging channel for each row
        df_filter['channel'] = pd.cut(df_filter['Wavelength(A)'], channel_point_df, labels=list(range(filterchannelnum)))
        
        # plot
        plot_filterchannel(filterchannelnum, filter_pickname, df_filter, df, filterchannelnum_savefig)
        
    return


def plot_filterchannel(filterchannelnum, filter_pickname, df_filter, df, filterchannelnum_savefig):
    """
    <<input>>
    filterchannelnum         :  int        ; the numbers of filter channel
    filter_pickname          :  string     ; (original) filter name 
    df_filter                :  dataframe  ; the table of (original) filter transmission information in its range
    df                       :  dataframe  ; the table of (original) filter channel information with left/right edge
    filterchannelnum_savefig :  int/string ; the string when saving the channel filter profile figure
    
    <<output>>
    figure                   : figure       ;  under path: 'Data_tk/passband/channel/
    """

    colors = plt.cm.jet(np.linspace(0,1,filterchannelnum))  # the color map with gradually change (.jet is one kind of cmap)

    fig = plt.figure(figsize=(8,6), dpi=100, constrained_layout=True)
    fig.suptitle(f"The channeling {filter_pickname} filter with {filterchannelnum} channels")
    fig.patch.set_facecolor('white')
    ax  = fig.add_subplot(111)
    for i in range(filterchannelnum):
        ymean  = df_filter['tranmission rate'][df_filter.channel==i].mean()
        each_w = df_filter['Wavelength(A)'][df_filter.channel==i].to_list()
        each_t = df_filter['tranmission rate'][df_filter.channel==i].to_list()

        # consider the separated channel details (the upper and lower boundary probem when face separated line),
        # using interpolation to find the appropriate value when wavelength go to separate into two channels
        if i == 0:                      # when the left limit of boundary
            f_right = interp1d([each_w[-1], df_filter['Wavelength(A)'][df_filter.channel==i+1].to_list()[0]],
                               [each_t[-1], df_filter['tranmission rate'][df_filter.channel==i+1].to_list()[0]])

            each_w = [df.loc[i]['low']] + each_w + [df.loc[i]['high']         , df.loc[i]['high']]
            each_t = [0] + each_t + [f_right(df.loc[i]['high']), 0]

        elif i == filterchannelnum-1:   # when the right limit of boundary
            f_left  = interp1d([df_filter['Wavelength(A)'][df_filter.channel==i-1].to_list()[-1], each_w[0]],
                               [df_filter['tranmission rate'][df_filter.channel==i-1].to_list()[-1], each_t[0]])

            each_w = [df.loc[i]['low'], df.loc[i]['low']] + each_w + [df.loc[i]['high']]
            each_t = [0, f_left(df.loc[i]['low'])] + each_t + [0]

        else:                           # boundary of each channel
            f_left  = interp1d([df_filter['Wavelength(A)'][df_filter.channel==i-1].to_list()[-1], each_w[0]],
                               [df_filter['tranmission rate'][df_filter.channel==i-1].to_list()[-1], each_t[0]])
            f_right = interp1d([each_w[-1], df_filter['Wavelength(A)'][df_filter.channel==i+1].to_list()[0]],
                               [each_t[-1], df_filter['tranmission rate'][df_filter.channel==i+1].to_list()[0]])

            each_w = [df.loc[i]['low'], df.loc[i]['low']] + each_w + [df.loc[i]['high'], df.loc[i]['high']]
            each_t = [0, f_left(df.loc[i]['low'])] + each_t + [f_right(df.loc[i]['high']),0]

        each_w = np.array(each_w)
        each_t = np.array(each_t)

        ax.plot(each_w/1e4, each_t, color=colors[i])
        ax.annotate(f"c{i}", xy=(each_w.mean()/1e4, ymean))
        ax.set_xlabel('Wavelength(um)')
        ax.set_ylabel('tranmission rate')
        ax.set_ylim(0,1)

    plt.savefig(f"Data_tk/passband/channel/{filter_pickname}_channel_{filterchannelnum_savefig}.png")
    plt.show()
    
    return
        
    
def gen_filtername_allchannellist(ldc_filter, filtername_list, filterchannelnum_list, planet_tk):
    """
    <<input>>
    ldc_filter                : dict                       ; the limb darkening coefficents dict
    filtername_list           : list(str)                  ; different filter (original) name
    filterchannelnum_list     : list(int)                  ; the numbers of filter channel
    planet_tk                 : pylightcurve planet object ; the inforamtion of planet parameter ; generated from func:create_planet_tkdata

    <<output>>
    filtername_allchannellist :  list(str)  ;   different filter (+channel) name
    """
    
    filter_index = 0
    filtername_allchannellist = []
    for filter_name in list(ldc_filter.keys()):

        filter_pickname = filter_name.split(".pass")[0]
        filter_pickwave = '_'.join(filter_name.split(".pass")[1].split("_")[1:])

        if filtername_list[filter_index] != filter_pickname:
            filter_index= filter_index+1

        if (filterchannelnum_list[filter_index] == 0) and (filter_pickwave != ''):
            continue

        # here, the self_fp_over_fs need the filter name to load the "transmission rate"
        filter_fp= self_fp_over_fs(planet_tk.rp_over_rs,
                                     planet_tk.sma_over_rs,
                                     planet_tk.albedo,
                                     planet_tk.emissivity,
                                     planet_tk.stellar_temperature,
                                     filter_pickname,
                                     filter_pickwave)

        ldc1, ldc2, ldc3, ldc4 = ldc_filter[filter_name]['claret4']['coefficients']

        if filter_pickwave == '':
            print(filter_pickname, ldc_filter[filter_name]['claret4']['coefficients'])
            planet_tk.add_filter(filter_pickname+filter_pickwave,  planet_tk.rp_over_rs,
                                 ldc1, ldc2, ldc3, ldc4, filter_fp)

            filtername_allchannellist.append(filter_pickname)
        else:
            print(filter_pickname+'-'+filter_pickwave, ldc_filter[filter_name]['claret4']['coefficients'])
            planet_tk.add_filter(filter_pickname+'-'+filter_pickwave,  planet_tk.rp_over_rs,
                                 ldc1, ldc2, ldc3, ldc4, filter_fp)

            filtername_allchannellist.append(filter_pickname+'-'+filter_pickwave)
            
    return filtername_allchannellist