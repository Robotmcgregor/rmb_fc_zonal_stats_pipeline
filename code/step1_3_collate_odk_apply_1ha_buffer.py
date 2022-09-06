#!/usr/bin/env python

'''
step1_3_collate_odk_apply_1ha_buffer.py
=============================================

Description: This script searches through a directory for all ODK output csv files.
Once located, all odk outputs are concatenated, based on their type(i.e integrated / RAS) and outputted to the
export_dir_path (odk_int_output.csv and odk_ras_output.csv) and (odk_int_output.shp and odk_ras_output.shp
(geographic (GCS_GDA_1994)).
Additionally, the attributes are removed excluding {'PROP_NAME', property name
(i.e. Nuthill Downs : 'SITE_NAME', site name (i.e. NTH01A) : 'DATE', DATETIME (i.e. 14/07/2020 9:35:00 AM)}
for data configuration / consistency and the integrated and RAS data is concatenated and output as a .shp
(odk_all_output.shp)

The script also re-projects the odk_all_output.shp to WGS_1984_UTM_Zone_52S and WGS_1984_UTM_Zone_53S, and a 1ha square
buffer is applied to each site, culminating in the output of two shapefiles compGeoDF_1ha_WHS84z52.shp and
compGeoDF_1ha_WHS84z53.shp.

All integrated and RAS outputs and exports a csv and a projected shapefiles (WGS52 and 53).
This script also applies a 1ha square buffer to each site and outputs a csv, projected shapefiles and a complete
(cleaned) shapefile for executing step1_4_landsat_tile_grid_identify.py.

Note: Ras assessment have been turned off.

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


========================================================================================================
'''

# Import modules
from __future__ import print_function, division
import os
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import pandas as pd
import glob
import sys

import warnings

warnings.filterwarnings("ignore")


def os_walk_odk_fn(directory_odk):
    """ Walks through the ODK output directory and appends file paths to one of two lists.

    @param directory_odk: string object containing the path to the property odk paths (--directory_odk).
    @return list_ras: list object containing all located ras output file paths.
    @return list_integrated: list object containing all located integrated star transect output file paths.
    """

    list_ras = []
    list_integrated = []

    for root, dirs, files in os.walk(directory_odk):

        for file in files:

            if file.endswith('star_transect.csv'):
                # Separate integrated/Tier 1 outputs
                odk = (os.path.join(root, file))
                list_integrated.append(odk)
                # todo uncomment out if time trace on ras site would be useful
                """elif file.endswith('ras.csv'):
                    # Separate RAS outputs
                    ras = (os.path.join(root, file))
                    list_ras.append(ras)"""
            else:
                pass

    print('The following ODK forms were identified for processing:')
    # todo uncomment out if time trace on ras site would be useful
    # print(' - RAS: ', len(list_ras))
    print(' - Integrated: ', len(list_integrated))

    return list_ras, list_integrated


def concatenate_df_list(list_input):
    """ Concatenate ODK csv outputs into a Pandas DataFrame.

    @param list_input: list object containing all located integrated star transect OR RAS output file paths.
    @return output_df: Pandas dataframe containing the concatenated csv files from the input list.
    """

    list_df = []
    # list_length = len(list_input)

    for i in list_input:

        df = pd.read_csv(i)
        if len(df.columns) == 234:
            df1 = df
        else:
            df1 = df.iloc[:, 1:]

        list_df.append(df1)
    # Concatenate list of DataFrames into a single DataFrame.
    output_df = pd.concat(list_df)

    return output_df


def single_csv_fn(list_input):
    """ Create a Pandas DataFrame from a list with only one list element (csv path).

    @param list_input: list object containing all located integrated star transect OR RAS output file paths.
    @return df: Pandas dataframe containing the concatenated csv files from the input list
    """
    for i in list_input:
        df = pd.read_csv(i)
        if len(df.columns) == 234:
            df1 = df
        else:
            df1 = df.iloc[:, 1:]

    return df1


def projection_file_name_fn(epsg, clean_odk_geo_df):
    """ Project a geo-dataframe with the input epsg param and return several crs specific string and integer outputs.

    @param epsg: integer object containing required crs for the current geo-dataframe.
    @param clean_odk_geo_df: geo-dataframe object which is to be re-projected.
    @return crs_name: string object containing the output crs in a standardised file naming convention.
    @return crs_output: dictionary object containing crs information used for older versions of GDAL.
    @return projected_df: geo-dataframe object projected to the input crs.
    """
    epsg_int = int(epsg)
    if epsg_int == 28352:
        crs_name = 'GDA94z52'
        crs_output = {'init': 'EPSG:28352'}
    elif epsg_int == 28353:
        crs_name = 'GDA94z53'
        crs_output = {'init': 'EPSG:28353'}
    elif epsg_int == 4283:
        crs_name = 'GDA94'
        crs_output = {'init': 'EPSG:4283'}
    elif epsg_int == 32752:
        crs_name = 'WGS84z52'
        crs_output = {'init': 'EPSG:32752'}
    elif epsg_int == 32753:
        crs_name = 'WGS84z53'
        crs_output = {'init': 'EPSG:32753'}
    elif epsg_int == 3577:
        crs_name = 'Albers'
        crs_output = {'init': 'EPSG:3577'}
    elif epsg_int == 4326:
        crs_name = 'GCS_WGS84'
        crs_output = {'init': 'EPSG:4326'}
    else:
        crs_name = 'not_defined'
        new_dict = {'init': 'EPSG:' + str(epsg_int)}
        crs_output = new_dict

    # Project DF to epsg value
    projected_df = clean_odk_geo_df.to_crs(epsg)

    return crs_name, crs_output, projected_df


def square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name):
    """ Separate each point, apply a 1ha square buffer and export shapefiles.

    @param projected_df: Pandas dataframe in the relevant projection (WGSz52 or WGSz53).
    @param prime_temp_buffer_dir: directory to the temporary sub-directory (temp_1ha_buffer).
    @param crs_name: string object containing the crs name for file naming.
    @return buffer_temp_dir: string object containing the path to the final output subdirectory titled after the crs name.
    """

    buffer_temp_dir = prime_temp_buffer_dir + '\\sites_1ha\\' + crs_name
    if not os.path.exists(buffer_temp_dir):
        os.makedirs(buffer_temp_dir)
    else:
        pass

    print(projected_df)
    for i in projected_df.site_name.unique():
        projected_df2 = projected_df.loc[projected_df.site_name == i]
        property_name = projected_df2.prop_name.unique()
        prop = property_name[0]
        prop1 = prop.title()

        if prop1 == 'La Belle Downs':
            prop2 = 'Labelle.Downs'
        else:
            prop2 = prop1.replace(' ', '.')

        date = projected_df2.date.unique()
        date1 = date[0]
        date2 = date1.split(' ')
        date3 = date2[0]
        date4 = date3.replace('/', '.')
        projected_df3 = projected_df2.buffer(50, cap_style=3)

        projected_df3.to_file(
            buffer_temp_dir + '\\' + prop2 + '_' + str(i) + '_' + str(date4) + '_1ha' + crs_name + '.shp')

    return buffer_temp_dir


def add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name, pastoral_estate):
    """ Retrieve file path for each 1ha shapefiles and add SITE_NAME and PROP_CODE attributes.

    @param prime_temp_buffer_dir: string object containing the path to a sub-directory within the temporary directory.
    @param buffer_temp_dir: string object containing the path to the sub-directory containing the 1ha site shapefiles.
    @param crs_name: string object containing the crs name for file naming.
    @param pastoral_estate: string object containing the path to the NT Pastoral Estate shapefile (command argument).
    @return prime_temp_buffer_dir: string object containing the path to a sub-directory within the temporary directory.
    """

    # Create a string path to a sub-directory
    attribute_temp_dir = prime_temp_buffer_dir + '\\1ha_attribute\\' + crs_name

    # Check if the sub-directory already exists and create if if does not.
    if not os.path.exists(attribute_temp_dir):
        os.makedirs(attribute_temp_dir)

    # search for shapefiles that meet the search criteria
    for root, dirs, files in os.walk(buffer_temp_dir):
        for file in files:
            ends_with = '_1ha' + str(crs_name) + '.shp'
            if file.endswith(ends_with):
                # split file name
                list_file_variables = file.split('_')
                property_dirty = list_file_variables[0]
                property_clean = property_dirty.title().replace('.', '_')

                # open pastoral estate and create a series only including the property name and property tag
                geo_df = gpd.read_file(pastoral_estate)
                geo_series = geo_df[['PROPERTY', 'PROP_TAG']]

                # call the prop_code_extraction_fn function to extract the property tag from the Pastoral Estate
                # shapefile using the property name.
                prop_code = prop_code_extraction_fn(property_clean, geo_series)
                # create two variables from the shapefile name
                site = list_file_variables[1]
                date = list_file_variables[2]

                # join the root and file name to create a complete path to the current shapefile to open and a
                # geo-dataframe.
                shp = os.path.join(root, file)
                geo_df = gpd.read_file(os.path.abspath(shp))

                # add required attributes to the geo-dataframe from previously defined variables.
                geo_df['site_name'] = str(site)
                geo_df['prop_name'] = property_clean
                geo_df['prop_code'] = str(prop_code)
                geo_df['site_date'] = str(date)

                # export finalised geo-dataframe as a shapefile.
                geo_df.to_file(
                    attribute_temp_dir + '\\' + property_clean + '_' + str(site) + '_1ha_attrib_' + crs_name + '.shp')

    return prime_temp_buffer_dir


def concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name):
    """  Concatenate attributed shapefiles and export completed shapefile.

    @param prime_temp_buffer_dir: string object containing the path to a sub-directory within the temporary directory.
    @param export_dir_path: string object containing the path to the export directory.
    @param crs_name: string object containing the standardised crs information to be used as part of the file/sub-dir.
    @return comp_geo_df: geo-dataframe created by the concatenation of all shapefiles located in the specified directory.
    @return crs_name: string object containing the standardised crs information to be used as part of the file/sub-dir.
    """

    list_df2 = []
    search_term = '*.shp'

    for file in glob.glob(prime_temp_buffer_dir + '\\1ha_attribute\\' + crs_name + '\\' + search_term):
        geo_df = gpd.read_file(file)
        list_df2.append(geo_df)

    if len(list_df2) >= 1:

        comp_geo_df = gpd.GeoDataFrame(pd.concat(list_df2, ignore_index=True), crs=list_df2[0].crs)
        comp_geo_df.to_file(export_dir_path + '\\comp_geo_df_1ha_' + crs_name + '.shp')

    else:

        print('There are no shapefiles to concatenate: ', crs_name)
        sys.exit(1)
        print('There are no shapefiles to concatenate: ', crs_name)
        comp_geo_df = None

    return comp_geo_df, crs_name


def prop_code_extraction_fn(prop, pastoral_estate):
    """ Extract the property tag from the Pastoral Estate shapefile using the property name.

    @param prop: string object containing the current property name.
    @param pastoral_estate: geo-dataframe object created from the Pastoral Estate shapefile
    @return prop_code: string object extracted from the Pastoral Estate based on the property name.
    """
    property_list = pastoral_estate.PROPERTY.tolist()

    prop_upper = prop.upper().replace('_', ' ')
    if prop_upper in property_list:

        prop_code = pastoral_estate.loc[pastoral_estate['PROPERTY'] == prop_upper, 'PROP_TAG'].iloc[0]
    else:
        prop_code = ''

    return prop_code


def main_routine(directory_odk, export_dir_path, prime_temp_buffer_dir, pastoral_estate):
    # ------------------------------------------- ODK csv collation --------------------------------------------------

    # Call the os_walk_odk_fn function to append all csv files with the required search criteria into one of two lists
    # list_integrated or list_ras depending on the type of site.
    list_ras, list_integrated = os_walk_odk_fn(directory_odk)

    list_input = list_integrated

    if len(list_input) >= 2:

        # Call the concatenate_df_list_fn function - input = list_input - output = integrated_df.

        int_df = concatenate_df_list(list_input)

        # rename two column headers so that both the integrated_df and ras_df columns are the same: PROP_NAME and
        # SITE_NAME
        int_df.rename(columns={'final_prop': 'prop_name', 'site_orig': 'site_name'}, inplace=True)

        integrated_df = int_df
        int_df.to_csv(export_dir_path + '//odk_int_output.csv')

        # ------------------------------------------- Convert to geo-DataFrame -----------------------------------------

        # Create a geometry column to convert the DF into a geo_df.
        geometry = [Point(xy) for xy in zip(integrated_df.wgs_c_lon, integrated_df.wgs_c_lat)]
        integrated_df2 = integrated_df.drop(['gda_c_lon', 'gda_c_lat'], axis=1)
        integrated_df2.date = integrated_df2.date.astype(str)
        clean_odk_geo_df = GeoDataFrame(integrated_df2, crs='EPSG:4283', geometry=geometry)

        # Export shapefile.
        clean_odk_geo_df.to_file(export_dir_path + '//odk_int_output.shp', driver='ESRI Shapefile')

        # ----------------------------------------------- EPSG: 32752 --------------------------------------------------
        # set epsg to WGSz52.
        epsg = 32752

        # Project clean_odk_geo_df to WGSz52.
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # ------------------------------------------------ EPSG: 32753 -------------------------------------------------

        # set epsg to WGSz52
        epsg = 32753

        # Project clean_odk_geo_df to WGSz53
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

    elif len(list_input) == 1:

        int_df = single_csv_fn(list_input)

        print(list(int_df.columns))
        # rename two column headers so that both the integrated_df and ras_df columns are the
        # same: PROP_NAME and SITE_NAME.

        int_df.rename(columns={'final_prop': 'prop_name', 'site_orig': 'site_name'}, inplace=True)

        integrated_df = int_df
        integrated_df.to_csv(export_dir_path + '//odk_int_output.csv')
        # -------------------------------------- Convert to geo-DataFrame ----------------------------------------------

        # Create a geometry column to convert the DF into a geo_df.
        geometry = [Point(xy) for xy in zip(integrated_df.wgs_c_lon, integrated_df.wgs_c_lat)]
        integrated_df2 = integrated_df.drop(['wgs_c_lon', 'wgs_c_lat'], axis=1)
        # print('integrated_df2: ', integrated_df2)
        # integrated_df2.info()
        integrated_df2.date = integrated_df2.date.astype(str)
        clean_odk_geo_df = GeoDataFrame(integrated_df2, crs='EPSG:4326', geometry=geometry)

        # Export shapefile.    
        clean_odk_geo_df.to_file(export_dir_path + '//odk_int_output_wgs84.shp', driver='ESRI Shapefile')

        # ---------------------------------------------- EPSG: 32752 ---------------------------------------------------
        # set epsg to WGSz52.
        epsg = 32752

        # Project clean_odk_geo_df to WGSz52.
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # ------------------------------------------------ EPSG: 32753 -------------------------------------------------

        # set epsg to WGSz52
        epsg = 32753

        # Project clean_odk_geo_df to WGSz53
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

    else:

        print('There are no integrated  sites to be processed.')

    # ------------------------------------------------------- RAS ------------------------------------------------------

    list_input = list_ras

    if len(list_input) >= 2:

        # run concatenate_df_list_fn function - input = list_input - output = integrated_df.

        ras_df = concatenate_df_list(list_input)
        # rename two column headers so that both the integrated_df and ras_df columns are the
        # same: PROP_NAME and SITE_NAME

        ras_df.rename(columns={'final_prop': 'prop_name', 'site_orig': 'site_name'}, inplace=True)
        # Drop rows which contain the string 'BLANK' instead of a Lon Lat value.

        ras_df_ = ras_df
        ras_df2 = ras_df_[ras_df_.loc_c != 'BLANK']

        # Export csv
        ras_df2.to_csv(export_dir_path + '//odk_ras_output.csv')

        # --------------------------------------- Convert to geo-DataFrame ---------------------------------------------

        # Create a geometry column to convert the DF into a geo_df
        geometry = [Point(xy) for xy in zip(ras_df2.wgs_c_lon, ras_df2.wgs_c_lat)]
        ras_df3 = ras_df2.drop(['wgs_c_lon', 'wgs_c_lat'], axis=1)
        ras_df3.date = ras_df3.date.astype(str)
        clean_odk_geo_df = GeoDataFrame(ras_df3, crs='EPSG:4326', geometry=geometry)

        # Export shapefile
        clean_odk_geo_df.to_file(export_dir_path + '//odk_ras_output_wgs84.shp', driver='ESRI Shapefile')

        # ---------------------------------------------- EPSG: 32752 ---------------------------------------------------
        # set epsg to WGSz52.
        epsg = 32752

        # Project clean_odk_geo_df to WGSz52.
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # Concatenate, clean and export geo_df_52
        geo_df_52, crs_name_52 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

        # ---------------------------------------------- EPSG: 32753 ---------------------------------------------------

        # set epsg to WGSz52
        epsg = 32753

        # Project clean_odk_geo_df to WGSz53
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # Concatenate, clean and export geo_df_53
        geo_df_53, crs_name_53 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

    elif len(list_input) == 1:

        ras_df = single_csv_fn(list_input)
        # rename two column headers so that both the integrated_df and ras_df columns are the
        # same: PROP_NAME and SITE_NAME
        ras_df.rename(columns={'final_prop': 'prop_name', 'site_orig': 'site_name'}, inplace=True)
        # Drop rows which contain the string 'BLANK' instead of a Lon Lat value.

        ras_df_ = ras_df
        ras_df2 = ras_df[ras_df.wgs_c_lon != 'BLANK']
        # Export csv
        ras_df2.to_csv(export_dir_path + '//odk_ras_output.csv')

        # --------------------------------------- Convert to geo-DataFrame ---------------------------------------------

        # Create a geometry column to convert the DF into a geo_df
        geometry = [Point(xy) for xy in zip(ras_df2.wgs_c_lon, ras_df2.wgs_c_lat)]
        ras_df3 = ras_df2.drop(['wgs_c_lon', 'wgs_c_lat'], axis=1)
        ras_df3.date = ras_df3.date.astype(str)
        clean_odk_geo_df = GeoDataFrame(ras_df3, crs='EPSG:4326', geometry=geometry)

        # Export shapefile
        clean_odk_geo_df.to_file(export_dir_path + '//odk_ras_output_wgs84.shp', driver='ESRI Shapefile')

        # --------------------------------------------- EPSG: 32752 ----------------------------------------------------
        # set epsg to WGSz52.
        epsg = 32752

        # Project clean_odk_geo_df to WGSz52.
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # Concatenate, clean and export geo_df_52
        geo_df_52, crs_name_52 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

        # ----------------------------------------------- EPSG: 32753 --------------------------------------------------

        # set epsg to WGSz52
        epsg = 32753

        # Project clean_odk_geo_df to WGSz53
        crs_name, crs_output, projected_df = projection_file_name_fn(epsg, clean_odk_geo_df)

        # Apply a 1ha square buffer to each point.
        buffer_temp_dir = square_buffer_fn(projected_df, prime_temp_buffer_dir, crs_name)

        # Add attributes (SITE_NAME and PROP_CODE) to geo-DataFrame.
        prime_temp_buffer_dir = add_site_attribute_fn(prime_temp_buffer_dir, buffer_temp_dir, crs_name,
                                                      pastoral_estate)

        # Concatenate, clean and export geo_df_53
        geo_df_53, crs_name_53 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

    else:
        pass
        # todo uncomment if time trace for ras is useful
        # print('There are no ras sites to be processed.')

    # Concatenate, clean and export geo_df_52
    crs_name = 'WGS84z52'
    geo_df_52, crs_name_52 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

    # Concatenate, clean and export geo_df_53
    crs_name = 'WGS84z53'
    geo_df_53, crs_name_53 = concatenate_df_fn(prime_temp_buffer_dir, export_dir_path, crs_name)

    return geo_df_52, crs_name_52, geo_df_53, crs_name_53


if __name__ == '__main__':
    main_routine()
