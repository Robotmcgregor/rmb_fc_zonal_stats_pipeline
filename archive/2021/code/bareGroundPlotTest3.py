#!/usr/bin/env python

# import modules.
from __future__ import print_function, division
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")
mpl.rcParams['figure.figsize'] = (30, 8.0)

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


===================================================================================================

variables:
-----------

--integrated: DataFrame
DataFrame object that srores the shapefile containing previous NT Star Transect information.

--siteS: DataFrame
DataFrame conating a suset of the outputRainfall DataFrame based on the unique identifier 'site'.

--siteLabel: str
string object containing the site name as a string.

--propertyName: list
List object containing a list of the unique outputRainfall DataFrame feature 'prop_name'.

--siteSsort: Series
Series object containing the sorted dates from the outputRainfall DataFrame.

--siteDate: list
list object conataining the unique outputRainfall feature 'siteDate'.

--siteDate: list
list object conataining the unique outputRainfall feature 'siteDate'.

--siteSsort: list
list object conataining the unique siteS feature 'date'.

--date: Series
Series object zzzz

--rain: Series
Series object to the rainafall mean as 'mm' fderived from the siteSsort zzzz feature 'mean'.

--lsatBG: DataFrame
Subset of the 

--lsatBG: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'. 

--dateBG: list/series
list object containing the sorted dateTime variables from the dateTime feature od fthe lsatBG DataFrame.

'''

def previousVisits(): 
    '''
    Read in and clean the integrated site shapefile for previous site visit information.
    '''
    # Import the integrated site shapefile for previous visit dates to the site.
    integrated = gpd.read_file(r"Z:\Scratch\Zonal_Stats_Pipeline\shapefiles\NT_StarTransect_20200713.shp")
    # convert site name to capital letters
    integrated['siteTitle'] = integrated.site.str.upper()
    integrated['dateTime'] = integrated.obs_time.apply(pd.to_datetime)
    integrated.to_csv(r'Z:\Scratch\Zonal_Stats_Pipeline\checkIntegrated.csv')
    
    return(integrated)
    

def importRainfallData(outputRainfall):    
    
    # create the date time field and sort the values
    outputRainfall['year'] = outputRainfall['imDate'].map(lambda x: str(x)[:4])
    outputRainfall['month'] = outputRainfall['imDate'].map(lambda x: str(x)[4:6])
    outputRainfall['Date'] = outputRainfall['year']  + '/' + outputRainfall['month'] + '/' + '15'
    outputRainfall.sort_values(['Date'])
    
    # convert site_date feature from object to datetime
    outputRainfall['site_date'] = pd.to_datetime(outputRainfall['site_date'])
    
    return(outputRainfall)
    
    
def importZonalStats(outputZonalStats):    

    outputZonalStats = outputZonalStats

    outputZonalStats['site_date'] = pd.to_datetime(outputZonalStats['site_date'])
    # remove all data points which do not have at least 3 valid pixels to produce the average bare ground for a site
    outputZonalStats = outputZonalStats.loc[(outputZonalStats['b1_count'] > 3)]
    # create the date time field and sort the values
    outputZonalStats['dateTime'] = outputZonalStats['year'].apply(str) +"/"+ outputZonalStats['month'].apply(str)+"/"+outputZonalStats['day'].apply(str)
    outputZonalStats['dateTime'] = outputZonalStats.dateTime.apply(pd.to_datetime)
    # sort values by dateTime.
    outputZonalStats.sort_values(['dateTime'])

    return(outputZonalStats)
    
    
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

    return (rain, date, siteLabel)
    

def b1(outputZonalStats, i):
    '''
    Caluclate rolling average for band 1
    '''
    # use all predicted bare frac cover values to produce the fitted line 
    lsatBG = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
    dateBG = lsatBG.sort_values(['dateTime'])
    print('dateBG: ', type(dateBG))
    dateFitBG = pd.Series(dateBG['dateTime']).apply(pd.to_datetime)

    meanBG = dateBG['b1_mean']

    # currently set to caluclate the rolloing mean for five points 
    meanBGfl = meanBG.rolling(5,center=True).mean()


    # interporlate the missing values to enable it to be plotted 
    interpBG = meanBGfl.interpolate(method ='linear', limit_direction ='both')

    valsBG = interpBG.values

    return (valsBG, dateFitBG)
    
    
def b2(outputZonalStats, i):
    '''
    Caluclate rolling average for band 2
    '''
    # use all predicted green frac cover values to produce the fitted line 
    lsatPV = outputZonalStats.loc[(outputZonalStats['site'] == i)]  
    datePV = lsatPV.sort_values(['dateTime'])
    dateFitPV = pd.Series(datePV['dateTime']).apply(pd.to_datetime)
    meanPV = datePV['b2_mean']
    
    # currently set to caluclate the rolloing mean for four points 
    meanPVfl = meanPV.rolling(5,center=True).mean() # changed from 5

    # interporlate the missing values to enable it to be plotted 
    interpPV = meanPVfl.interpolate(method ='linear', limit_direction ='both')
    valsPV = interpPV.values
    
    return (valsPV, dateFitPV)


def b3(outputZonalStats, i):
    '''
    Caluclate rolling average for band 3
    '''
    # use all predicted NPV frac cover values to produce the fitted line 
    lsat_npv = outputZonalStats[(outputZonalStats['site'] == i)]  
    date_npv = lsat_npv.sort_values(['dateTime'])
    dateFitNPV = pd.Series(date_npv['dateTime']).apply(pd.to_datetime)
    meanNPV = date_npv['b3_mean']
    
    # currently set to caluclate the rolloing mean for four points 
    meanNPVfl = meanNPV.rolling(5,center=True).mean() # changed from 5

    # interporlate the missing values to enable it to be plotted 
    interpNPV = meanNPVfl.interpolate(method ='linear', limit_direction ='both')
    valsNPV = interpNPV.values  
    
    return (valsNPV, lsat_npv, dateFitNPV)
    
    
def plotBareGround(lsat_npv, vals, date, rain, integrated, completeTile, siteLabel, startDate, finishDate, dateFitBG, sDate, i, plotOutputs):

    ###################################################################################
    #                              BARE GROUND PLOT
    ###################################################################################
    
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
    ax.plot(dateFitBG, vals, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')

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
           
    return(fig)    
    
def plotAllBands(lsat_npv, date, rain, valsBG, valsPV, valsNPV, integrated, completeTile, siteLabel, startDate, finishDate,  dateFitBG, dateFitPV, dateFitNPV, sDate, i, plotOutputs):
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
    ax.plot(dateFitBG, valsBG, linestyle='-', linewidth=2, color = '#E13B18', label='Bare ground')
    ax.plot(dateFitPV, valsPV, linestyle='-', linewidth=2, color = 'green', label='PV')
    ax.plot(dateFitNPV, valsNPV, linestyle='-', linewidth=2, color = '#1873E1', label='NPV')
    
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
    # ax.tick_params(axis='both', which='major', labelsize=20)
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
       
    return(fig)
    
    
   
def mainRoutine(exportDirPath, outputZonalStats, outputRainfall, completeTile, rainFinishDate):

    # export_dir_path, zonalStatsOutput, rainfallOutput
    
    print('bareGroundPlots.py INITIATED.')
    
    plotOutputs = exportDirPath + '\\plots'

    # define the start and finsh dates fro the plots
    startDate = '1988-05-01'
    finishDate = rainFinishDate
    
    # call previous visits function.
    integrated = previousVisits()
 
    outputRainfall = importRainfallData(outputRainfall)
    
    outputZonalStats = importZonalStats(outputZonalStats)

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
          
        valsBG, dateFitBG = b1(outputZonalStats, i)
        valsPV, dateFitPV = b2(outputZonalStats, i)
        valsNPV, lsat_npv, dateFitNPV = b3(outputZonalStats, i)
        
        fig = plotBareGround(lsat_npv, valsBG, date, rain, integrated, completeTile, siteLabel, startDate, finishDate, dateFitBG, sDate, i, plotOutputs)
        
        
        
        fig = plotAllBands(lsat_npv, date, rain, valsBG, valsPV, valsNPV, integrated, completeTile, siteLabel, startDate, finishDate,  dateFitBG, dateFitPV, dateFitNPV, sDate, i, plotOutputs)
        
        print('interactivePlot.py initiating...........')
    
    import interactivePlotTest # drop this out by one indent.
    interactivePlotTest.mainRoutine(outputZonalStats, completeTile, plotOutputs)  
        
    return(outputZonalStats)
    
    print('bareGroundPlot.py COMPLETED')

    
  
    
if __name__ == "__main__":
    mainRoutine()   
