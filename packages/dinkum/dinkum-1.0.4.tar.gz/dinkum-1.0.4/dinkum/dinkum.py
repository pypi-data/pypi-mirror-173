import os
import re
import copy
import bitstring
from collections import defaultdict
import logging

from dinkum.utils import is_dinkum_name, find_all_dinkum_files, is_science_file, DINKUM_MATCH

# 1,2 bytes = signed int
# 4,8 bytes = single / double precision float
byte_typele = ['bits:8', 'bits:8', 'intle:16', 'floatle:32', 'floatle:64']
byte_format_with_number = {
    "1byte": 'bits:8',
    "2bytes": 'int{}:16',
    "4bytes": 'float{}:32',
    "8bytes": 'float{}:64'
}
byte_format = {
    "byte": 'bits:',
    "int": 'int{}:',
    "float": 'float{}:',
}
BIG_ENDIAN = "be"
LITTLE_ENDIAN = "le"
#0x1234 in decimal is 4660
TWO_BYTE_INTEGER_0x1234 = 4660
SENSOR_BEING_TRANSMITTED = 'T'
DATA_START_TAG = 's'
CYCLE_START_TAG = 'd'
CYCLE_END_TAG = 'X'
class Dinkum:
    def __init__(self):
        self.data_directory = None
        self.caches = {}
        self.data_files = []
        self.cache_directory = None
        self.endian = None
        self.df_sensor_name = {}
        self.df_unit = {}

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

    def _pair_files(self):
        if self.pair:
            pair_dict = defaultdict(list)
            for file_with_path in self.data_files:
                file_name = os.path.splitext(os.path.basename(file_with_path))[0]
                pair_dict[file_name].append(file_with_path)
            return dict(pair_dict)

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

    def fetch_cache(self):
        found_cache_list = []
        for x in self.data_files:
            with open(x, 'rb') as f:
                header = self._parse_header(f)
                cache = self._get_cache(f, header, cache_generate=True)
                if cache:
                    file_name = header["sensor_list_crc"] + ".cac"
                    cache_path = os.path.join(self.cache_directory, file_name)
                    if not os.path.isfile(cache_path):
                        with open(cache_path, 'w+') as write_cache:
                            for l in cache:
                                write_cache.write(l)
                        found_cache_list.append({"cache_file_name": file_name, "data_file_name": os.path.basename(x)})
        return found_cache_list

    def _decode(self, x, cover_to_df=False):
        with open(x, 'rb') as f:
            header = self._parse_header(f)
            cache = self._get_cache(f, header)
            if not cache:
                logging.warning(
                    x + ' does not have a cache {}, fail to cover to dataframe'.format(header['sensor_list_crc']))
                return None
            sensor_data = self._parse_sensor_data(f, header, cache)
            cache = self._filter_cache(cache)
            names, units = self._sensor_names_and_units(header, cache)
            if cover_to_df:

                df_header = self._combine_names_with_units(names, units)
                ret = {'header': header, 'cache': cache, 'data': sensor_data, 'df': df_header[0], 'unit': df_header[1]}
            else:
                ret = {'header': header, 'cache': cache, 'data': sensor_data, "names": names, "units": units}
        return ret

    def _sensor_names_and_units(self, header, cache):
        cache_file_name = header['sensor_list_crc']
        names = []
        units = []
        if cache_file_name in self.df_sensor_name:
            names = self.df_sensor_name[cache_file_name]
            units = self.df_unit[cache_file_name]
        else:
            for item in cache:
                names.append(item['sensor_name'])
                units.append(item['unit'])
            self.df_sensor_name[cache_file_name] = names
            self.df_unit[cache_file_name] = units
        return names, units

    def _combine_names_with_units(self, names, units):
        df_header = []
        df_header.append(names)
        df_header.append(units)
        return df_header

    def _get_cache(self, f, header, cache_generate=False):
        cache_file_name = header['sensor_list_crc']
        cache_file_name = cache_file_name + '.cac'
        cache = None
        cache_content = self._get_sensor_cache_content(f)
        if not cache_generate:
            if not cache_content and self.cache_directory:
                cache_file_path = os.path.join(self.cache_directory, cache_file_name)
                try:
                    with open(cache_file_path, 'r') as cache_f:
                        cache_content = cache_f.readlines()
                except FileNotFoundError:
                    ...
                # self.generate_cache_file(cache_file_name, cache_content)

            if cache_content:
                cache = self._parse_sensor_cache(cache_content)
        else:
            return cache_content
        return cache

    def generate_cache_file(self, cache_file_name, cache_content):
        cache_file_path = os.path.join(self.cache_directory, cache_file_name)
        with open(cache_file_path, 'w') as f:
            f.write(cache_content)

    def _parse_header(self, f):
        """
    dbd_label:             Identifies it as a Dinkum Binary Data file.
    encoding_ver:          What encoding version: 5.  (Version 0
                           is reserved for the future development
                           of an OBD to DBD translator.)
    num_ascii_tags:        The number of (key,value) pairs: 14.
    all_sensors:           T (TRUE) means every sensor is being transmitted;
                           F (FALSE) means only some sensors are being
                           transmitted, i.e. this is an *.SBD or *.MBD file.
    the8x3_filename:       The filename on the Glider: 00410011, which
                           stands for the 12th segment of the 41st mission
                           this glider has ever flown.
    full_filename:         What the filename should be on the host
                           (not counting the extension).
    filename_extension:
    mission_name:          The name of the mission file being run.
    fileopen_time:         Human readable date string.
    total_num_sensors:     Total number of sensors in the system.
    sensors_per_cycle:     Number of sensors we are transmitting.
    state_bytes_per_cycle: The number of "state bytes" sent per cycle.
                           These are the state @ 2 bits/sensor.
    sensor_list_crc:       CRC32 of the section <<A sensor list in ASCII>>.
    sensor_list_factored:  1 if the section <<A sensor list in ASCII>>
                           is present, 0 if factored out.
        """
        line = f.readline()
        line = line.decode('utf-8')
        header = dict()
        header['num_ascii_tags'] = 99
        bindata_filepos = f.tell()
        while line.split(':') != 's' and len(header) < int(header['num_ascii_tags']):
            name, content = line.split(':', 1)
            header[name] = content.strip()
            bindata_filepos = f.tell()  # keep this for seeking purposes later.
            line = f.readline()
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                break
        f.seek(bindata_filepos)
        return header

    def _get_sensor_cache_content(self, f):
        cache_content = []
        bindata_filepos = f.tell()
        line = f.readline()
        try:
            line = line.decode('utf-8')
        except UnicodeDecodeError:
            f.seek(bindata_filepos)
            return None
        while line.split(':')[0] == 's':
            cache_content.append(line)
            bindata_filepos = f.tell()  # keep this for seeking
            line = f.readline()
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                f.seek(bindata_filepos)
                break
        return cache_content

    def _parse_sensor_cache(self, cache_list):
        """
        The "s:" marks a sensor line.

        The next field is either:
            T    Sensor being transmitted.
            F    Sensor is NOT being transmitted.

        The next field is the sensor number, from 0 to (total_num_sensors-1).

        The next field is the index, from 0 to (sensors_per_cycle-1), of all the
        sensors being transmitted.  -1 means the sensor is not being transmitted.
        If all_sensors is TRUE, then this and the prior field will be identical.
        The last numerical field is the number of bytes transmitted for each sensor:
        1    A 1 byte integer value [-128 .. 127].
        2    A 2 byte integer value [-32768 .. 32767].
        4    A 4 byte float value (floating point, 6-7 significant digits,
                                   approximately 10^-38 to 10^38 dynamic range).
        8    An 8 byte double value (floating point, 15-16 significant digits,
                                     approximately 10^-308 to 10^308 dyn. range).

        The last two fields are the sensor name and its units.
        """
        cache_pattern = '^s:\s([TF])\s*([0-9]*)\s*([0-9]*|-1)\s*([0-9]*)\s*(\S*)\s*(\S*)$'
        cache_structure = {"transmitted": None, "sensor_number": None, "index": None, "number_of_bytes": None,
                           "sensor_name": None, "unit": None}
        cache_dict_list = []
        for x in cache_list:
            x = x.replace('\n', '')
            # 's: T    0    0 4 sci_badd_error nodim'
            try:
                find = re.match(cache_pattern, x)
                cache_dict = copy.deepcopy(cache_structure)
                cache_dict['transmitted'] = find.group(1)
                cache_dict['sensor_number'] = find.group(2)
                cache_dict['index'] = find.group(3)
                cache_dict['number_of_bytes'] = find.group(4)
                cache_dict['sensor_name'] = find.group(5)
                cache_dict['unit'] = find.group(6)
                cache_dict_list.append(cache_dict)
            except:
                raise ValueError
        return cache_dict_list

    def _parse_sensor_data(self, f, header, cache):
        """
        <<A known bytes binary cycle>>

        Three known binary values are transmitted.  This allows the host
        to detect if any byte swapping is required:
            s                  Cycle Tag (this is an ASCII s char).
            a                  One byte integer.
            0x1234             Two byte integer. to decimal is 4660
            123.456            Four byte float.
            123456789.12345    Eight byte double.

            <<A data cycle with every sensor value transmitted>>
            This is like a regular data cycle, but every sensor is marked as updated
            with a new value.  This represents the initial value of all sensors.
            See <<data cycle>> for the format.

                <<data cycle>>

            The data cycle consists of:
                d                Cycle tag (this is an ASCII d char).
                <state bytes>    There are state_bytes_per_cycle of these binary bytes.
                <sensor data>    1,2,4, or 8 binary bytes for every sensor that was
                  ....                    updated with a new value.
                <sensor data>

            The state bytes consist of 2 bits per sensor.  The MSB of the first byte is
            associated with the first transmitted sensor.  The next two bits, with the
            next sensor, etc.  Any unused bits in the last byte will be 0.

            The meanings of the two bit field for each sensor:
                MSB    LSB
                0      0    Sensor NOT updated.
                0      1    Sensor updated with same value.
                1      0    Sensor updated with new value.
                1      1    Reserved for future use.

                <<end of file cycle>>
                X    cycle tag (a single ASCII X char).

            There may very well be data in the file after this last cycle.  It should be
            ignored.  The Persistor currently has a really annoying habit of transmitting
            a bunch of Control-Z characters after the end of valid data.
            This ought to be fixed.
        """
        cache = self._filter_cache(cache)
        bindata_filepos = f.tell()
        offset = bindata_filepos * 8
        binary_data = bitstring.BitStream(f, offset=offset)
        self.check_byte_swap(binary_data)
        number_of_bytes = []
        for i in cache:
            number_of_bytes.append(i['number_of_bytes'])
        row_size = 0
        for i in number_of_bytes:
            row_size += int(i)

        return self._decode_endian(binary_data, number_of_bytes, header)

    def _decode_endian(self, binary_data, number_of_bytes, header):
        data = []
        frame_check = binary_data.read('bytes:1').decode('utf-8')
        current_values = [None] * int(header['sensors_per_cycle'])
        cache_values = ['NaN'] * int(header['sensors_per_cycle'])
        updated_code = ['00'] * int(header['sensors_per_cycle'])
        while frame_check == 'd':
            for i in range(int(header['sensors_per_cycle'])):
                updated_code[i] = binary_data.read('bin:2')
            binary_data.bytealign()  # Any unused bits in the last byte will be 0.
            for i, code in enumerate(updated_code):
                if code == '00':  # No new value
                    current_values[i] = 'NaN'
                elif code == '01':  # Same value as before.
                    current_values[i] = cache_values[i]
                elif code == '10':
                    if int(number_of_bytes[i]) in [4, 8]:
                        current_values[i] = binary_data.read(
                            byte_format["float"].format(self.endian) + str(int(number_of_bytes[i]) * 8))
                    elif int(number_of_bytes[i]) in [1, 2]:
                        current_values[i] = binary_data.read(
                            byte_format["int"].format(self.endian) + str(int(number_of_bytes[i]) * 8))
                    else:
                        raise ValueError('For No.{} sensor, the number of bytes transmitted was {}.\n'
                                         'Unrecognizable code in data cycle. Parsing failed.'
                                         .format(i, current_values[i]))
                    cache_values[i] = current_values[i]
            cycle_sign = binary_data.peek('bytes:1').decode('utf-8')
            if cycle_sign == CYCLE_START_TAG:  # We've arrived at the next line.
                frame_check = binary_data.read('bytes:1').decode('utf-8')
                data.append([num for num in current_values])
                # Maybe print out the current values to our data structure / out file.
            elif cycle_sign == CYCLE_END_TAG:  # End of file cycle tag. We made it through.
                data.append([num for num in current_values])
                break
            else:
                raise ValueError('Got {} expected d or X'
                                 'Error parsing end of line data at byte position {}.'
                                 .format(cycle_sign, binary_data.bytepos))
        if data:
            s = data.pop(0)  # remove initial value of all sensors

        return data

    def _filter_cache(self, cache_dict):
        new_cache = []
        for x in cache_dict:
            if x['transmitted'] == SENSOR_BEING_TRANSMITTED:
                new_cache.append(x)

        return new_cache

    def check_byte_swap(self, binary_data):
        """
        to detect if any byte swapping is required:
        s                  Cycle Tag (this is an ASCII s char).
        a                  One byte integer.
        0x1234             Two byte integer. to decimal is 4660
        123.456            Four byte float.
        123456789.12345    Eight byte double.
        """
        byte_typele = [byte_format_with_number["1byte"], byte_format_with_number["1byte"],
                       byte_format_with_number["2bytes"].format(LITTLE_ENDIAN),
                       byte_format_with_number["4bytes"].format(LITTLE_ENDIAN),
                       byte_format_with_number["8bytes"].format(LITTLE_ENDIAN)]
        diag_header = binary_data.readlist(byte_typele)
        third_value = diag_header[2]
        if third_value == TWO_BYTE_INTEGER_0x1234:
            self.endian = LITTLE_ENDIAN
        else:
            self.endian = BIG_ENDIAN


    def reorder_files(self, path_list):
        if is_science_file(path_list[0]):
            merge_result = [path_list[1], path_list[0]]
        else:
            merge_result = path_list
        return merge_result

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
