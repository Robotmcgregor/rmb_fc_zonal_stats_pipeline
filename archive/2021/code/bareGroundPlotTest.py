#!/usr/bin/env python

# import modules.
from __future__ import print_function, division

'''
bareGroundPlot.py
=================

Description: This reads in the fractonal cover zonal stats and the rainfall zonal stats csv file and produces two time series plots per site.
Plot 1: bare ground
plot 2: all bands for interpretation.

This script also reads in the star transect shapefile for historic site visists and plots this information on each plot using the axvline function.

Author Grant Staben
email grant.staben@nt.gov.au
Date: 21/09/2020
Version: 1.0

Modified: Rob McGregor
email: Robert.Mcgregor@nt.gov.au
Date: 27/10/2020
Version: 2.0

###############################################################################################

MIT License

Copyright (c) 2020 Rob McGregor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

##################################################################################################

Input requirements:
-------------------

1.	A DataFrame produced from an open csv titled (output_zonal_stats). The csv should be produced by running zonal stats with the folowing features: 'site_date', 'year', 
    'month', 'day', b1_count', 'b2_count', 'b3_count', 'b1_mean', 'b2_mean' and b3_mean'. Expected format is produced from step1_6_fc_zonal_stats.py

2.  A DataFrame produced from an open csv titled (outputRainfall). The csv should be produced by running zonal stats with the folowing features: ''imDate'', 'year', 
    'month', 'site', 'prop_name', 'mean'. Expected format is produced from monthlyRainfallZponalStats.py

3.  A shapefile containing NT Star Transect information (i.e. "Z:\Scratch\Zonal_Stats_Pipeline\shapefiles\NT_StarTransect_20200713.shp") with the features: 'siteTitle' and 'dateTitle.


4.  rain_finish_date A string variable conatining the finish date (i.e. 'YYYY_MM_DD') for each plot as a string. the varible is produced from the last rainfall image used in step1_2_list_of_rainfall_images.py


'day', b1_count', 'b2_count', 'b3_count', 'b1_mean', 'b2_mean' and b3_mean'.
2.	Singlepart polygon shapefile or shapefiles with the following attributes “LAISKEY”, “PROP_NAME”, “WGS52_ha” and “WGS53_ha”. The shapefiles with correct attributes can be derived from: select_and_project_property_shapefiles_calc_area.py (McGregor, 2020).
3.	A final classification must been applied to the MODIS derived NAFI fire scars file names include (i.e. MTHS.tif or MTH.tif). However, if you wish to include the current year (not complete) you will need to pre-process that raster. Pre-processing can be derived from: modis_raster_12_month_classification.py (McGregor, 2020).

===================================================================================================

Command arguments:
------------------

None


======================================================================================================

Input requirements (used in script):
------------------------------------

--export_dir_path: str
string object containing the path to a newly created temporary directory titled 'YYYYMMDD_HHMM' - created in the location specified by command argument exportdir.
  
--output_zonal_stats: DataFrame
open DataFrame containing the fractonal cover zonal stats derived from step1_6_fc_zonal_stats.py.  

--complete_tile: str
string object contining the Landsat tile name created by step1_6_fc_zonal_stats.py

--rain_finish_date: str
string object containing the year month and day of the last image available (YYYY + '-' + MM + '-30').

--outputRainfall: DataFrame
DataFrame object containing the rainfall zonal stats results containing in the output_list.



variables:
-----------

integrated: DataFrame
DataFrame object that srores the shapefile containing previous NT Star Transect information.

siteS: DataFrame
DataFrame conating a suset of the outputRainfall DataFrame based on the unique identifier 'site'.

siteLabel: str
string object containing the site name as a string.

propertyName: list
List object containing a list of the unique outputRainfall DataFrame feature 'prop_name'.

siteSsort: Series
Series object containing the sorted dates from the outputRainfall DataFrame.

siteDate: list
list object conataining the unique outputRainfall feature 'siteDate'

siteDate: list
list object conataining the unique outputRainfall feature 'siteDate'

siteSsort: list
list object conataining the unique siteS feature 'date'.

date: Series
Series object zzzz

rain: Series
Series object to the rainafall mean as 'mm' fderived from the siteSsort zzzz feature 'mean'.

lsat_bare: DataFrame
Subset of the 

lsat_bare: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'. 

date_b: list/series zzzz
list object containing the sorted dateTime variables from the dateTime feature od fthe lsat_bare DataFrame.

datefit: DataFrame zzzz
DataFrame object from the Series object with the sorted dist date_b appended

bare_mean: zzzz
zzzzz containing the bare ground mean value.

b_mean_fl: zzzzzzzz containing a rolling mean derived from the bare_mean zzzz and the zzzz input.

interp: Series
Series object conataining an interpolated linier value derived from the b_mean_fl (limit_direction ='both')


vals = interp.values

333333333333333333333333333333333333333333333333333333333333333333333333333333

lsat_pv: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'. 

date_pv: list/series zzzz
list object containing the sorted dateTime variables from the dateTime feature of the lsat_pv DataFrame.

datefit2: DataFrame zzzz
DataFrame object from the Series object with the sorted dist date_pv appended

pv_mean: zzzz
zzzzz containing the bare ground mean value.

pv_mean_fl: zzzzzzzz containing a rolling mean derived from the pv_mean zzzz and the zzzz input.

# interporlate the missing values to enable it to be plotted 
interp2: zzzz
zzzz object conataining an interpolated linier value derived from the b_mean_fl (limit_direction ='both')

vals_pv = interp2.values


444444444444444444444444444444444444444444444444
    
lsat_npv: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'. 

date_npv: list/series zzzz
list object containing the sorted dateTime variables from the dateTime feature of the lsat_npv DataFrame.

datefit2: DataFrame zzzz
DataFrame object from the Series object with the sorted dist date_npv appended

npv_mean: zzzz
zzzzz containing the bare ground mean value.

npv_mean_fl: zzzzzzzz containing a rolling mean derived from the npv_mean zzzz and the zzzz input.

# interporlate the missing values to enable it to be plotted 
interp3: zzzz
zzzz object conataining an interpolated linier value derived from the b_mean_fl (limit_direction ='both')

vals_npv = interp3.values

55555555555555555555555555555555555555555555555555555

complete_tile: str
String object containing the Landsat tile number as a string whcih is currently being plotted. complete_tile is derived by the script fcZonalStats.

siteLabel

startDate: str
string object containing the rainfall start date for the plots (i.e. 'YYYY-MM-01')

finishDate: str
string object containing the rainfall finish date for the plots - derived by the step1_2_list_of_rainfall_images.py script (i.e. 'YYYY-MM-01')
    

========================================================================================================

'''


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")
mpl.rcParams['figure.figsize'] = (30, 8.0)



def previousVisits(): 
    '''
    Read in and clean the integrated site shapefile for previous site visit information.
    '''
    # Import the integrated site shapefile for previous visit dates to the site.
    integrated = gpd.read_file(r"Z:\Scratch\Zonal_Stats_Pipeline\shapefiles\NT_StarTransect_20200713.shp")
    # convert site name to capital letters
    integrated['siteTitle'] = integrated.site.str.upper()
    integrated['dateTime'] = integrated.obs_time.apply(pd.to_datetime)
    #integrated.to_csv(r'Z:\Scratch\Zonal_Stats_Pipeline\checkIntegrated.csv')
    
    return(integrated)
    

def importRainfallData(outputRainfall):    
    
    # create the date time field and sort the values
    outputRainfall['year'] = outputRainfall['imDate'].map(lambda x: str(x)[:4])
    outputRainfall['month'] = outputRainfall['imDate'].map(lambda x: str(x)[4:6])
    outputRainfall['Date'] = outputRainfall['year']  + '/' + outputRainfall['month'] + '/' + '15'
    outputRainfall.sort_values(['Date'])
    
    # convert site_date feature from object to datetime
    outputRainfall['site_date'] = pd.to_datetime(outputRainfall['site_date'])
    
    return (outputRainfall)
    
    
def importZonalStats(outputZonalStats):    


    outputZonalStats['site_date'] = pd.to_datetime(outputZonalStats['site_date'])
    # remove all data points which do not have at least 3 valid pixels to produce the average bare ground for a site
    outputZonalStats = outputZonalStats.loc[(outputZonalStats['b1_count'] > 3)]
    # create the date time field and sort the values
    outputZonalStats['dateTime'] = outputZonalStats['year'].apply(str) +"/"+ outputZonalStats['month'].apply(str)+"/"+outputZonalStats['day'].apply(str)
    outputZonalStats['dateTime'] = outputZonalStats.dateTime.apply(pd.to_datetime)
    # sort values by dateTime.
    outputZonalStats.sort_values(['dateTime'])

    return (outputZonalStats)
    
    
def rainfallDataAmend(outputRainfall, i):

    # select the site to plot
    siteS = outputRainfall.loc[(outputRainfall.site == i)]
    
    siteLabel = str(i)
    
    propertyName = outputRainfall.prop_name.unique()
    prop = propertyName[0]
    
    siteDate = outputRainfall.site_date.unique()
    sDate = siteDate[0]
    
    # read in the rainfall stats and covert them to total mm
    siteSsort = siteS.sort_values(['Date'])
    date = pd.Series(siteSsort['Date']).apply(pd.to_datetime)
    rain = siteSsort['mean'] /10
    print('date: ', type(date))
    print('rain: ', type(rain))
    return (rain, date, siteLabel)


def b1(outputZonalStats, i):
    '''
    Caluclate rolling average for band 1
    '''
    # use all predicted bare frac cover values to produce the fitted line 
    lsat_bare = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
    date_b = lsat_bare.sort_values(['dateTime'])
    print('date_b: ', type(date_b))
    datefit = pd.Series(date_b['dateTime']).apply(pd.to_datetime)
    bare_mean = date_b['b1_mean']
    
    # currently set to caluclate the rolloing mean for five points 
    b_mean_fl = bare_mean.rolling(5,center=True).mean()

    # interporlate the missing values to enable it to be plotted 
    interp = b_mean_fl.interpolate(method ='linear', limit_direction ='both')
    print('interp:', type(interp))
    vals = interp.values

    return (vals)
    
    
def b2(outputZonalStats, i):
    '''
    Caluclate rolling average for band 2
    '''
    # use all predicted green frac cover values to produce the fitted line 
    lsat_pv = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
    date_pv = lsat_pv.sort_values(['dateTime'])
    datefit2 = pd.Series(date_pv['dateTime']).apply(pd.to_datetime)
    pv_mean = date_pv['b2_mean']
    
    # currently set to caluclate the rolloing mean for four points 
    pv_mean_fl = pv_mean.rolling(5,center=True).mean() # changed from 5

    # interporlate the missing values to enable it to be plotted 
    interp2 = pv_mean_fl.interpolate(method ='linear', limit_direction ='both')
    vals_pv = interp2.values
    
    return (vals_pv)


def b3(outputZonalStats, i):
    '''
    Caluclate rolling average for band 3
    '''
    # use all predicted NPV frac cover values to produce the fitted line 
    lsat_npv = outputZonalStats[(outputZonalStats['site'] == i)]  
    date_npv = lsat_npv.sort_values(['dateTime'])
    datefit3 = pd.Series(date_npv['dateTime']).apply(pd.to_datetime)
    npv_mean = date_npv['b3_mean']
    
    # currently set to caluclate the rolloing mean for four points 
    npv_mean_fl = npv_mean.rolling(5,center=True).mean() # changed from 5

    # interporlate the missing values to enable it to be plotted 
    interp3 = npv_mean_fl.interpolate(method ='linear', limit_direction ='both')
    vals_npv = interp3.values  
    
    return (vals_npv, lsat_npv)
    

def plotBareGround(lsat_npv, vals, date, rain, integrated, completeTile, siteLabel, startDate, finishDate):
    '''
    #Create and export the bare ground and rainfall plots.
    '''
    # get the site name for the plot title
    sName = str(lsat_npv.site.unique())
    siteName = sName.strip("['']")

    # set up the format for the plot 
    fig, ax = plt.subplots() 
    ax.set_ylim(0,100)

    # set up the x axis limits using pandas 
    ax.set_xlim(pd.Timestamp(startDate), pd.Timestamp(finishDate))
         
    barax = ax.twinx()
    barax.bar(date, rain, width= 20, color = ('#00539C'),  label='Rainfall')#, alpha=0.15

    # add bare ground data to the plot
    ax.plot(datefit, vals, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')

    # add av line representing previous visits to the site.
    #plt.axvline(x = sDate, color ='r') #, linestyle = '--', linewidth = 1)
    ##################################################################
    years = mdates.YearLocator(1)   # 2 plots up every second year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)# Tick every year on Jan 1st
    ##################################################################
    # add legend in the fixed position and use numpoints=1 to only show one point otherwise it will show two points which is annoying
    #ax.tick_params(axis='both', which='major', labelsize=20)
    ax.legend(loc=2,numpoints=1, prop={'size': 20})
    ax.set_title("Time Trace - site " + siteName , fontsize=25)
    ax.set_xlabel('Year',fontsize=25)
    ######################### Select a y axis label #############################
    ax.set_ylabel('Bare Ground (%)',fontsize=20)

    barax.set_ylabel('Monthly Rainfall mm)',fontsize=20)
    barax.tick_params(axis='both', which='major', labelsize=20)
    barax.legend(loc=1,numpoints=1, prop={'size': 20})

    fig.autofmt_xdate()

    # Add the current years inspection date.
    plt.axvline(x = pd.Timestamp(sDate), color ='dimgrey', linestyle = '--')

    # Add previous dates from the star transect shapefile.
    integratedSite = integrated.loc[integrated['siteTitle']==i]
    listDate = integratedSite.dateTime.unique().tolist()

    listLength = len(listDate)

    if listLength >= 1:
        
        for i in listDate:
            plt.axvline(x = pd.Timestamp(i), color ='dimgrey', linestyle = '--')

    # export plot
    fig.savefig(plotOutputs + '\\bareGroundPlot_' + str(completeTile) + '_' + siteLabel + '_' + str(startDate) + '_' + str(finishDate) + '_150.png', dpi=150, bbox_inches='tight') # bbox_inches removes the white space
    plt.close(fig)
        
    return ()

    
def plotAllBands(lsat_npvl, date, rain, vals, vals_pv, vals_npv, integrated, completeTile, siteLabel, startDate, finishDate):
    '''
    #Create and export the bare ground, pv, npv and rainfall plots.
    '''
    # get the site name for the plot title
    sName = str(lsat_npv.site.unique())
    siteName = sName.strip("['']")

    # set up the format for the plot 
    fig, ax = plt.subplots()

    ax.set_ylim(0,100)

    # set up the x axis limits using pandas 
    ax.set_xlim(pd.Timestamp(startDate), pd.Timestamp(finishDate))

    barax = ax.twinx()
    barax.bar(date, rain, width= 20, color = ('#00539C'),  label='Rainfall', alpha=0.15)#, alpha=0.15

    ###################################################################################

    # plot all three data fields (bare ground, npv and pv)
    ax.plot(datefit, vals, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')
    ax.plot(datefit2, vals_pv, linestyle='-', linewidth=2, color = 'green', label='PV')
    ax.plot(datefit3, vals_npv, linestyle='-', linewidth=2, color = '#1873E1', label='NPV')

    #plt.axvline(x = sDate, color ='r') #, linestyle = '--', linewidth = 1)

    ##################################################################
    years = mdates.YearLocator(1)   # 2 plots up every second year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)# Tick every year on Jan 1st
    ##################################################################
    # add legend in the fixed position and use numpoints=1 to only show one point otherwise it will show two points which is annoying
    #ax.tick_params(axis='both', which='major', labelsize=20)
    ax.legend(loc=2,numpoints=1, prop={'size': 20})
    ax.set_title("Time Trace - site " + siteName , fontsize=25)
    ax.set_xlabel('Year',fontsize=25)

    ######################### Select a y axis label #############################
    ax.set_ylabel('Bare Ground (%)',fontsize=20)
    ax.set_ylabel('Photosynthetic Vegetation (%)',fontsize=20)
    ax.set_ylabel('Non-photosynthetic Vegetation (%)',fontsize=20)
    ax.set_ylabel('Fractional Cover (%)',fontsize=20)

    barax.set_ylabel('Monthly Rainfall mm)',fontsize=20)
    barax.tick_params(axis='both', which='major', labelsize=20)
    barax.legend(loc=1,numpoints=1, prop={'size': 20})

    fig.autofmt_xdate()

    # inspection dates

    # Add the current years inspection date.

    plt.axvline(x = pd.Timestamp(sDate), color ='dimgrey', linestyle = '--')

    # Add previous dates from the star transect shapefile.
    integratedSite = integrated.loc[integrated['siteTitle']==i]
    listDate = integratedSite.dateTime.unique().tolist()
    #print('listDate: ', listDate)
    listLength = len(listDate)
    #print('listLength: ', listLength)

    if listLength >= 1:
        
        for i in listDate:
            plt.axvline(x = pd.Timestamp(i), color ='dimgrey', linestyle = '--')

    # export plot
    fig.savefig(plotOutputs + '\\all_bands_for_interpretation_' + str(completeTile) + '_' + siteLabel + '_' + str(startDate) + '_' + str(finishDate) + '_150.png', dpi=150, bbox_inches='tight') # bbox_inches removes the white space
    plt.close(fig)

    return ()
   


def mainRoutine(exportDirPath, outputZonalStats, outputRainfall, completeTile, rainFinishDate):

    print('bareGroundPlots.py INITIATED.')
    
    # define plot output path
    plotOutputs = exportDirPath + '\\plots'

    # define the start and finsh dates fro the plots
    startDate = '1988-05-01'
    finishDate = rainFinishDate
    
    # call previous visits function.
    integrated = previousVisits()
    
    # call importRainfallData function.
    outputRainfall = importRainfallData(outputRainfall)
    
    # call the importZonalStats function.
    outputZonalStats = importZonalStats(outputZonalStats)

    #def plotZonalRainfall():
     
    for i in outputRainfall.site.unique():
        
        rain, date, siteLabel = rainfallDataAmend(outputRainfall, i)
        
        # select the site to plot
        siteS = outputRainfall.loc[(outputRainfall.site == i)]
        
        siteLabel = str(i)
        
        propertyName = outputRainfall.prop_name.unique()
        prop = propertyName[0]
        
        siteDate = outputRainfall.site_date.unique()
        sDate = siteDate[0]
        
        # read in the rainfall stats and covert them to total mm
        siteSsort = siteS.sort_values(['Date'])
        date = pd.Series(siteSsort['Date']).apply(pd.to_datetime)
        rain = siteSsort['mean'] /10
        
        
        ###################################################################################
        #vals = b1(output_zonal_stats, i)
        
        # use all predicted bare frac cover values to produce the fitted line 
        lsat_bare = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
        date_b = lsat_bare.sort_values(['dateTime'])
        datefit = pd.Series(date_b['dateTime']).apply(pd.to_datetime)
        bare_mean = date_b['b1_mean']
        
        # currently set to caluclate the rolloing mean for four points 
        b_mean_fl = bare_mean.rolling(5,center=True).mean() # changed from 5


        # interporlate the missing values to enable it to be plotted 
        interp = b_mean_fl.interpolate(method ='linear', limit_direction ='both')
        vals = interp.values
        
        ###################################################################################
        #vals_pv = b2(output_zonal_stats, i)
        
        # use all predicted green frac cover values to produce the fitted line 
        lsat_pv = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
        date_pv = lsat_pv.sort_values(['dateTime'])
        datefit2 = pd.Series(date_pv['dateTime']).apply(pd.to_datetime)
        pv_mean = date_pv['b2_mean']
        
        # currently set to caluclate the rolloing mean for four points 
        pv_mean_fl = pv_mean.rolling(5,center=True).mean() # changed from 5

        # interporlate the missing values to enable it to be plotted 
        interp2 = pv_mean_fl.interpolate(method ='linear', limit_direction ='both')
        vals_pv = interp2.values
        
        ##################################################################################
        #vals_npv, lsat_npv = b3(output_zonal_stats, i)
        
        # use all predicted NPV frac cover values to produce the fitted line 
        lsat_npv = outputZonalStats[(outputZonalStats['site'] == i)]  
        date_npv = lsat_npv.sort_values(['dateTime'])
        datefit3 = pd.Series(date_npv['dateTime']).apply(pd.to_datetime)
        npv_mean = date_npv['b3_mean']
        
        # currently set to caluclate the rolloing mean for four points 
        npv_mean_fl = npv_mean.rolling(5,center=True).mean() # changed from 5

        # interporlate the missing values to enable it to be plotted 
        interp3 = npv_mean_fl.interpolate(method ='linear', limit_direction ='both')
        vals_npv = interp3.values
        
        
        ###################################################################################
        #                              BARE GROUND
        ###################################################################################
        
        #plotBareGround(lsat_npv, vals, date, rain, integrated, complete_tile, siteLabel, startDate, finishDate)
        
        
        # get the site name for the plot title
        sName = str(lsat_npv.site.unique())
        siteName = sName.strip("['']")
        
        # set up the format for the plot 
        fig, ax = plt.subplots()
       
        ax.set_ylim(0,100)

        # set up the x axis limits using pandas 
        ax.set_xlim(pd.Timestamp(startDate), pd.Timestamp(finishDate))
             
        barax = ax.twinx()
        barax.bar(date, rain, width= 20, color = ('#00539C'),  label='Rainfall')#, alpha=0.15

        ###################################################################################

        # add bare ground data to the plot
        ax.plot(datefit, vals, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')

        # add av line representing previous visits to the site.
        #plt.axvline(x = sDate, color ='r') #, linestyle = '--', linewidth = 1)
        
        
        ##################################################################
        years = mdates.YearLocator(1)   # 2 plots up every second year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)# Tick every year on Jan 1st


        ##################################################################


        # add legend in the fixed position and use numpoints=1 to only show one point otherwise it will show two points which is annoying
        #ax.tick_params(axis='both', which='major', labelsize=20)
        ax.legend(loc=2,numpoints=1, prop={'size': 20})
        ax.set_title("Time Trace - site " + siteName , fontsize=25)
        ax.set_xlabel('Year',fontsize=25)
        
        ######################### Select a y axis label #############################
        ax.set_ylabel('Bare Ground (%)',fontsize=20)


        barax.set_ylabel('Monthly Rainfall mm)',fontsize=20)
        barax.tick_params(axis='both', which='major', labelsize=20)
        barax.legend(loc=1,numpoints=1, prop={'size': 20})
        
        fig.autofmt_xdate()
        
     
        # Add the current years inspection date.
        
        plt.axvline(x = pd.Timestamp(sDate), color ='dimgrey', linestyle = '--')
        
        # Add previous dates from the star transect shapefile.
        integratedSite = integrated.loc[integrated['siteTitle']==i]
        listDate = integratedSite.dateTime.unique().tolist()

        listLength = len(listDate)

        
        if listLength >= 1:
            
            for i in listDate:
                plt.axvline(x = pd.Timestamp(i), color ='dimgrey', linestyle = '--')


        fig.savefig(plotOutputs + '\\bareGroundPlot_' + str(completeTile) + '_' + siteLabel + '_' + str(startDate) + '_' + str(finishDate) + '_150.png', dpi=150, bbox_inches='tight') # bbox_inches removes the white space

        plt.close(fig)
        
        
        ###################################################################################
        #                              ALL
        ###################################################################################
        
        #plotAllBands(lsat_npvl, date, rain, vals, vals_pv, vals_npv, integrated, complete_tile, siteLabel, startDate, finishDate)
        
        # get the site name for the plot title
        sName = str(lsat_npv.site.unique())
        siteName = sName.strip("['']")
        
        # set up the format for the plot 
        fig, ax = plt.subplots()
       
        ax.set_ylim(0,100)

        # set up the x axis limits using pandas 
        ax.set_xlim(pd.Timestamp(startDate), pd.Timestamp(finishDate))
        
        
        barax = ax.twinx()
        barax.bar(date, rain, width= 20, color = ('#00539C'),  label='Rainfall', alpha=0.15)#, alpha=0.15

        ###################################################################################

        # plot all three data fields (bare ground, npv and pv)
        ax.plot(datefit, vals, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')
        ax.plot(datefit2, vals_pv, linestyle='-', linewidth=2, color = 'green', label='PV')
        ax.plot(datefit3, vals_npv, linestyle='-', linewidth=2, color = '#1873E1', label='NPV')
        
        #plt.axvline(x = sDate, color ='r') #, linestyle = '--', linewidth = 1)
        
        
        ##################################################################
        years = mdates.YearLocator(1)   # 2 plots up every second year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)# Tick every year on Jan 1st


        ##################################################################


        # add legend in the fixed position and use numpoints=1 to only show one point otherwise it will show two points which is annoying
        #ax.tick_params(axis='both', which='major', labelsize=20)
        ax.legend(loc=2,numpoints=1, prop={'size': 20})
        ax.set_title("Time Trace - site " + siteName , fontsize=25)
        ax.set_xlabel('Year',fontsize=25)
        
        ######################### Select a y axis label #############################
        ax.set_ylabel('Bare Ground (%)',fontsize=20)
        ax.set_ylabel('Photosynthetic Vegetation (%)',fontsize=20)
        ax.set_ylabel('Non-photosynthetic Vegetation (%)',fontsize=20)
        ax.set_ylabel('Fractional Cover (%)',fontsize=20)
       
        barax.set_ylabel('Monthly Rainfall mm)',fontsize=20)
        barax.tick_params(axis='both', which='major', labelsize=20)
        barax.legend(loc=1,numpoints=1, prop={'size': 20})
        
        fig.autofmt_xdate()
        
        # Add the current inspection date.
        plt.axvline(x = pd.Timestamp(sDate), color ='dimgrey', linestyle = '--')
        
        # Add previous dates from the star transect shapefile.
        integratedSite = integrated.loc[integrated['siteTitle']==i]
        listDate = integratedSite.dateTime.unique().tolist()

        listLength = len(listDate)

        
        if listLength >= 1:
            
            for i in listDate:
                plt.axvline(x = pd.Timestamp(i), color ='dimgrey', linestyle = '--')


        fig.savefig(plotOutputs + '\\all_bands_for_interpretation_' + str(completeTile) + '_' + siteLabel + '_' + str(startDate) + '_' + str(finishDate) + '_150.png', dpi=150, bbox_inches='tight') # bbox_inches removes the white space

        plt.close(fig)
    
    print('interactivePlot.py initiating...........')
    
    import interactivePlotTest
    interactivePlotTest.mainRoutine(outputZonalStats, completeTile, plotOutputs)    
    
    return(outputZonalStats)


    print('bareGroundPlot.py COMPLETED')
    print('interactivePlot.py initiated...........')
    
  
    
if __name__ == "__main__":
    mainRoutine()   
