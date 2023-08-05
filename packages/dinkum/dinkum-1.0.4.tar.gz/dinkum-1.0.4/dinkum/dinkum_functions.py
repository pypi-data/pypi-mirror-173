import os
from dinkum.dinkum import Dinkum
from dinkum.dinkum_ascii_generate import generate_ascii_content, generate_ascii_file_name, generate_merge_content
from dinkum.utils import find_all_dinkum_files
from dinkum.dinkum_ascii_reader import parse_dbd2asc_result
import pandas as pd
from dbdreader import DBD
from dinkum.dinkum_dbd import DinkumDBD

__all__ = ['dinkum2dicts', 'dinkum2pandas', 'dinkum2ascii', 'dinkumMergeAscii', 'dinkumMergeBinary', 'dbd_asc2dict', 'cache_generator']


def dinkum2dicts(source_directory_or_file, cache_directory):
    dict_list = []
    my_dinkum = DinkumDBD()
    my_dinkum.load_files(source_directory_or_file, cache_directory)
    for data in my_dinkum.decode():
        dict_list.append(data)
    return dict_list


def dinkum2pandas(source_directory_or_file, cache_directory, with_unit=False, appending=False):
    dataframe_list = []
    my_dinkum = DinkumDBD()
    my_dinkum.load_files(source_directory_or_file, cache_directory)
    flight_appending = pd.DataFrame()
    sci_appending = pd.DataFrame()
    flight_unit = None
    sci_unit = None
    for data in my_dinkum.decode(cover_to_df=True):
        if data:
            df = pd.DataFrame(data['data'], columns=data['df'])
            if appending:
                if 'm_present_time' in df.columns:
                    if flight_unit is None:
                        flight_unit = pd.DataFrame([data['unit']], columns=data['df'])
                    flight_appending = my_dinkum.merge_df(df, flight_appending, True)
                else:
                    if sci_unit is None:
                        sci_unit = pd.DataFrame([data['unit']], columns=data['df'])
                    sci_appending = my_dinkum.merge_df(df, sci_appending, False)
            else:
                dataframe_list.append(df)
    if with_unit:
        flight_appending = pd.concat([flight_unit, flight_appending], ignore_index=True)
        sci_appending = pd.concat([sci_unit, sci_appending], ignore_index=True)
    if appending:
        return flight_appending, sci_appending
    return dataframe_list


def dinkum2ascii(source_directory_or_file, cache_directory, output_directory):
    my_dinkum = DinkumDBD()
    my_dinkum.load_files(source_directory_or_file, cache_directory)
    for data in my_dinkum.decode():
        if data:
            ascii_content = generate_ascii_content(data)
            file_name = generate_ascii_file_name(data)
            file_name_path = os.path.join(output_directory, file_name)
            with open(file_name_path, 'w') as f:
                f.write(ascii_content)


def dinkumMergeAscii(source_directory_or_file_list, output_directory=None):
    my_dinkum = DinkumDBD()
    merged_dicts_list = []
    if isinstance(source_directory_or_file_list, list):
        my_dinkum.pair = True
        my_dinkum.data_files = source_directory_or_file_list
    else:
        my_dinkum.load_files(source_directory_or_file_list, None, True)
    for file_name, file_path_list in my_dinkum.decode():
        reorder_list = my_dinkum.reorder_files(file_path_list)
        flight = dbd_asc2dict(reorder_list[0])
        sci = dbd_asc2dict(reorder_list[1])
        merged_dict = my_dinkum.merge_flight_and_sci(flight, sci)
        merged_dicts_list.append(merged_dict)
        if output_directory:
            ascii_content = generate_merge_content(merged_dict)
            merged_file_name = str(os.path.basename(reorder_list[0]))
            merged_file_name = merged_file_name.replace('-', '_')
            merged_file_name = merged_file_name.replace('.', '_')
            merged_file_name = merged_file_name + '.dat'
            file_name_path = os.path.join(output_directory, merged_file_name)
            print(file_name_path)
            with open(file_name_path, 'w') as f:
                f.write(ascii_content)
    return merged_dicts_list


def dinkumMergeBinary(source_directory, cache_directory, destination_directory):
    ascii_dir = os.path.join(source_directory, 'decode_result')
    path_exists = os.path.exists(ascii_dir)
    if not path_exists:
        os.makedirs(ascii_dir)
    dinkum2ascii(source_directory, cache_directory, ascii_dir)
    merged_dicts_list = dinkumMergeAscii(ascii_dir, destination_directory)
    return merged_dicts_list


def dbd_asc2dict(dbd_asc_name, column_output=None):
    res = parse_dbd2asc_result(dbd_asc_name, column_output)
    return res


def cache_generator(source_directory, cache_directory):
    my_dinkum = DinkumDBD()
    my_dinkum.load_files(source_directory, cache_directory)
    return my_dinkum.fetch_cache()