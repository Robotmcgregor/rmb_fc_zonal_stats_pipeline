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

# Import modules
from __future__ import print_function, division
import os
from datetime import datetime
import argparse
import shutil
import sys
import pandas as pd
from glob import glob
import warnings
import geopandas as gpd

warnings.filterwarnings("ignore")


def get_cmd_args_fn():
    p = argparse.ArgumentParser(description='Produce zonal plots (.jpg) and interactive .html files.')

    p.add_argument('-d', '--directory_zonal', help='The directory containing the zonal stats csv files (default)',
                   default=r'Z:\Scratch\Zonal_Stats_Pipeline\rmb_fractional_cover_zonal_stats\outputs\20210621_2016\zonal_stats')

    p.add_argument('-x', '--export_dir', help='Enter the export directory for all outputs (default)',
                   default=r'Z:\Scratch\Zonal_Stats_Pipeline\rmb_fractional_cover_zonal_stats\outputs')

    p.add_argument('-r', '--rainfall_dir', help='The directory containing the rainfall zonal stats csv files (default)',
                   default=r'Z:\Scratch\Zonal_Stats_Pipeline\rmb_fractional_cover_zonal_stats\outputs\20210621_2016\rainfall')

    p.add_argument('-e', '--end_date', help='Final date for the rainfall data override (i.e.2020-08-31) Do not enter if'
                                            'you want the script to determine the finish date..',
                   default='2021-06-30')

    p.add_argument('-i', '--rainfall_raster_dir', help='Directory containing the rainfall raster images (default)',
                   default=r'Z:\Scratch\Zonal_Stats_Pipeline\rainfall')

    p.add_argument('-v', '--visits', help='Path to the latest integrated site shapefile containing previous '
                                          'visit information (default).',
                   default=r"Z:\Scratch\Zonal_Stats_Pipeline\shapefiles\NT_StarTransect_20200713.shp")

    p.add_argument('-p', '--pastoral_estate', help='File path to the pastoral estate shapefile.',
                   default=r"Z:\Scratch\Rob\shapefiles\pastoral_estate.shp")

    p.add_argument('-m', '--rolling_mean', help='Integer value (i.e 3 or 5) to create the rolling mean of the date.',
                   default=5)

    p.add_argument('-pd', '--pastoral_districts_dir', help='File path to the Pastoral_Districts directory.',
                   default=r"Z:\Scratch\Zonal_Stats_Pipeline\rmb_aggregate_processing\Pastoral_Districts")

    cmdargs = p.parse_args()

    if cmdargs.directory_zonal is None:
        p.print_help()

        sys.exit()

    return (cmdargs)


def export_dir_fn(export_dir):
    """Create an export directory 'YYYMMDD_HHMM' at the location specified in command argument exportDir.

    :param export_dir: string object containing the path to the export directory.
    :return export_dir_path: string object containing the path to a newly created folder within the
            export_dir. """

    # create file name based on date and time.
    date_time_replace = str(datetime.now()).replace('-', '')
    date_time_list = date_time_replace.split(' ')
    date_time_list_split = date_time_list[1].split(':')
    export_dir_path = export_dir + '\\' + str(date_time_list[0]) + '_' + str(date_time_list_split[0]) + str(
        date_time_list_split[1])

    # check if the folder already exists - if False = create directory, if True = return error message.
    try:
        shutil.rmtree(export_dir_path)

    except:
        print('The following directory did not exist: ', export_dir_path)

    # create folder
    os.makedirs(export_dir_path)

    return export_dir_path


def create_export_dir_fn(export_dir_path):
    """ Create export directory folder structure.

    @param export_dir_path: string object containing the path to a newly created folder within the
    export_dir.
    @return plot_dir: string object containing the path to a newly created plot folder within the
    export_dir.
    """

    # Create folders within the tempDir directory.
    plot_dir = export_dir_path + '\\plots'
    os.mkdir(plot_dir)

    interactive_dir = plot_dir + '\\interactive'
    os.mkdir(interactive_dir)

    final_plot_dir = export_dir_path + '\\final_plots'
    os.mkdir(final_plot_dir)

    final_inter_dir = export_dir_path + '\\final_interactive'
    os.mkdir(final_inter_dir)

    return plot_dir


def glob_create_df(directory, search_criteria):
    """ Search for files with the matching search criteria passed through the function, open as pandas data frames and
    store in a list.

    @param directory: input dictionary containing the property name and either the prop tag or district for the property.
    @param search_criteria: string object passed into the function used to match files.
    @return df: pandas dataframe created from the located dataframes that met the search criteria.
    @return file_list: list objet containing open data frames.
    """

    # create a df from all csv files in a directory.
    list_df = []
    file_list = []
    # search through the directory
    for file in glob(directory + search_criteria):
        file_list.append(file)
        df = pd.read_csv(file)
        list_df.append(df)

    df = pd.concat(list_df)

    return df, file_list


def list_dir(rainfall_raster_dir, search_criteria):
    """ Return a list of the rainfall raster images in a directory for the given file extension.

    @param rainfall_raster_dir: string object containing the rainfall directory path (command argument)
    @param search_criteria: string object passed into the function used to match files.
    @return list_image: list object containing the path to all files that matched the search criteria.
    """

    list_image = []

    for root, dirs, files in os.walk(rainfall_raster_dir):

        for file in files:

            if file.endswith(search_criteria):
                img = (os.path.join(root, file))
                list_image.append(img)

    return list_image


def rainfall_start_fin_dates(list_image):
    """ Extract the first and last dates for available rainfall images.

    @param list_image: list object containing the path to all files that matched the search criteria.
    @return rain_start_date: string object containing the first image date.
    @return rain_finish_date: string object containing the last image date. """

    print('-' * 50)
    # sort the list image
    list_image.sort()
    path_s = list_image[0]

    image_ = path_s.rsplit('\\')
    image_name = image_[-1]

    year_s = image_name[:4]
    month_s = image_name[4:6]
    rain_start_date = (str(year_s) + '-' + str(month_s) + '-01')

    path_f = list_image[-1]
    image_ = path_f.rsplit('\\')
    image_name = image_[-1]

    year_f = image_name[:4]
    month_f = image_name[4:6]

    rain_finish_date = (str(year_f) + '-' + str(month_f) + '-30')
    print('rain_finish_date: ', rain_finish_date)

    return rain_start_date, rain_finish_date


def main_routine(zonal_dir, export_dir, rainfall_dir, end_date, rainfall_raster_dir, previous_visits,
                 pastoral_estate, rolling_mean, pastoral_districts_dir, zonal_stats_ready_dir):
    """ Created time series plots using matplotlib one per site per tile and interactive time series plots using Boken.
    Plots are sorted based on which tile registered the most amount of zonal stats hits (i.e. limited cloud masking)."""

    # read in the command arguments
    """cmdargs = get_cmd_args_fn()
    zonal_dir = cmdargs.directory_zonal
    export_dir = cmdargs.export_dir
    rainfall_dir = cmdargs.rainfall_dir
    end_date = cmdargs.end_date
    rainfall_raster_dir = cmdargs.rainfall_raster_dir
    previous_visits = cmdargs.visits
    pastoral_estate = cmdargs.pastoral_estate
    rolling_mean = cmdargs.rolling_mean
    pastoral_districts_dir = cmdargs.pastoral_districts_dir"""

    print('=' * 50)
    print('Initiate plotting')
    print('=' * 50)
    # call the export_dir function.
    # export_dir_path = export_dir_fn(export_dir)
    export_dir_path = export_dir
    # call the create_export_dir_fn function.
    # plot_dir = create_export_dir_fn(export_dir_path)
    plot_dir = "{0}\\plots".format(export_dir_path)
    output_zonal_stats, zonal_file_list = glob_create_df(zonal_dir, '//*.csv')

    output_rainfall, rainfall_file_list = glob_create_df(rainfall_dir, '//*.csv')
    list_image = list_dir(rainfall_raster_dir, '.tif')

    rain_start_date, rain_finish_date = rainfall_start_fin_dates(list_image)
    print(rain_finish_date)

    if end_date is not None:
        finish_date = str(rain_finish_date)
    else:
        finish_date = '2022-10-30'

    # read in the pastoral estate shapefile and create two property dictionaries to extract the district and prop tag
    # information.
    pastoral_estate_gdf = gpd.read_file(pastoral_estate)
    prop_dist_dict = dict(zip(pastoral_estate_gdf.PROPERTY, pastoral_estate_gdf.DISTRICT))
    prop_tag_dict = dict(zip(pastoral_estate_gdf.PROPERTY, pastoral_estate_gdf.PROP_TAG))

    for tile in zonal_file_list:
        # strip Landsat tile label from csv file name.

        print('=' * 50)
        test_tile = tile.split('_')
        complete_tile = test_tile[-3]
        output_zonal_stats = pd.read_csv(tile)

        # import step2_2_bare_ground_plots
        # step2_2_bare_ground_plots.main_routine(output_zonal_stats, output_rainfall, complete_tile, previous_visits,
        #                                        plot_dir, rolling_mean, finish_date)

        import step2_3_interactive_plots
        step2_3_interactive_plots.main_routine(export_dir_path, output_zonal_stats, complete_tile,
                                               plot_dir, pastoral_estate, rolling_mean)

    import step2_4_sort_plots
    step2_4_sort_plots.main_routine(export_dir_path, zonal_dir)

    import step2_5_file_plots_to_working_drive
    step2_5_file_plots_to_working_drive.main_routine(pastoral_districts_dir, export_dir_path, zonal_dir, rainfall_dir,
                                                     finish_date, prop_dist_dict, prop_tag_dict, zonal_stats_ready_dir)

    print('Zonal stats and plots have been created!!.'
          'The zonal stats pipeline has finished.')


if __name__ == '__main__':
    main_routine()
