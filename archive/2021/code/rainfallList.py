#!/usr/bin/env python

from __future__ import print_function, division
import pdb
import fiona
import rasterio
import pandas as pd 
import argparse
from rasterstats import zonal_stats 
import glob
import geopandas as gpd
import os


'''
step1_3_collate_odk_apply_1ha_buffer.py
=============================================

Description: This script searches through a directory for all ODK output excel files. 
Once located, all odk outputs are concatenated, based on their type(i.e integrated / RAS) and outputed to the export_dir_path (odk_int_output.csv and odk_ras_output.csv) and (odk_int_output.shp and odk_ras_output.shp (geographics (GCS_GDA_1994.
Additonally, the attributes are removed excluding {'PROP_NAME', property name (i.e. Nuthill Downs : 'SITE_NAME', site name (i.e. NTH01A) : 'DATE', DATETIME (i.e. 14/07/2020 9:35:00 AM)}
for data configeration / consistancy and the integrated and RAS data is concatinated and output as a .shp (odk_all_output.shp)


The script also reprojects the odk_all_output.shp to WGS_1984_UTM_Zone_52S and WGS_1984_UTM_Zone_53S, and a 1ha square buffer is applied to each site.
Colminating in the output of two shapefiles compGeoDF_1ha_WHS84z52.shp and compGeoDF_1ha_WHS84z53.shp.
Note1: Each output does not de


all integrated and RAS outputs and exports a csv and a projected shapefiles (WGS52 and 53).
This script also applies a 1ha square buffer to each site and outputs a csv, projected shapefiles and a complete (cleaned) shapefile for executing XXXXXXXXXXXXXXX.



Author: Rob McGregor
email: Robert.Mcgregor@nt.gov.au
Date: 27/10/2020
Version: 1.0

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

1.	ODK output directory in .xlsx format
2.	Singlepart polygon shapefile or shapefiles with the following attributes “LAISKEY”, “PROP_NAME”, “WGS52_ha” and “WGS53_ha”. The shapefiles with correct attributes can be derived from: select_and_project_property_shapefiles_calc_area.py (McGregor, 2020).
3.	A final classification must been applied to the MODIS derived NAFI fire scars file names include (i.e. MTHS.tif or MTH.tif). However, if you wish to include the current year (not complete) you will need to pre-process that raster. Pre-processing can be derived from: modis_raster_12_month_classification.py (McGregor, 2020).

===================================================================================================

Command arguments:
------------------

None

======================================================================================================

IMPORTANT
---------

Because the NAFI fire scar by year raster do not have a standardised naming convention you may need to amend the following variables: 
“imgName”, “imgDate”, ‘cleanPropName” . Print functions have been commented out for you to make the necessary amendments.

======================================================================================================

Parameters:
-----------

tempDir: str


directoryODK: str


export_dir_path: str


tile_grid: str

rainfallImageList: list
List object containing all of the QLD rainfall imiage pathways.

dirName: str
directort path containing the QLD rainfall images.

endFileName: str
search criteria to discover the QLD rainfall images.

image_s: 

projected_shape_path: str
path to the reprojected 1ha polygons 'GCSWGS84' for zonal stats calculations.

uid: attribute name

image_s: str
variable containing an individual path for arainfall image as it loops through the xxxx list.

finalresults

'GCSWGS84'

========================================================================================================
'''



"""
Read in rainfall raster images and create a csv.


Author: Rob McGregor
Date: 24/11/2020
"""



def getCmdargs():

    p = argparse.ArgumentParser()

    p.add_argument("-i","--imglist", help="Input Landsat fractional cover PV band to derive zonal stats from")
        
    p.add_argument("-s","--shape", help="shape file contiaing the zones needs to have a field defined as id")
    
    p.add_argument("-u","--uid", help="input the column name for the unique id field in the shapefile") 
    
    p.add_argument("-o","--csv", help="name of the output csv file containing the results")
    
    cmdargs = p.parse_args()
    
    if cmdargs.imglist is None:

        p.print_help()

        sys.exit()

    return cmdargs
    
def listdir(dirName,endFileName):
    """
    this function will return a list of files in a directory for the given file extention. 
    """
    rainfallImageList = []
     
    for root, dirs, files in os.walk(dirName):
        for file in files:
            if file.endswith(endFileName):
                img = (os.path.join(root, file))
                rainfallImageList.append(img)
                #print (img)
    
    rainfallImageList.sort()
    print('rainfallImageList:', rainfallImageList)
    
    # using list indexing 
    # to get first and last element of list 
    resDates = [ rainfallImageList[0], rainfallImageList[-1] ] 
    print('resDates: ', resDates)    
    
    return (rainfallImageListNew, resDates)
    
    
'''

def apply_zonal_stats_fn(image_s, projected_shape_path, uid):
    
    
    """
    function to derive zonal stats for a list of Landsat imagery
    """    
    # create an empty lists to write the results 
            
    zonestats = []
    siteID = []
    image_Name = []
    nodata = -1 # the nodata value for the silo rainfall raster imagery
    
    #pdb.set_trace()
    
    with rasterio.open(image_s, nodata=nodata) as srci:
        #print ('image_s:', image_s)
        affine = srci.transform      #srci.affine
        array = srci.read(1) 

        with fiona.open(projected_shape_path) as src:
            #print('projected_shape_path: ' , projected_shape_path)
            
            zs = zonal_stats(src, array, affine=affine, nodata=nodata, stats=['count', 'min', 'max', 'mean','median', 'std','percentile_5.0', 'percentile_25.0','percentile_50.0','percentile_75.0', 'percentile_95.0'],all_touched=True) 
            # using "all_touched=True" will increase the number of pixels used to produce the stats "False" reduces the number 
            # extract the image name from the opened file from the input file read in by rasterio
            imgName1 = str(srci)[-21:]
            #print('imgName1: ' , imgName1)
            
            imgName = imgName1[0:10] # this expects to see a file name looking like this in lenght - l5tmre_p106r069_19930311_dilm_zstdmask.img l8olre_p106r069_p106r068_20190826_dc4m_zstdmask.img 
            #print ('imgName: ' , imgName)
            #print ("-------------------------")
            #print (imgName)
            imgDate = imgName[0:6]  
            #print ('imgDate: ', imgDate)
            #print ("::::::::::::::::::::::::::")
            #pdb.set_trace()

            for zone in zs:
                zone_stats = zone
                count = zone_stats["count"]
                mean = zone_stats["mean"]
                Min = zone_stats["min"]
                Max = zone_stats['max']
                med = zone_stats['median']
                std = zone_stats['std']
                perc5 = zone_stats['percentile_5.0']
                perc25 = zone_stats['percentile_25.0']
                perc50 = zone_stats['percentile_50.0']
                perc75 = zone_stats['percentile_75.0']
                perc95 = zone_stats['percentile_95.0']
            
                # put the individual results in a list and append them to the zonestats list
                result = [mean,std, med, Min, Max, count, perc5, perc25, perc50, perc75, perc95] #perc5,perc95
                zonestats.append(result)
                            
            # extract out the site number for the polygon
            for i in src:
                table_attributes = i['properties'] # reads in the attribute table for each record 
                        
                ident = table_attributes[uid] # reads in the id field from the attribute table and prints out the selected record 
                site = table_attributes['SITE_NAME']
                prop = table_attributes['PROP_NAME']   
                prop_code = table_attributes['PROP_CODE']
                site_date = table_attributes['SITE_DATE']
                details = [ident, site, prop, prop_code, site_date, imgDate]
                siteID.append(details)
                imageUsed = [imgName]
                
   
                image_Name.append(imageUsed)

        # join the elements in each of the lists row by row 
        finalresults =  [siteid + zoneR + imU for siteid, zoneR, imU in zip(siteID, zonestats,image_Name)]  
                          
        # close the vector and raster file 
        src.close() 
        srci.close() 

        # print out the file name of the processed image
        #print (imgName + ' ' + 'is' + ' ' + 'complete') 
                
        #pdb.set_trace()
    print('rainfall zonal stats are complete.')
    return(finalresults)
    '''       

def mainRoutine(exportDir, zonalStatsReadyDir, zonalStatsOutput, tile, file, concatenated_df, completeTile):

    dirName = r'Z:\Scratch\mcintyred\Rainfall'
    endFileName = r'.img'

    rainfallImageList = listdir(dirName,endFileName)
    '''
    #empty_df = pd.DataFrame()
    
    output_list = []
    
    # read in the command arguments
    #cmdargs = getCmdargs()
    #rainfallImageList = r'Z:\Scratch\mcintyred\Rainfall\silo_rainfall_img_1987_2020.csv' # need to get the script to create this list. 
    uid = 'uid'
    #exportDir = r'Z:\Scratch\Zonal_Stats_Pipeline\pipeline_test2'
    #zonal_stats_ready_dir = r'E:\DENR\rob\outputs1\tempFolder\tempTileGrid\zonalStatsReady'
    listDF = []
    
    gcs_wgs84_dir = (exportDir + '\\GCSWGS84')

    rainfall_output_dir = (exportDir + '\\rainfall')
    #os.mkdir(rainfall_output_dir)
    
    '''
    '''
    for odkShapefile in glob.glob(zonal_stats_ready_dir + '\\*_ODK_by_tile.shp'):
    #print('odkShapefile', odkShapefile)
    tile = str(odkShapefile[-22:-16])
    '''    
    '''
    # reproject each tile shapefile to GCSWGS84'
    #print('tile: ', tile)
    beginTile = tile[-29:-26]
    #print('beginTile: ', beginTile)
    endTile = tile[-25:-22]
    #print('endTile: ', endTile)
    tileName = str(beginTile) + str(endTile)
    #print(tileName)
    
    shapefilePath = zonal_stats_ready_dir + '\\' + tileName + '_ODK_by_tile.shp'
    #print('shapefilePath: ', shapefilePath)
    
    DF = gpd.read_file(shapefilePath)
    #print(DF)
    cgsDF = DF.to_crs(epsg=4326)
    #print(cgsDF.crs)
    crs_name = 'GCSWGS84'
    # Export re-projected shapefiles.
    projected_shape_path = gcs_wgs84_dir + '\\' + str(tileName) + '_' + str(crs_name) + '.shp'
    #print('projected_shape_path: ' , projected_shape_path)
    cgsDF.to_file(projected_shape_path)
    
    # Append a list with the paths for the newly projected shapefiles.
    #for shape in glob.glob(gcs_wgs84_dir + '\\*GCSWGS84.shp'):
    #print(shape)
    #listDF.append(cgsShapefile)
    #print(listDF)
    
    
    # open the list of imagery and read it into memory and call the apply_zonal_stats_fn function
    with open(rainfallImageListNew, 'r') as imagerylist:
                
        # loop throught the list of imagery and imput the image into the rasterstats zonal_stats function        
        for image in imagerylist:
            image_s = image.rstrip()
            #print('image_s: ', image_s)
            #pdb.set_trace()        
            finalresults = apply_zonal_stats_fn(image_s, projected_shape_path, uid)
                        
            for i in finalresults:
                
                output_list.append(i)
        

    # convert the list to a pandas dataframe with a headers
    headers = ['ident', 'site', 'prop_name', 'prop_code', 'site_date', 'imDate','mean','std', 'median', 'Min', 'Max', 'count','perc5','perc25','perc50','perc75','perc95','imName'] #'perc5','perc95',
    
    outputRainfall = pd.DataFrame.from_records(output_list,columns=headers)
    #print('outputRainfall: ', outputRainfall)
    
    # export the pandas df to a csv file
    outputRainfall.to_csv(rainfall_output_dir + '\\' + str(tileName) + 'rainfallZonalStats.csv', index=False)
    #print(tileName + ' zonal stats are complete.')

    print('monthly rainfall zonal stats script is complete.')
    
    import bareGroundPlot
    bareGroundPlot.main_routine(exportDir, zonalStatsOutput, rainfall_output_dir, tile, file, concatenated_df, outputRainfall, complete_tile, resDates)
    
    
if __name__ == "__main__":
    main_routine()   
