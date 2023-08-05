from dbdreader import DBD, DBDHeader
from dinkum.utils import find_all_dinkum_files, is_dinkum_name, is_science_file
import numpy as np
import os
from collections import defaultdict


# A class designed to mimic Dinkum functionaility using the dbdreader library
class DinkumDBD():
    def __init__(self):
        self.data_files = []
        self.cache_directory = None

    def load_files(self, file_or_directory, cache_directory=None, pair=False):
        self.cache_directory = cache_directory
        if os.path.isfile(file_or_directory):
            if is_dinkum_name(file_or_directory):
                self.data_files.append(file_or_directory)
        elif os.path.isdir(file_or_directory):
            self.data_files = find_all_dinkum_files(file_or_directory)
        else:
            raise FileNotFoundError

        if not self.cache_directory:
            self.cache_directory = cache_directory

        if not self.data_files:
            raise FileNotFoundError
        self.pair = pair

    def merge_flight_and_sci(self, flight_file, sci_file):
        f_data = flight_file.get('data')
        f_meta = flight_file.get('meta')
        s_data = sci_file.get('data')
        s_meta = sci_file.get('meta')
        flight_m_time_index = f_meta.get('columns')[0].index('m_present_time')
        sci_m_present_index = s_meta.get('columns')[0].index('sci_m_present_time')
        flight_columns = len(f_meta.get('columns')[0])
        sci_coloumns = len(s_meta.get('columns')[0])
        merge_meta = self._merge_meta(f_meta, s_meta)
        merge_data = self._merge_data(f_data, s_data, flight_m_time_index, sci_m_present_index,
                                      flight_columns, sci_coloumns)
        merge_result = {'meta': merge_meta, 'data': merge_data}
        return merge_result

    def decode(self, cover_to_df=False):
        if self.pair:
            pair_result = self._pair_files()
            for file_name in pair_result:
                match_files = pair_result.get(file_name)
                if len(match_files) != 2:
                    continue
                yield file_name, match_files
        else:
            for x in self.data_files:
                yield self._decode(x, cover_to_df)
    
    def _decode(self, x, cover_to_df):
        dbd = DBD(x, cacheDir=self.cache_directory)
        header = self._get_header(dbd)
        cache = self._get_cache(dbd)
        sensor_data = self._get_sensor_data(dbd)
        names, units = self._sensor_names_and_units(dbd)

        if cover_to_df:
            df_header = self._combine_names_with_units(names, units)
            ret = {'header': header, 'cache': cache, 'data': sensor_data, 'df': df_header[0], 'unit': df_header[1]}
        else:
            ret = {'header': header, 'cache': cache, 'data': sensor_data, "names": names, "units": units}
        return ret

    def reorder_files(self, path_list):
        if is_science_file(path_list[0]):
            merge_result = [path_list[1], path_list[0]]
        else:
            merge_result = path_list
        return merge_result

    def _combine_names_with_units(self, names, units):
        df_header = []
        df_header.append(names)
        df_header.append(units)
        return df_header

    def _sensor_names_and_units(self, dbd):
        names = dbd.parameterNames
        units = []
        for name in names:
            units.append(dbd.parameterUnits[name])
        return names, units

    def _get_sensor_data(self, dbd):
        ret_arr = []
        sensor_data = dbd.get(*dbd.parameterNames, return_nans=True, decimalLatLon=False)
        for i in range(len(sensor_data[0][1])):
            row = []
            for j in range(len(sensor_data)):
                val = sensor_data[j][1][i]
                if np.isnan(val):
                    row.append("NaN")
                else:
                    if dbd.byteSizes[j] == 1:
                        row.append(int(val))
                    else:
                        row.append(val)
            ret_arr.append(row)
        return ret_arr

    def _get_cache(self, dbd):
        ret = []
        para_names = dbd.parameterNames
        for i in range(len(para_names)):
            ret.append({
                'transmitted': 'T',
                # the sensor number doesn't get stored by dbdreader
                # Dinkum defaults to None, so that's what's done here
                'sensor_number': None,
                'index': str(i),
                'number_of_bytes': str(dbd.byteSizes[i]),
                'sensor_name': para_names[i],
                'unit':dbd.parameterUnits[para_names[i]]
            })
        return ret

    def _pair_files(self):
        if self.pair:
            pair_dict = defaultdict(list)
            for file_with_path in self.data_files:
                file_name = os.path.splitext(os.path.basename(file_with_path))[0]
                pair_dict[file_name].append(file_with_path)
            return dict(pair_dict)

    def _get_header(self, dbd):
        dbd_header = DBDHeader()
        dbd_header.keywords['filename_extension'] = "string"
        dbd_header.keywords['all_sensors'] = "string"
        fp = open(dbd.filename, 'br')
        dbd_header.read_header(fp)
        fp.close()
        ret_dict = {key: str(value) for key, value in dbd_header.info.items()}
        return ret_dict

    def fetch_cache(self):
        found_cache_list = []
        for x in self.data_files:
            original_cache_count = len(os.listdir(self.cache_directory))
            try:
                dbd = DBD(x, cacheDir=self.cache_directory)
            except:
                dbd = None
            if dbd is not None:
                header = self._get_header(dbd)
                cache = self._get_cache(dbd)
                if cache:
                    file_name = header["sensor_list_crc"] + ".cac"
                    if len(os.listdir(self.cache_directory)) > original_cache_count:
                        found_cache_list.append({"cache_file_name": file_name, "data_file_name": os.path.basename(x)})
        return found_cache_list

    def _merge_meta(self, flight, sci):
        merged_meta = []
        if flight.get('dbd_label') == 'DBD_ASC(dinkum_binary_data_ascii)file':
            if sci.get('dbd_label') == 'DBD_ASC(dinkum_binary_data_ascii)file':
                merged_meta.append({'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file'})
            else:
                raise ValueError('Not a DBD_ASC file.')
        else:
            raise ValueError('Not a DBD_ASC file.')
        merged_meta.append({'encoding_ver': flight.get('encoding_ver')})
        merged_meta.append({'num_ascii_tags': flight.get('num_ascii_tags')})
        merged_meta.append({'filename': flight.get('filename')})
        merged_meta.append({'the8x3_filename': flight.get('the8x3_filename')})
        merged_meta.append({'filename_extension': 'edba'})
        merged_meta.append({'filename_label': flight.get('filename_label')})
        merged_meta.append({'mission_name': flight.get('mission_name')})
        merged_meta.append({'fileopen_time': flight.get('fileopen_time')})
        sensors_per_cycle = int(flight.get('sensors_per_cycle')) + int(sci.get('sensors_per_cycle'))
        merged_meta.append({'sensors_per_cycle': sensors_per_cycle})
        merged_meta.append({'num_label_lines': flight.get('num_label_lines')})
        merged_meta.append({'num_segments': flight.get('num_segments')})
        merged_meta.append({'segment_filename_0': flight.get('filename')})
        columns_name = flight.get('columns')[0] + sci.get('columns')[0]
        merged_meta.append({'columns': columns_name})
        units = flight.get('columns')[1] + sci.get('columns')[1]
        merged_meta.append({'units': units})
        num_of_byes = flight.get('columns')[2] + sci.get('columns')[2]
        merged_meta.append({'number_of_bytes': num_of_byes})
        return merged_meta

    def _merge_data(self, flight, sci, m_time_index, sci_present_index, flight_columns_num, sci_columns_num):
        merged_data = []
        i, j = 0, 0
        while i < len(flight) and j < len(sci):
            if flight[i][m_time_index] < sci[j][sci_present_index]:
                line = flight[i] + ['NaN'] * sci_columns_num
                merged_data.append(line)
                i += 1
            elif flight[i][m_time_index] > sci[j][sci_present_index]:
                line = ['NaN'] * flight_columns_num + sci[j]
                merged_data.append(line)
                j += 1
            else:
                line = flight[i] + sci[j]
                merged_data.append(line)
                i += 1
                j += 1
        while i < len(flight):
            line = flight[i] + ['NaN'] * sci_columns_num
            merged_data.append(line)
            i += 1
        while j < len(sci):
            line = ['NaN'] * flight_columns_num + sci[j][0: sci_columns_num]
            merged_data.append(line)
            j += 1
        return merged_data

    def merge_df(self, df, df_appending, flight_type=True):
        if df_appending.dropna().empty:
            merge_result = df
        else:
            merge_result = df_appending.append(df)
            if flight_type:
                merge_result.sort_values(by=['m_present_time'])
            else:
                merge_result.sort_values(by=['sci_m_present_time'])
        return merge_result
