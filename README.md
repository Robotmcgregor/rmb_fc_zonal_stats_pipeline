[Back to Remote Sensing Unit Wiki](https://github.com/Robotmcgregor/ntg_wiki/wiki)

# RMB Fractional Cover Zonal Statistics Pipeline


**Pipeline description**: This pipeline comprises 12 scripts which read in the star_transect csv produced by the 
RMB_obs_ras_sheet_pipeline. The pipeline creates a 1ha plot around each of the site point data, determines which 
Landsat tiles the point datasets overlay and produces fractional cover (fc) zonal statistics on each overlaying Landsat tile.
Additionally, this pipeline extracts monthly rainfall zonal statistics from SILO rainfall raster's.
Furthermore, this pipeline produces static and integrated time series plots per site, if site overlays multiple Landsat 
tiles, the tile with the most amount of non-null single date available data will be exported to the working drive.


**IMPORTANT**: This pipeline can be run on your local computer; however, regional teams (Katherine and Alice Springs) 
should utilise the remote desktop due to file transfer speeds (i.e. a priority should be given to regional teams).

Pipeline Description: Description: This pipeline comprises of 11 scripts which read in the AGB biomass csv. Pipeline 
converts data to  geo-dataframe and created a 1ha polygon (site) for each point. Once this is complete the pipeline 
runs zonal statistics on the current Landsat mosaic and exports a csv per site into an outputs directory. 

**Note:** Seasonal composites can be 6 band, 3 band, greyscale and classified.
Once pipeline is complete a temporary directory which was created will be deleted from the working drive, 
if script fails the temporary directory requires manual deletion.


| File Name | date range | Definition | Band Comp | Data Type | Current|
| :---:  | :---:  | :---: | :---: | :---: | :---: |
| dp0 |  single date | Fractional cover v3| 3 bands | Continuous | Current |
| dil |  single date | Fractional cover v2| 4 bands | Continuous | Archived |


## Outputs
- **Output 1**: FC zonal statistic csv for each site per Landsat tile that overlays each 1ha site.
- **Output 2**: Rainfall zonal statistic csv for each site.
- **Output 3**: GDA94 point shapefile.
- **Output 4**: WGSz52 1ha polygon shapefile.
- **Output 4**: WGSz53 1ha polygon shapefile.


## Parameters

input csv - point data in geographics GDA94 with the following features: 

| uid | site | date_time |
| :---:   | :---: | :---: |
| int (unique id) | str(site name)   | timestamp |

Landsat wrs2 directory:
located here: Z:\Landsat\wrs2
**Note**: script requires the current directory structure.

Command arguments:
------------------

 - **tile_grid**
    - String object containing the path to the Landsat tile grid shapefile.
    Default location: E:\DEPWS\code\rangeland_monitoring\rmb_fractional_cover_zonal_stats_pipeline_tif\assets\shapefiles\Landsat_wrs2_TileGrid.shp


 - **directory_odk**:
    - String object containing the directory path to the property level star transect csv produced from the 
      RMB Obs Ras Sheet Pipeline.

    Refer to previous section for csv feature requirements.


 - **export_dir**:
    - String object containing the path to a directory where the pipeline will create a directory tree containing all 
      finalised outputs.
    **NOTE1**: the script will search for a duplicate folder and delete it if found.
    **NOTE2**: the folder created is titled (YYYYMMDD_TIME) to avoid the accidental deletion of data due to poor naming
conventions.
      

 - **image_count**:
    -   Integer object that contains the minimum number of Landsat images (per tile) required for the fractional cover
zonal stats.
        Default value: 900.

 - **landsat_dir**:
    - String object containing the path to the Landsat wrs2 directory.
      Default path: Z:\Landsat\wrs2.
   **Note**: Deviation from this structure fill cause the pipeline to fail.
      

 - **no_data**:
    - Integer object containing the Landsat FC no data value.
    Default value: 0.


 - **rainfall_dir**
    - String object containing the pathway to the rainfall image directory.
    Default value: Z:\Landsat\rainfall.


 - **search_criteria1**:
    - String object containing the end part of the filename search criteria for the FC Landsat images.
    Default string: dilm2_zstdmask.img


 - **search_criteria2**:
    - String object containing the end part of the filename search criteria for the FC Landsat images.
    Default string: dilm3_zstdmask.img


 - **search_criteria3**:
    - String object containing the end part of the filename search criteria for the FC Landsat images.
    Default string: .img


 - **search_criteria4**:
    - String object containing the end part of the filename search criteria for the FC Landsat images.
    Default string: dilm4_zstdmask.img
