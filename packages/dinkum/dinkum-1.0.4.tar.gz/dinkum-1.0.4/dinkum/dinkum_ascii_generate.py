def generate_ascii_file_name(dinkum_data):
    header = dinkum_data['header']
    file_name = "{}.{}".format(header['full_filename'], header["filename_extension"].upper())
    return file_name


def generate_ascii_content(dinkum_data):
    header = dinkum_data['header']
    cache = dinkum_data['cache']
    sensor_data = dinkum_data['data']
    header_str = generate_ascii_header(header)
    meta_str = generate_variable_name_unit_and_size(cache)
    data_str = generate_data_str(sensor_data)
    ret_str = header_str + meta_str + data_str
    return ret_str


def generate_ascii_header(header):
    header_content_list = []
    dbd_label_p = 'dbd_label: {data_type}_ASC(dinkum_binary_data_ascii)file'
    data_type = header['filename_extension']
    dbd_label = dbd_label_p.format(data_type='DBD')
    header_content_list.append(dbd_label)
    header_content_list.append('encoding_ver: 2')
    header_content_list.append('num_ascii_tags: {}'.format(header['num_ascii_tags']))
    header_content_list.append('all_sensors: {}'.format(1 if header['all_sensors'] == 'T' else 0))
    header_content_list.append('filename: {}'.format(header['full_filename']))
    header_content_list.append('the8x3_filename: {}'.format(header['the8x3_filename']))
    header_content_list.append('filename_extension: {}'.format(header['filename_extension']))
    header_content_list.append('filename_label: {}'.format(
        '{file_name}-{file_extension}({the8x3_filename})'.format(file_name=header['full_filename'],
                                                                 file_extension=header['filename_extension'],
                                                                 the8x3_filename=header['the8x3_filename'])))
    header_content_list.append('mission_name: {}'.format(header['mission_name']))
    header_content_list.append('fileopen_time: {}'.format(header['fileopen_time']))
    header_content_list.append('sensors_per_cycle: {}'.format(header['sensors_per_cycle']))
    header_content_list.append('num_label_lines: {}'.format(3))
    header_content_list.append('num_segments: {}'.format(1))
    header_content_list.append('segment_filename_0: {}'.format(header['full_filename']))
    header_str = ''
    for x in header_content_list:
        header_str = header_str + x + '\n'

    return header_str


def generate_variable_name_unit_and_size(caches):
    variable_name = ''
    variable_unit = ''
    variable_size = ''
    for cache in caches:
        variable_name = variable_name + cache['sensor_name'] + ' '
        variable_unit = variable_unit + cache['unit'] + ' '
        variable_size = variable_size + cache['number_of_bytes'] + ' '
    variable_name = variable_name + '\n'
    variable_unit = variable_unit + '\n'
    variable_size = variable_size + '\n'
    ret_str = variable_name + variable_unit + variable_size
    return ret_str


def generate_data_str(sensor_data):
    ret_str = ''
    for d in sensor_data:
        the_str = " ".join(map(str, d))
        ret_str = ret_str + the_str + '\n'
    return ret_str


def generate_merge_content(merged_result):
    ret_str = ''
    meta = merged_result['meta']
    data = merged_result['data']
    s = ' '
    for line in meta:
        key = list(line.keys())
        value = list(line.values())
        if not isinstance(value[0], list):
            ret_str = ret_str + str(key[0]) + ': ' + str(value[0]) + '\n'
        else:
            ret_str = ret_str + s.join(value[0]) + '\n'
    for line in data:
        ret_str = ret_str + s.join(line) + '\n'
    return ret_str
