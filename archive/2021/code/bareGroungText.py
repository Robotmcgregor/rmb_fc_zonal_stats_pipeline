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

--dateFitBG: series
series object from the Series object with the sorted dist dateBG appended.

--meanBG: series
series object containing the bare ground mean value.

--meanBGfl: series
series object containing a rolling mean derived from the meanBG zzzz and the zzzz input.

--interpBG: Series
Series object conataining an interpolated linier value derived from the meanBGfl (limit_direction ='both').

--valsBG = interpBG.values

--lsatPV: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'.

--datePV: DataFrame
DataFrame object containing the sorted dateTime variables from the dateTime feature of the lsatPV DataFrame.

--dateFitPV: series
series object from the Series object with the sorted dist datePV appended

--meanPV: series
series object containing the photosynthetic vegetation mean value.

--meanPVfl: series
series object containing a rolling mean derived from the pv_mean zzzz and the zzzz input.

--interpPV: zzzz
zzzz object conataining an interpolated linier value derived from the meanPVfl (limit_direction ='both')

--valsPV = interpPV.values
    
--lsat_npv: DataFrame
DataFrame object that contins a subset of output_zonal_stats dataFrame by the feature 'site'.

--dateNPV: series
series object containing the sorted dateTime variables from the dateTime feature of the lsat_npv DataFrame.

--dateFitNPV: series
series object from the Series object with the sorted dist date_npv appended

--meanNPV: series
series containing the bare ground mean value.

--meanNPVfl: series
series object containing a rolling mean derived from the meanNPV zzzz and the zzzz input.

--interpNPV: zzzz
zzzz object conataining an interpolated linier value derived from the meanNPVfl (limit_direction ='both')

--valsNPV = interpNPV.values

--siteLabel: str

--startDate: str
string object containing the rainfall start date for the plots (i.e. 'YYYY-MM-01')

--finishDate: str
string object containing the rainfall finish date for the plots - derived by the step1_2_list_of_rainfall_images.py script (i.e. 'YYYY-MM-01')
    
--plotOutputs: str
string object contining the path to the plots folder within the export directory 'YYYYMMDD_HHMM'.




"""

