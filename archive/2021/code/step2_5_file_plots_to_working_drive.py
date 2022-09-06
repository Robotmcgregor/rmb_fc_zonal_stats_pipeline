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

warnings.filterwarnings("ignore")


def create_subFolders_fn(prop_name, prop_output):
    output = '{0}\\{1}'.format(prop_output, str(prop_name))
    if not os.path.exists(output):
        os.mkdir(output)

    return output


def glob_dir_fn(zonal_dir, export_dir, prop_output, file_end, prop_list):
    """  Search a specified Directory (zonalStats) and concatenate all records to a DataFrame.

        :param zonal_dir: list object containing the path to the fractional cover zonal stats directory.
        :return df_concat: pandas data frame object - all zonal stats csv files concatenated together."""
    print('P' * 50)
    for file_path in glob.glob(zonal_dir + '\\*'):
        print('file: ', file_path)
        _, file = file_path.rsplit('\\', 1)
        _, tile = file.rsplit('_', 1)
        tile_name, _ = tile.rsplit('.', 1)
        # read in all zonal stats csv
        df = pd.read_csv(file_path)
        comp_site_list = df.prop_name.unique().tolist()

        for prop in comp_site_list:
            ind_prop_output = create_subFolders_fn(prop, prop_output)
            print('ind_prop_output: ', ind_prop_output)
            site_df = df.loc[df['prop_name'] == prop]
            site_date = site_df['site_date'].iloc[0]
            _, year = site_date.rsplit('.', 1)

            print(site_date)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(ind_prop_output, str(prop), str(tile_name), file_end)
            print('line 72 file output: ', file_output)
            site_df.to_csv(file_output)

            matching_path = [s for s in prop_list if prop in s]
            prop_dir_path = matching_path[0]
            dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Zonal_Stats')
            print('dest_prop_path: ', dest_prop_path)

            year_dir_path = create_subFolders_fn(str(year), dest_prop_path)
            raw_year_dir_path = create_subFolders_fn('Raw', year_dir_path)
            print(']' * 50)
            print('raw_year_dir_path: ', raw_year_dir_path)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(raw_year_dir_path, str(prop), str(tile_name), file_end)
            print('line 84 site df output: ', file_output)
            site_df.to_csv(file_output)
            print('P' * 50)


def glob_rainfall_dir_fn(rainfall_dir, export_dir, prop_output, file_end, prop_list):
    """  Search a specified Directory (zonalStats) and concatenate all records to a DataFrame.

        :param zonal_dir: list object containing the path to the fractional cover zonal stats directory.
        :return df_concat: pandas data frame object - all zonal stats csv files concatenated together."""
    print('P' * 50)
    for file_path in glob.glob(rainfall_dir + '\\*'):
        print('file: ', file_path)
        _, file = file_path.rsplit('\\', 1)
        _, tile = file.rsplit('_', 1)
        tile_name, _ = tile.rsplit('.', 1)
        # read in all zonal stats csv
        df = pd.read_csv(file_path)
        comp_site_list = df.prop_name.unique().tolist()

        for prop in comp_site_list:
            ind_prop_output = create_subFolders_fn(prop, prop_output)
            print('ind_prop_output: ', ind_prop_output)
            site_df = df.loc[df['prop_name'] == prop]
            site_date = site_df['site_date'].iloc[0]
            _, year = site_date.rsplit('.', 1)

            print(site_date)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(ind_prop_output, str(prop), str(tile_name), file_end)
            print('line 72 file output: ', file_output)
            site_df.to_csv(file_output)

            matching_path = [s for s in prop_list if prop in s]
            prop_dir_path = matching_path[0]
            dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Zonal_Stats')
            print('dest_prop_path: ', dest_prop_path)

            year_dir_path = create_subFolders_fn(str(year), dest_prop_path)
            raw_year_dir_path = create_subFolders_fn('Raw', year_dir_path)
            print(']' * 50)
            print('raw_year_dir_path: ', raw_year_dir_path)
            file_output = '{0}\\{1}_{2}{3}.csv'.format(raw_year_dir_path, str(prop), str(tile_name), file_end)
            print('line 84 site df output: ', file_output)
            site_df.to_csv(file_output)
            print('P' * 50)


def property_path_fn(path):
    """ Create a path to all property sub-directories and return them as a list.

    :param path: string object containing the path to the Pastoral Districts directory.
    :return prop_list: list object containing the path to all property sub-directories.
    """
    # create a list of pastoral districts.
    dir_list = next(os.walk(path))[1]

    prop_list = []

    # loop through districts to get property name
    for district in dir_list:
        dist_path = os.path.join(path, district)

        property_dir = next(os.walk(dist_path))[1]

        # loop through the property names list
        for prop_name in property_dir:
            # join the path, district and property name to create a path to each property directory.
            prop_path = os.path.join(path, district, prop_name)
            # append all property paths to a list
            prop_list.append(prop_path)

    print('prop_list(line 113): ', prop_list)
    return prop_list


def glob_plot_dir_fn(export_dir, prop_list, search_criteria, year, n, folder_, folder_name):
    """ ."""
    print('n' * 50)
    print('line 120 searching for: ', '{0}\\{1}\\{2}'.format(export_dir, folder_, search_criteria))
    for file_path in glob.glob('{0}\\{1}\\{2}'.format(export_dir, folder_, search_criteria)):
        print('=' * 50)
        print('file: ', file_path)
        _, file = file_path.rsplit('\\', 1)
        prop = file.split('_')[n]

        matching_path = [s for s in prop_list if prop in s]
        prop_dir_path = matching_path[0]
        print('prop_dir_path (130): ', prop_dir_path)
        dest_prop_path = os.path.join(prop_dir_path, 'Data', 'Rs_Outputs', 'Time_Trace')

        year_dir_path = create_subFolders_fn(str(year), dest_prop_path)
        raw_year_dir_path = create_subFolders_fn('Raw', year_dir_path)
        final_dir_path = create_subFolders_fn(folder_name, raw_year_dir_path)
        print('line136_' * 20)
        print('file_path: ', file_path)
        print('final_dir_path; ', final_dir_path)
        shutil.copy(file_path, final_dir_path)


def assets_search_fn(search_criteria, folder):
    """ Searches through a specified directory "folder" for a specified search item "search_criteria".

    :param search_criteria: string object containing a search variable including glob wildcards.
    :param folder: string object containing the path to a directory.
    :return files: string object containing the path to any located files or "" if none were located.
    """
    path_parent = os.path.dirname(os.getcwd())
    assets_dir = (path_parent + '\\' + folder)

    files = ""
    file_path = (assets_dir + '\\' + search_criteria)
    for files in glob.glob(file_path):
        print(search_criteria, 'located.')
        pass

    return files


"""
def extract_paths_fn(upload_list, transition_dir):
    #transition_dir = r'Z:\Scratch\Zonal_Stats_Pipeline\Infrastructure_transition_DO_NOT_EDIT'
    year = '2021'
    folder_list = ['points', 'lines', 'polygons']
    print(upload_list)
    for i in upload_list:
        #print(i)
        for n in folder_list:

            direct = os.path.join(i, year, n)
            output_dir = os.path.join(transition_dir, n)
            check_folder = os.path.isdir(direct)
            if check_folder:
                for files in glob(direct + '\\*'):
                    print('files: ', files)
                    if not files.endswith('.shp.xml'):

                        shutil.copy(files, output_dir)
                    else:
                        print(files, 'not copied')"""


def main_routine(pastoral_districts_dir, export_dir_path, zonal_dir, rainfall_dir,
                 finish_date):  # df_tile, export_dir, zonal_dir):

    """pastoral_districts_dir = r"Z:\Scratch\Zonal_Stats_Pipeline\rmb_aggregate_processing\Pastoral_Districts"
    export_dir_path = r"Z:\Scratch\Zonal_Stats_Pipeline\rmb_fractional_cover_zonal_stats\outputs\20210621_2016"
    zonal_dir = '{0}\\{1}'.format(export_dir_path, 'zonal_stats')
    rainfall_dir = '{0}\\{1}'.format(export_dir_path, 'rainfall')"""

    prop_output = '{0}\\{1}'.format(export_dir_path, 'prop_output')
    if not os.path.exists(prop_output):
        os.mkdir(prop_output)

    print('step1_2_search_folders.py INITIATED.')

    prop_list = property_path_fn(pastoral_districts_dir)

    glob_dir_fn(zonal_dir, export_dir_path, prop_output, '_fc_zonal_stats', prop_list)

    glob_dir_fn(rainfall_dir, export_dir_path, prop_output, '_rain_zonal_stats', prop_list)

    year = finish_date.split('-')[0]
    print('year: ', year)

    glob_plot_dir_fn(export_dir_path, prop_list, 'All_B*.png', year, -5, 'final_plots', 'All_Bands')

    glob_plot_dir_fn(export_dir_path, prop_list, 'BG*.png', year, -5, 'final_plots', 'Bare_Ground')

    glob_plot_dir_fn(export_dir_path, prop_list, '*.html', year, -4, 'final_interactive', 'Interactive')


if __name__ == "__main__":
    main_routine()
