#!/usr/bin/env python

"""

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


===================================================================================================

Command arguments:
------------------

None


======================================================================================================

Input requirements (used in script):
------------------------------------

--output_zonal_stats: DataFrame
open DataFrame containing the fractonal cover zonal stats derived from step1_6_fc_zonal_stats.py.
    - this DataFrame will be subset based on: 
            - b1, b2 and b3 count feature greater than 3, and
            - year feature greater than 1987.
    
--complete_tile: str
string object contining the Landsat tile name created by step1_6_fc_zonal_stats.py

--rain_finish_date: str
string object containing the year month and day of the last image available (YYYY + '-' + MM + '-30').

--plotOutputs: str
string object contining the path to the plots folder within the export directory 'YYYYMMDD_HHMM'.

output_zonal_stats: DataFrame
DataFrame object zzzz

propName: str
string object to house the property name for each plot, derived from the pastoral estate shapefile. zzzz

siteDF: DataFrame
DataFrame object - subset of DataFrame 'output_zonal_stats', based on unique identifier 'site'.

dateSortDF: DataFrame
DataFrame object siteDF that has been sorted in assending order by the dateTime feature.

# use all predicted frac cover values to produce the fitted line
sortSiteDF: DataFrame
DataFrame object - subset of the sorted DataFrame 'dateSortDF', based on unique identifier 'site'.

variables:
-----------

--interactiveOutputs: str
string object containing the path to the interactive folder within the plotOutputs folder.

--unique_site: list
list object containing the unique identifier 'SITE' from the output_zonal_stats DataFrame.

--propName: str
string object containing the property name derived from the pastoral estate shapefile.

--siteID: str
string object containing the variable 'i' derived from zzzz

--i: zzzz
zzzz
 
siteDF: GeoDataFrame
geoDataFrame object - a subset of the output_zonal_stats geoDataFrmae based on the uniqe identifier 'site'.

--dateSortDF: DataFrame
DataFrame object sorted in assending order based on the dateTime feature - For the hover tool.

--sortSiteDF: geoDataFrame
geoDataFrame - subset of the a subset of the output_zonal_stats geoDataFrmae based on the uniqe identifier 'site'.

--dateF: DataFrame
DataFrame object in assending order base on the feature dateTime.
              
--dateFit: series
series object contining the dateTime feature from the datef DataFrame.
        
--meanBGfit: series
series object contining the b1_mean feature from the datef DataFrame.

--meanBGrolling: series
series object containing the rolling mean of the feature datef from the bg_mean_f series - perameters:(3,center=True)

s1, s2, s3: plots       

"""





from __future__ import print_function, division
import pandas as pd
import numpy as np
import bokeh.plotting as bp
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook, output_file
from bokeh.models import ColumnDataSource, LabelSet, HoverTool
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.plotting import figure
import warnings
warnings.filterwarnings("ignore")


         
def mainRoutine(outputZonalStats, completeTile, plotOutputs):

    print('interactivePlot.py INITIATED.')
    interactiveOutputs = plotOutputs + '\\interactive'

    # create a unique list of site names from the output_zonal_stats DataFrame
    unique_site = outputZonalStats.site.unique().tolist()
    #print(unique_site)
    
    '''
    Pull in pastoral estate shapefile for prop name zzzz.
    '''
    propName = 'Unknown property'
    
    # read in the new csv file and create an index using the date_time column
    
    # subset DataFrame - drop all values less than 3 to reduce noise
    outputZonalStats = outputZonalStats[(outputZonalStats['b1_count'] > 3)]

    # subset DataFrame - drop all values less than 1987
    outputZonalStats = outputZonalStats.loc[(outputZonalStats['year'] >= 1987)]

    for i in outputZonalStats.site.unique():
        # convert all site names variables to a string.
        siteID = str(i)
        # select out only the landsat derived frac cover values.
        '''
        Can I delete the one of the subset and sorts? zzzz
        '''
        # subset DataFrame by the unique identifier 'site'.  
        siteDF = outputZonalStats.loc[(outputZonalStats.site == i)]  # comment
        
        # sort DF by dateTime.
        dateSortDF = siteDF.sort_values(['dateTime'])  # comment
        print('dateSortDF: ', type(dateSortDF))
        # format the image date for the hovertool
        dateSortDF['DateTime'] = dateSortDF['dateTime'].dt.strftime('%d/%m/%Y')
        
        """-------------------------------------------------------Bare ground - band 1 --------------------------------------"""
        
        # use all predicted frac cover values to produce the fitted line
        sortSiteDF = outputZonalStats.loc[(outputZonalStats.site == i)]
        dateF = sortSiteDF.sort_values(['dateTime'])
        print('dateF: ', type(dateF))
        dateFit = dateF['dateTime']
        print('dateFit: ', type(dateFit))
        meanBGfit = dateF['b1_mean']
        print('meanBGfit: ', type(meanBGfit))
        meanBGrolling = meanBGfit.rolling(3,center=True).mean()
        print('meanBGrolling: ', type(meanBGrolling))
        # set up the hovertool
        source2 = ColumnDataSource(dateSortDF)
        print('source2: ', type(source2))        
        TOOLS="pan,wheel_zoom,box_zoom,reset,save,".split(',')     
        hover = HoverTool(tooltips=[( 'image date','@DateTime'),( 'Bare fraction', '@b1_mean{int}%')],names=["lsat"])       
        TOOLS.append(hover)
        
        # set up the plots parameters
        s1 = figure(title='Fractional Cover Time Trace - Bare ground: ' + propName + ' site (%s)'% (siteID), x_axis_label= 'time', 
                    y_axis_label= 'Bare Ground fraction %', x_axis_type='datetime',y_range = (0,105), 
                    plot_width=900, plot_height=250, tools=TOOLS)
        # plot the time series data
        s1.line(dateFit, meanBGrolling, color='red', line_width=3)
        s1.circle("dateTime", "b1_mean", source=source2,name="lsat", size=5,color='red',alpha=0.6, line_alpha=0.6,line_color='black')
        print('s1:', type(s1))
     
        """------------------------------------------------------- Photosynthetic vegetation band 2 ---------------------------------------"""
        
        outputZonalStats = outputZonalStats.loc[(outputZonalStats['b2_count'] > 3)]
        outputZonalStats.sort_values(['dateTime'])
        outputZonalStats = outputZonalStats.loc[(outputZonalStats['year'] >= 1987)]
        #print('output_zonal_stats line 157: ', output_zonal_stats)

        pv_mean_f = dateF['b2_mean']
        pv_mean_fpd4 = pv_mean_f.rolling(3,center=True).mean()
        
        # set up the hovertool
        source2 = ColumnDataSource(dateSortDF)
               
        TOOLS="pan,wheel_zoom,box_zoom,reset,save,".split(',')
        
        hover = HoverTool(tooltips=[( 'image date','@DateTime'),( 'pv fraction', '@b2_mean{int}%')],names=["lsat"])
        
        TOOLS.append(hover)
        
        # set up the plots parameters
        s2 = figure(title='Fractional Cover Time Trace - Photosynthetic vegetation: ' + propName + ' site (%s)'% (siteID), x_axis_label= 'time', 
                    y_axis_label= 'PV fraction %', x_axis_type='datetime',y_range = (0,105), 
                    plot_width=900, plot_height=250, tools=TOOLS)
        # plot the time series data
        s2.line(dateFit, pv_mean_fpd4, color='green', line_width=3)
        s2.circle("dateTime", "b2_mean", source=source2,name="lsat", size=5,color='green',alpha=0.6, line_alpha=0.6,line_color='black')#TODO b3 has been changed to b2

        """------------------------------------------------------- Non - photosynthetic vegetation band 3 ---------------------------------------"""
        
        outputZonalStats = outputZonalStats[(outputZonalStats['b3_count'] > 3)]
        outputZonalStats.sort_values(['dateTime'])
        outputZonalStats = outputZonalStats[(outputZonalStats['year'] >= 1987)]


        npv_mean_f = dateF['b3_mean']
        npv_mean_fpd4 = npv_mean_f.rolling(3,center=True).mean()
        
        # set up the hovertool
        source2 = ColumnDataSource(dateSortDF)
               
        TOOLS="pan,wheel_zoom,box_zoom,reset,save,".split(',')
        
        hover = HoverTool(tooltips=[( 'image date','@DateTime'),( 'npv fraction', '@b3_mean{int}%')],names=["lsat"])
        
        TOOLS.append(hover)
        
        # set up the plots parameters
        s3 = figure(title='Fractional Cover Time Trace - Non-photosynthetic vegetation: ' + propName + ' site (%s)'% (siteID), x_axis_label= 'time', 
                    y_axis_label= 'NPV fraction %', x_axis_type='datetime',y_range = (0,105), 
                    plot_width=900, plot_height=250, tools=TOOLS)
        # plot the time series data
        s3.line(dateFit, npv_mean_fpd4, color='blue', line_width=3)
        s3.circle("dateTime", "b3_mean", source=source2,name="lsat", size=5,color='blue',alpha=0.6, line_alpha=0.6,line_color='black')
        
        #complete_tile = str(106071)
        output_file(interactiveOutputs + '\\' + str(siteID) + '_' + completeTile + '_layout.html')

        save(column(s1, s2, s3))
    

    print('interactive plots script is complete.')
        
  
if __name__ == "__main__":
    mainRoutine()   
