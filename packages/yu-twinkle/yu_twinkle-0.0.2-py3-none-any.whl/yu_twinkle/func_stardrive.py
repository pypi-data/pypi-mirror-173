import pandas as pd
import json
from astropy.time import Time
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER



def plot_avail(data):
    
    fs=18
    plt.figure(figsize=(10,6))

    for ii in range(np.shape(data)[0]):
    
        times = data_avail[ii]
        t = Time(times, format='isot', scale='utc')
        year = int(data[ii][0][0:4])
    
        year_start = Time([f'{year}-01-01T00:00:00.000'], format='isot', scale='utc')
        day_start = t[0].jd - year_start.jd
        day_end = t[1].jd - year_start.jd
    
        plt.plot([day_start,day_end],[year,year],lw=4,c='r')
        plt.scatter([day_start,day_end],[year,year],c='r',marker='d',s=80)

    plt.xlim(0,365)
    plt.ylim(2023,2030)
    plt.xlabel('Day',fontsize=fs)
    plt.ylabel('Year',fontsize=fs)
    plt.xticks(fontsize=fs-2)
    plt.yticks(fontsize=fs-2)
    plt.show()
    
    
def plot_cartopy(data, num_levels):
    
    X = data['full_ra']
    Y = data['full_dec']
    plot_data = data['full_coverage']
    
    #sun = pd.read_csv('sun_coord.csv')
    #interp_ecliptic = interp1d(sun['RA'],sun['Dec'],bounds_error=None, fill_value='extrapolate')

   #ecliptic_dec = interp_ecliptic(X)
    
    fs = 14
    
    levels = MaxNLocator(nbins=num_levels).tick_values(np.min(plot_data)-1, np.max(plot_data)+1)
    cmap = plt.get_cmap('Spectral_r')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    
    #plt.style.use("dark_background")
    
    fig = plt.figure(figsize=(10,6))
    
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide(central_longitude=180))
    
    cs = ax.contourf(X,Y,plot_data, levels = levels,
                transform=ccrs.PlateCarree(),
                cmap=cmap, norm = norm)
    
    cbar = plt.colorbar(cs, ax = ax, shrink = 0.6)
    cbar.ax.set_ylabel('Total Time Available [Days/Year]', fontsize = fs-2)
    
    ax.scatter(data['ra'],data['dec'],c='w',edgecolor='k',transform=ccrs.PlateCarree(),lw=0.5)
      
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='black', linestyle=':')
    gl.bottom_labels = False
    gl.top_labels = False
    gl.left_labels = False
    gl.right_labels = False
    gl.xlines = True
    gl.ylines = True
    
    text_ra = [60,120,180,240,300]
    for ii in text_ra:
        if ii < 100:
            ax.text(ii-5,-2.5,f'{ii}$^\circ$',transform=ccrs.PlateCarree(),fontsize=fs)
        else:
            ax.text(ii-10,-2.5,f'{ii}$^\circ$',transform=ccrs.PlateCarree(),fontsize=fs)
            
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    ax.text(-0.07, 0.55, 'Declination', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
        
    ax.text(0.5, -0.2, 'Right Ascension', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
    
    ax.text(-0.02, 0.475, '0$^\circ$', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
    ax.text(0.015, 0.68, '30$^\circ$', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
    ax.text(0.14, 0.87, '60$^\circ$', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
    ax.text(0.015, 0.24, '-30$^\circ$', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)
    ax.text(0.14, 0.06, '-60$^\circ$', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize = fs)

    plt.show()
    
    

def plot_transit(data,lc_num):
    
    t_start  = Time(data['transit'][lc_num]['start_time'])
    t_end    = Time(data['transit'][lc_num]['end_time'])
    
    t_mid    = Time((t_start.jd + t_end.jd)/2., format='jd')
    mid_date = Time(t_mid.iso , out_subfmt='date').iso

    time     = np.linspace(t_start.jd,t_end.jd,len(data['lc']))

    fs = 18
    plt.figure(figsize=(8,4))
    plt.plot(time,data['lc'],c='k',lw=2)

    for ii in range(len(data['transit'][lc_num]['viewing_times'])):
        view_start = Time(data['transit'][lc_num]['viewing_times'][ii][0])
        view_end = Time(data['transit'][lc_num]['viewing_times'][ii][1])
        plt.fill_between([view_start.jd,view_end.jd],[0.1,0.1],[1.5,1.5],color='g',alpha=0.2, label=f'Visable Channel{ii+1}')

    td = 1-min(data['lc'])
    plt.xlim(min(time),max(time))
    plt.ylim(1-1.4*td,1. + td*0.2)
    plt.xlabel('Time [BJD]',fontsize=fs)
    plt.ylabel('Relative Flux',fontsize=fs)
    plt.xticks(fontsize=fs-2)
    plt.yticks(fontsize=fs-2)
    plt.legend()
    plt.title(f"Date: {mid_date} | Coverage: {np.round(data['transit'][lc_num]['coverage']*100,1)}%",fontsize=fs-2)
    plt.show()
    

def replot_star_data(data, col):
    
    fs=18
    plt.figure(figsize=(10,6))
    plt.scatter(data['ch0']['wavelength'],data['ch0'][col],c='w',edgecolor='b')
    plt.scatter(data['ch1']['wavelength'],data['ch1'][col],c='w',edgecolor='r')
    plt.xlim(0.5,4.5)
    plt.xlabel('Wavelength [$\mu$m]',fontsize=fs)
    if col == 'error_per_hour':
        plt.ylabel('Error Per Hour [ppm]',fontsize=fs)
    elif col == 'error_per_exposure':
        plt.ylabel('Error Per Exposure [ppm]',fontsize=fs)
        plt.title(f"Exposure Time: {np.round(data['exposure_time'],2)} s",fontsize=fs-4)
    plt.xticks(fontsize=fs-2)
    plt.yticks(fontsize=fs-2)
    plt.show()
    
    
def replot_transit_data(data, num_sh):
    
    fs=18
    plt.figure(figsize=(10,6))
    plt.scatter(data['ch0']['wavelength'],data['ch0'][f'transit_snr_{num_sh}sh'],c='w',edgecolor='b')
    plt.scatter(data['ch1']['wavelength'],data['ch1'][f'transit_snr_{num_sh}sh'],c='w',edgecolor='r')
    plt.xlim(0.5,4.5)
    plt.xlabel('Wavelength [$\mu$m]',fontsize=fs)
    plt.ylabel(f'Transit SNR ({num_sh} Scale Heights)',fontsize=fs)
    plt.xticks(fontsize=fs-2)
    plt.yticks(fontsize=fs-2)
    plt.show()
    
    fs=18
    plt.figure(figsize=(10,6))
    plt.scatter(data['ch0']['wavelength'],data['ch0']['eclipse_snr'],c='w',edgecolor='b')
    plt.scatter(data['ch1']['wavelength'],data['ch1']['eclipse_snr'],c='w',edgecolor='r')
    plt.xlim(0.5,4.5)
    plt.xlabel('Wavelength [$\mu$m]',fontsize=fs)
    plt.ylabel('Eclipse SNR',fontsize=fs)
    plt.xticks(fontsize=fs-2)
    plt.yticks(fontsize=fs-2)
    plt.show()