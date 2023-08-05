import os
import time
import dinkum
from io import StringIO
from unittest import TestCase
from dinkum.dinkum import Dinkum
from dinkum.dinkum_ascii_generate import generate_ascii_header, generate_variable_name_unit_and_size, \
    generate_ascii_content
from dinkum.dinkum_ascii_reader import read
from shutil import rmtree
from dbdreader import DBD


class TestDinkium(TestCase):
    def setUp(self):
        self.resource_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
        self.raw_path = os.path.join(self.resource_path, 'raw')
        self.sample_file = os.path.join(self.raw_path, '01280000.DBD')
        self.cache_path = os.path.join(self.raw_path, 'cache')
        self.sample2_file = os.path.join(self.raw_path, '00940161.DBD')
        self.sample3_file = os.path.join(self.raw_path, '00940161.EBD')
        self.sample4_file = os.path.join(self.raw_path, '01670028.DBD')
        self.sample5_file = os.path.join(self.raw_path, '01340007.DBD')
        self.sample6_file = os.path.join(self.raw_path, '01340007.EBD')
        self.my_dinkum = Dinkum()

    def test_get_header(self):
        with open(self.sample_file, 'rb') as f:
            header = self.my_dinkum._parse_header(f)

        expected_output = {'sensor_list_factored': '1', 'state_bytes_per_cycle': '402', 'num_ascii_tags': '14',
                           'dbd_label': 'DBD(dinkum_binary_data)file', 'filename_extension': 'dbd', 'encoding_ver': '5',
                           'the8x3_filename': '01280000', 'mission_name': 'STATUS.MI', 'all_sensors': 'F',
                           'total_num_sensors': '2462', 'full_filename': 'scotia-2018-316-1-0',
                           'sensors_per_cycle': '1608', 'sensor_list_crc': '00cda96e',
                           'fileopen_time': 'Tue_Nov_13_02:45:27_2018'}
        self.assertEqual(expected_output, header)

    def test_get_header2(self):
        with open(self.sample2_file, 'rb') as f:
            header2 = self.my_dinkum._parse_header(f)
        expected_header2 = {'sensors_per_cycle': '2077', 'full_filename': 'dal556-2016-077-0-161',
                            'sensor_list_factored': '1', 'the8x3_filename': '00940161',
                            'fileopen_time': 'Tue_Apr__5_20:04:36_2016', 'mission_name': 'STOCK.MI',
                            'state_bytes_per_cycle': '520', 'total_num_sensors': '2077', 'filename_extension': 'dbd',
                            'all_sensors': 'T', 'num_ascii_tags': '14', 'encoding_ver': '5',
                            'dbd_label': 'DBD(dinkum_binary_data)file', 'sensor_list_crc': '825a5b11'}
        self.assertEqual(expected_header2, header2)

    def test_get_header3(self):
        with open(self.sample3_file, 'rb') as f:
            header = self.my_dinkum._parse_header(f)
        expected_header = {'encoding_ver': '5', 'num_ascii_tags': '14', 'sensor_list_factored': '0', 'all_sensors': 'T',
                           'sensors_per_cycle': '34', 'the8x3_filename': '00940161', 'mission_name': 'STOCK.MI',
                           'total_num_sensors': '34', 'state_bytes_per_cycle': '9',
                           'dbd_label': 'DBD(dinkum_binary_data)file', 'filename_extension': 'ebd',
                           'sensor_list_crc': '6472c02f', 'full_filename': 'dal556-2016-077-0-161',
                           'fileopen_time': 'Tue_Apr__5_20:03:56_2016'}
        self.assertEqual(expected_header, header)

    def test_get_cache_content(self):
        expected_cache_path = os.path.join(*[self.raw_path, 'cache', '6472c02f.cac'])
        with open(self.sample3_file, 'rb') as f:
            self.my_dinkum._parse_header(f)
            cache_list = self.my_dinkum._get_sensor_cache_content(f)

        with open(expected_cache_path, 'r') as f:
            expected_cache = f.readlines()

        cache_str = ''
        for x in cache_list:
            cache_str = cache_str + x
        self.assertEqual(cache_list, expected_cache)

    def test_reorder_files(self):
        path_list1 = ['flight_file.dbd', 'sci_file.ebd']
        path_list2 = ['sci_file.ebd', 'flight_file.dbd']
        reorder_files1 = self.my_dinkum.reorder_files(path_list1)
        reorder_files2 = self.my_dinkum.reorder_files(path_list2)
        self.assertEqual(path_list1, reorder_files1)
        self.assertEqual(path_list1, reorder_files2)

    def test_merge_meta(self):
        flight = {
            'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file_test',
            'encoding_ver': 'encoding_ver',
            'num_ascii_tags': 'num_ascii_tags',
            'filename': 'filename',
            'the8x3_filename': 'the8x3_filename',
            'filename_label': 'filename_label',
            'mission_name': 'mission_name',
            'fileopen_time': 'fileopen_time',
            'sensors_per_cycle': '10',
            'num_label_lines': 'num_label_lines',
            'num_segments': 'num_segments',
            'columns': ['columns0', 'columns1', 'columns2']
        }

        sci = {
            'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file_test',
            'sensors_per_cycle': '10',
            'columns': ['columns0', 'columns1', 'columns2']
        }
        expected = [{'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file'}, {'encoding_ver': 'encoding_ver'},
                    {'num_ascii_tags': 'num_ascii_tags'}, {'filename': 'filename'},
                    {'the8x3_filename': 'the8x3_filename'}, {'filename_extension': 'edba'},
                    {'filename_label': 'filename_label'}, {'mission_name': 'mission_name'},
                    {'fileopen_time': 'fileopen_time'}, {'sensors_per_cycle': 20},
                    {'num_label_lines': 'num_label_lines'}, {'num_segments': 'num_segments'},
                    {'segment_filename_0': 'filename'}, {'columns': 'columns0columns0'}, {'units': 'columns1columns1'},
                    {'number_of_bytes': 'columns2columns2'}]
        try:
            self.my_dinkum._merge_meta(flight, sci)
        except ValueError:
            self.assertTrue(True)

        flight['dbd_label'] = 'DBD_ASC(dinkum_binary_data_ascii)file'

        try:
            self.my_dinkum._merge_meta(flight, sci)
        except ValueError:
            self.assertTrue(True)

        sci['dbd_label'] = 'DBD_ASC(dinkum_binary_data_ascii)file'

        res = self.my_dinkum._merge_meta(flight, sci)
        self.assertEqual(res, expected)

    def test_merge_data(self):
        flight = [
            [0, 1, 0, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 4, 0, 0, 0]
        ]
        sci = [
            [1, 2, 1, 1],
            [1, 5, 1, 1],
            [1, 6, 1, 1]
        ]

        expected1 = [
            [0, 1, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 1, 2, 1, 1],
            [0, 3, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            [0, 4, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 1, 5, 1, 1],
            ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 1, 6, 1, 1]]

        res1 = self.my_dinkum._merge_data(flight, sci, 1, 1, 5, 4)
        self.assertEqual(res1, expected1)

        flight = [
            [0, 1, 0, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 7, 0, 0, 0],
        ]
        sci = [
            [1, 3, 1, 1],
            [1, 5, 1, 1],
            [1, 6, 1, 1]
        ]
        res2 = self.my_dinkum._merge_data(flight, sci, 1, 1, 5, 4)
        print(res2)
        expected2 = [
            [0, 1, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            [0, 3, 0, 0, 0, 1, 3, 1, 1],
            [0, 4, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 1, 5, 1, 1],
            ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 1, 6, 1, 1],
            [0, 7, 0, 0, 0, 'NaN', 'NaN', 'NaN', 'NaN']
        ]
        self.assertEqual(res2, expected2)

    def test_merge_flight_and_sci(self):
        flight_file = {
            'meta': {
                'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file',
                'encoding_ver': 'encoding_ver',
                'num_ascii_tags': 'num_ascii_tags',
                'filename': 'filename',
                'the8x3_filename': 'the8x3_filename',
                'filename_label': 'filename_label',
                'mission_name': 'mission_name',
                'fileopen_time': 'fileopen_time',
                'sensors_per_cycle': '10',
                'num_label_lines': 'num_label_lines',
                'num_segments': 'num_segments',
                'columns': [
                    ['index0', 'index1', 'm_present_time', 'index3'],
                    ['unit0', 'unit1', 'unit2', 'unit3'],
                    ['byte0', 'byte1', 'byte2', 'byte3']
                ]
            },
            'data': [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 3, 0],
                [0, 0, 5, 0],
            ]
        }
        sci_file = {
            'meta': {
                'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file',
                'sensors_per_cycle': '10',
                'columns': [
                    ['index0', 'sci_m_present_time', 'index2', 'index3'],
                    ['unit0', 'unit1', 'unit2', 'unit3'],
                    ['byte0', 'byte1', 'byte2', 'byte3']
                ]
            },
            'data': [
                [1, 3, 1, 1],
                [1, 5, 1, 1],
                [1, 6, 1, 1]
            ]
        }
        res = self.my_dinkum.merge_flight_and_sci(flight_file, sci_file)
        expected = {'data': [
            [0, 0, 1, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            [0, 0, 1, 0, 'NaN', 'NaN', 'NaN', 'NaN'],
            [0, 0, 3, 0, 1, 3, 1, 1],
            [0, 0, 5, 0, 1, 5, 1, 1],
            ['NaN', 'NaN', 'NaN', 'NaN', 1, 6, 1, 1]],
            'meta': [{'dbd_label': 'DBD_ASC(dinkum_binary_data_ascii)file'}, {'encoding_ver': 'encoding_ver'},
                     {'num_ascii_tags': 'num_ascii_tags'}, {'filename': 'filename'},
                     {'the8x3_filename': 'the8x3_filename'}, {'filename_extension': 'edba'},
                     {'filename_label': 'filename_label'}, {'mission_name': 'mission_name'},
                     {'fileopen_time': 'fileopen_time'}, {'sensors_per_cycle': 20},
                     {'num_label_lines': 'num_label_lines'}, {'num_segments': 'num_segments'},
                     {'segment_filename_0': 'filename'}, {
                         'columns': ['index0', 'index1', 'm_present_time', 'index3', 'index0',
                                     'sci_m_present_time', 'index2', 'index3']},
                     {'units': ['unit0', 'unit1', 'unit2', 'unit3', 'unit0', 'unit1', 'unit2', 'unit3']}, {
                         'number_of_bytes': ['byte0', 'byte1', 'byte2', 'byte3', 'byte0', 'byte1', 'byte2',
                                             'byte3']}]}

        self.assertEqual(res, expected)

    def test_get_cache_content_from_file_has_no_cache_content(self):
        with open(self.sample5_file, 'rb') as f:
            header1 = self.my_dinkum._parse_header(f)

            cache = self.my_dinkum._get_cache(f, header1)

        self.assertEqual(None, cache)

    def test_get_cache_content_from_file_with_cache_content(self):
        with open(self.sample3_file, 'rb') as f:
            header1 = self.my_dinkum._parse_header(f)

            cache = self.my_dinkum._get_cache(f, header1)
        expected_cache_path = os.path.join(self.cache_path, '6472c02f.cac')
        with open(expected_cache_path, 'r') as f:
            expected_cache_content = f.readlines()
            expected_cache_value = self.my_dinkum._parse_sensor_cache(expected_cache_content)
        self.assertEqual(expected_cache_value, cache)

    def test_parse_cache(self):
        expected_cache_path = os.path.join(*[self.raw_path, 'cache', '6472c02f.cac'])
        with open(expected_cache_path, 'r') as f:
            expected_cache = f.readlines()

        res = self.my_dinkum._parse_sensor_cache(expected_cache)

        print(res)

    def test_parse_sensor_data_self_generated_cache(self):
        with open(self.sample3_file, 'rb') as f:
            header3 = self.my_dinkum._parse_header(f)
            cache_content = self.my_dinkum._get_sensor_cache_content(f)
            cache_dict = self.my_dinkum._parse_sensor_cache(cache_content)
            res = self.my_dinkum._parse_sensor_data(f, header3, cache_dict)
        print(res)

    def test_parse_sensor_data_with_input_cache(self):
        expected_cache_path = os.path.join(*[self.raw_path, 'cache', '00cda96e.cac'])
        with open(expected_cache_path, 'r') as f:
            cache_content = f.readlines()
        with open(self.sample4_file, 'rb') as f:
            header3 = self.my_dinkum._parse_header(f)
            # cache_content = self.my_dinkum._get_sensor_cache_content(f)
            cache_dict = self.my_dinkum._parse_sensor_cache(cache_content)
            start_time = time.time()
            res = self.my_dinkum._parse_sensor_data(f, header3, cache_dict)
            end_time = time.time()
        print(end_time - start_time)

    def test_merge_dbd_ebd(self):
        cahce_path1 = os.path.join(self.cache_path, '00cda96e.cac')
        cahce_path2 = os.path.join(self.cache_path, '755c391b.cac')

        with open(cahce_path1, 'r') as f:
            cache_content1 = f.readlines()

        with open(cahce_path2, 'r') as f:
            cache_content2 = f.readlines()

        with open(self.sample5_file, 'rb') as f:
            header1 = self.my_dinkum._parse_header(f)

            cache_dict = self.my_dinkum._parse_sensor_cache(cache_content1)
            start_time = time.time()
            res1 = self.my_dinkum._parse_sensor_data(f, header1, cache_dict)
            end_time = time.time()

        with open(self.sample6_file, 'rb') as f:
            header2 = self.my_dinkum._parse_header(f)
            cache_dict = self.my_dinkum._parse_sensor_cache(cache_content2)
            start_time = time.time()
            res2 = self.my_dinkum._parse_sensor_data(f, header2, cache_dict)
            end_time = time.time()

        print(res1, res2)

    def test_decode_with_cache_content_include(self):
        res = self.my_dinkum._decode(self.sample3_file)
        print(res)

    def test_generate_dinkum_ascii(self):
        res = self.my_dinkum._decode(self.sample3_file)
        expected_output_path = os.path.join(self.raw_path, '00940161_EBD.txt')
        with open(expected_output_path, 'r') as f:
            expected_output = f.read()
        print(expected_output)

    def test_generate_dinkum_ascii_header(self):
        expected_header = """dbd_label: DBD_ASC(dinkum_binary_data_ascii)file
encoding_ver: 2
num_ascii_tags: 14
all_sensors: 1
filename: dal556-2016-077-0-161
the8x3_filename: 00940161
filename_extension: ebd
filename_label: dal556-2016-077-0-161-ebd(00940161)
mission_name: STOCK.MI
fileopen_time: Tue_Apr__5_20:03:56_2016
sensors_per_cycle: 34
num_label_lines: 3
num_segments: 1
segment_filename_0: dal556-2016-077-0-161"""
        with open(self.sample3_file, 'rb') as f:
            header = self.my_dinkum._parse_header(f)
        res = generate_ascii_header(header)
        self.assertEqual(expected_header.strip('\n'), res.strip('\n'))

    def test_generate_ascii_meta(self):
        expected_meta = """sci_badd_error sci_badd_finished sci_badd_n_tries_to_connect sci_badd_power_on sci_badd_target_range sci_ctd41cp_is_installed sci_ctd41cp_timestamp sci_dmon_is_installed sci_dmon_msg_byte_count sci_echosndr853_is_installed sci_echosndr853_ping_count sci_m_disk_free sci_m_disk_usage sci_m_free_heap sci_m_min_free_heap sci_m_min_spare_heap sci_m_present_secs_into_mission sci_m_present_time sci_m_science_on sci_m_spare_heap sci_reqd_heartbeat sci_software_ver sci_viper_collect_time sci_viper_collecting sci_viper_error sci_viper_finished sci_viper_target sci_wants_comms sci_wants_surface sci_water_cond sci_water_pressure sci_water_temp sci_x_disk_files_removed sci_x_sent_data_files 
nodim bool nodim bool m bool timestamp bool nodim bool nodim mbytes mbytes bytes bytes bytes sec timestamp bool bytes secs nodim sec bool nodim bool enum bool enum s/m bar degc nodim nodim 
4 1 4 1 4 1 8 1 4 1 4 4 4 4 4 4 4 8 1 4 4 4 4 1 4 1 1 1 1 4 4 4 4 4 """
        # with open(self.sample3_file, 'rb') as f:
        #     header = self.my_dinkum._parse_header(f)
        #     cache = self.my_dinkum._get_cache(f, header)

        dbd = DBD(self.sample3_file, cacheDir=self.cache_path)

        param_names = dbd.parameterNames
        byte_sizes = dbd.byteSizes
        param_units = dbd.parameterUnits

        cache_str = generate_variable_name_unit_and_size(param_names,
                                                        param_units,
                                                        byte_sizes)

        self.assertEqual(expected_meta.strip('\n'), cache_str.strip('\n'))

    def test_generate_ascii_content(self):
        expected_file_path = os.path.join(self.raw_path, '00940161_EBD.txt')
        with open(expected_file_path, 'r') as f:
            expected_file_content = f.read()

        res = DBD(self.sample3_file, cacheDir=self.cache_path)

        ret_str = generate_ascii_content(res)

        # self.assertEqual(expected_file_content, ret_str)

    def test_encode(self):
        self.my_dinkum.load_files(self.raw_path, cache_directory=self.cache_path)
        content = []
        for x in self.my_dinkum.decode():
            content.append(x)
        print(content)

    def test_read_dinkum_ascii(self):
        expected_file_path = os.path.join(self.raw_path, '00940161_EBD.txt')

        res = DBD(self.sample3_file, cacheDir=self.cache_path)

        ret_str = generate_ascii_content(res)

        data = read(StringIO(ret_str))
        print(data)

    def test_read_dinkum_ascii2(self):
        expected_file_path = os.path.join(self.raw_path, 'scotia_2018_316_7_7_dbd.dat')
        # res = self.my_dinkum._decode(expected_file_path)
        #
        # ret_str = generate_ascii_content(res)
        with open(expected_file_path, 'r') as f:
            data = read(f)
        df = data[1]
        TIMESTAMP_SENSORS = ['m_present_time', 'sci_m_present_time']
        for t in TIMESTAMP_SENSORS:
            if t in df.columns:
                df['t'] = df[t]
                break
        df = df.sort_values(by=['t'])
        time_series = df['t']
        time_list = time_series.tolist()
        import collections
        duplicated_value = [item for item, count in collections.Counter(time_list).items() if count > 1]
        print(duplicated_value)
        # print(df)
        print(data)


class TestDinkumInterface(TestCase):
    def setUp(self):
        self.output_path = os.path.join(os.path.dirname(__file__), 'output')
        self.resource_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
        self.raw_path = os.path.join(self.resource_path, 'raw')
        self.sample_file = os.path.join(self.raw_path, '00940161.DBD')
        self.cache_path = os.path.join(self.raw_path, 'cache')

    def test_dinkum_2_dicts(self):
        res = dinkum.dinkum2dicts(self.raw_path, self.cache_path)
        print(res)

    def test_dinkum_2_ascii(self):
        dinkum.dinkum2ascii(self.sample_file, self.cache_path, self.output_path)


class TestDinkumCacheGeneration(TestCase):
    def setUp(self):
        self.output_path = os.path.join(os.path.dirname(__file__), 'output')
        self.resource_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
        self.raw_path = os.path.join(self.resource_path, 'raw')
        self.expected_output = ['4bb51f28.cac', '6472c02f.cac', 'a3381691.cac']

    def test_generate_cache(self):
        dinkum.cache_generator(self.raw_path, self.output_path)
        arr = os.listdir(self.output_path)
        self.assertEqual(sorted(self.expected_output), sorted(arr))

    def tearDown(self) -> None:
        dir_list = os.listdir(self.output_path)
        for file in dir_list:
            path = os.path.join(self.output_path, file)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                rmtree(path)
