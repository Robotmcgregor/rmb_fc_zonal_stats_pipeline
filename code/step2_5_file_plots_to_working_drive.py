#!/usr/bin/env python

"""
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
"""

# import modules
from __future__ import print_function, division
import pandas as pd
import glob
import os
import shutil
import warnings
import geopandas as gpd

warnings.filterwarnings("ignore")


def create_sub_directories_fn(sub, directory):
    """Check if a sub-directory exists and create it if it does not.
    @param sub: string object containing the sub-directory.
    @param directory: string object containing the path to an existing directory.
    """
    output = '{0}\\{1}'.format(directory, str(sub))

    if not os.path.exists(output):
        os.mkdir(output)

    return output


def glob_dir_fn(zonal_dir, export_dir, prop_output, file_end, prop_list, year):
    """  Search a specified Directory (zonalStats) and concatenate all records to a DataFrame.

        @param year:
        @param prop_list: list object containing a list of paths to the property level sub-directory within the
        pastoral districts directory.
        @param file_end: string object containing the sub-directory for the export file type (i.e. Shp or Csv)
        @param prop_output:
        @param export_dir:
        @param zonal_dir: list object containing the path to the fractional cover zonal stats directory.
        @return df_concat: pandas data frame object - all zonal stats csv files concatenated together."""

    for file_path in glob.glob(zonal_dir + '\\*'):

        _, file = file_path.rsplit('\\', 1)
        tile_name = file.split('_')
        tile_name_ = tile_name[-3]

        if tile_name_ == 'rainfall':
            tile_ = tile_name[-4]
        else:
            tile_ = tile_name[-3]

        print('-' * 50)
        print('tile_: ', tile_)

        # read in all zonal stats csv
        df = pd.read_csv(file_path)
        comp_site_list = df.prop_name.unique().tolist()

        for prop in comp_site_list:
            ind_prop_output = create_sub_directories_fn(prop, prop_output)

            site_df = df.loc[df['prop_name'] == prop]
            file_output = '{0}\\{1}_{2}{3}.csv'.format(ind_prop_output, str(prop), str(tile_), file_end)
            print("Output: ", file_output)
            site_df.to_csv(file_output)

            matching_path = [s for s in prop_list if prop in s]

            prop_dir_path = matching_path[0]
            dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Zonal_Stats')

            year_dir_path = create_sub_directories_fn(str(year), dest_prop_path)
            raw_year_dir_path = create_sub_directories_fn('Raw', year_dir_path)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(raw_year_dir_path, str(prop), str(tile_), file_end)
            print("Output: ", file_output)
            site_df.to_csv(file_output)

    return prop_dir_path


def glob_rainfall_dir_fn(rainfall_dir, export_dir, prop_output, file_end, prop_list):
    """  Search a specified Directory (zonalStats) and concatenate all records to a DataFrame.

        @param zonal_dir: list object containing the path to the fractional cover zonal stats directory.
        @return df_concat: pandas data frame object - all zonal stats csv files concatenated together."""

    for file_path in glob.glob(rainfall_dir + '\\*'):

        _, file = file_path.rsplit('\\', 1)
        _, tile = file.rsplit('_', 1)
        tile_name, _ = tile.rsplit('.', 1)
        # read in all zonal stats csv
        df = pd.read_csv(file_path)
        comp_site_list = df.prop_name.unique().tolist()

        for prop in comp_site_list:
            ind_prop_output = create_sub_directories_fn(prop, prop_output)

            site_df = df.loc[df['prop_name'] == prop]
            site_date = site_df['site_date'].iloc[0]
            _, year = site_date.rsplit('.', 1)

            file_output = '{0}\\{1}_{2}{3}.csv'.format(ind_prop_output, str(prop), str(tile_name), file_end)
            print("Output: ", file_output)
            site_df.to_csv(file_output)

            matching_path = [s for s in prop_list if prop in s]
            prop_dir_path = matching_path[0]
            dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Zonal_Stats')

            year_dir_path = create_sub_directories_fn(str(year), dest_prop_path)
            raw_year_dir_path = create_sub_directories_fn('Raw', year_dir_path)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(raw_year_dir_path, str(prop), str(tile_name), file_end)
            print("Output: ", file_output)
            site_df.to_csv(file_output)


def property_path_fn(pastoral_districts_dir, prop_dist_dict, prop_tag_dict):
    prop_list = []
    for key, value in prop_dist_dict.items():

        prop_key = key
        prop = key.replace(' ', '_').title()
        dist = value.replace(' ', '_').title()

        if dist == 'Northern_Alice_Springs':
            district = 'Northern_Alice'
        elif dist == 'Southern_Alice_Springs':
            district = 'Southern_Alice'
        elif dist == 'Victoria_River':
            district = 'VRD'
        else:
            district = dist

        prop_code = prop_tag_dict[prop_key]
        final_prop = "{0}_{1}".format(prop_code, prop)
        path = os.path.join(pastoral_districts_dir, district, final_prop)
        prop_list.append(path)

    return prop_list


def glob_plot_dir_fn(export_dir, search_criteria, year, folder_, folder_name, prop_dir_path):
    """ ."""

    print("searching in: ", export_dir, folder_, search_criteria)

    for file_path in glob.glob('{0}\\{1}\\{2}'.format(export_dir, folder_, search_criteria)):
        print('located: ', file_path)

        _, file_name = os.path.split(file_path)

        dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Time_Trace')
        # print('dest_prop_path: ', dest_prop_path)

        year_dir_path = create_sub_directories_fn(str(year), dest_prop_path)
        raw_year_dir_path = create_sub_directories_fn('Raw', year_dir_path)
        final_dir_path = create_sub_directories_fn(folder_name, raw_year_dir_path)
        shutil.copy(file_path, final_dir_path)
        print("Output: ", os.path.join(final_dir_path, file_name))


def assets_search_fn(search_criteria, folder):
    """ Searches through a specified directory "folder" for a specified search item "search_criteria".

    @param search_criteria: string object containing a search variable including glob wildcards.
    @param folder: string object containing the path to a directory.
    @return files: string object containing the path to any located files or "" if none were located.
    """
    path_parent = os.path.dirname(os.getcwd())
    assets_dir = (path_parent + '\\' + folder)

    files = ""
    file_path = (assets_dir + '\\' + search_criteria)
    for files in glob.glob(file_path):
        pass

    return files


def glob_dir_1_ha_fn(ha_directory, prop_list, year):
    """  Search a temporary directory for the 1ha shapefile and export for property.

    @param ha_directory: list object containing the path to the temporary directory with 1ha shapefiles produced
    under step1_4_landsat_tile_list.
    @param year: integer object containing the current year.
    @param prop_list: list object containing all located property sub-directory paths.
    """

    gdf_list = []
    for file_path in glob.glob(ha_directory + '\\*.shp'):
        _, file = file_path.rsplit('\\', 1)
        gdf = gpd.read_file(file_path)
        gdf['crs'] = str(gdf.crs)
        gda94 = gdf.to_crs(epsg=4283)

        gdf_list.append(gda94)

    complete_gdf = pd.concat(gdf_list)

    for prop in complete_gdf.prop_name.unique():
        prop_gdf = complete_gdf[complete_gdf['prop_name'] == prop]
        prop_tag = prop_gdf.loc[prop_gdf['prop_name'] == prop, 'prop_code'].iloc[0]
        prop_final = "{0}_{1}".format(prop_tag, prop)
        # print('prop_final: ', prop_final)

        matching_path = [s for s in prop_list if prop_final in s]
        prop_dir_path = matching_path[0]

        data_path = create_sub_directories_fn('Data', prop_dir_path)
        odk_path = create_sub_directories_fn('Processed_Odk', data_path)
        prop_path = create_sub_directories_fn('Property', odk_path)
        year_path = create_sub_directories_fn(str(year), prop_path)
        output_path = create_sub_directories_fn('Shp', year_path)

        file_output = '{0}\\{1}_1ha_plot_gda94.shp'.format(output_path, str(prop_final))
        print("Output: ", file_output)
        prop_gdf.to_file(file_output, driver="ESRI Shapefile")


def main_routine(pastoral_districts_dir, export_dir_path, zonal_dir, rainfall_dir, finish_date,
                 prop_dist_dict, prop_tag_dict, zonal_stats_ready_dir):

    print("Transferring plots to working drive")
    if zonal_stats_ready_dir:
        print(zonal_stats_ready_dir)
    prop_output = '{0}\\{1}'.format(export_dir_path, 'prop_output')
    if not os.path.exists(prop_output):
        print('Create the following directory:')
        print(' - ', prop_output)
        os.mkdir(prop_output)

    prop_list = property_path_fn(pastoral_districts_dir, prop_dist_dict, prop_tag_dict)
    year = finish_date.split('-')[0]

    prop_dir_path = glob_dir_fn(zonal_dir, export_dir_path, prop_output, '_fc_zonal_stats', prop_list, year)
    prop_dir_path = glob_dir_fn(rainfall_dir, export_dir_path, prop_output, '_rain_zonal_stats', prop_list, year)
    #glob_plot_dir_fn(export_dir_path, 'All_B*.png', year, 'final_plots', 'All_Bands', prop_dir_path)
    # glob_plot_dir_fn(export_dir_path, 'BG*.png', year, 'final_plots', 'Bare_Ground', prop_dir_path)
    glob_plot_dir_fn(export_dir_path, '*.html', year, 'final_interactive', 'Interactive', prop_dir_path)

    # stops transfer of a shapefile during plotting only pipeline
    if zonal_stats_ready_dir:
        glob_dir_1_ha_fn(zonal_stats_ready_dir, prop_list, year)


if __name__ == "__main__":
    main_routine()
