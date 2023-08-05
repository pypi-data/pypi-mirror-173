import pandas as pd
from collections import OrderedDict
import logging


def read(ascii_file_io_string):
    headers = None
    metadata = OrderedDict()
    af = ascii_file_io_string
    for li, al in enumerate(af):
        if 'm_present_time' in al or 'sci_m_present_time' in al:
            headers = al.strip().split(' ')
        elif headers is not None:
            data_start = li + 2  # Skip units line and the interger row after that
            break
        else:
            title, value = al.split(':', 1)
            metadata[title.strip()] = value.strip()

    df = pd.read_csv(
        af,
        index_col=False,
        skiprows=1,
        header=None,
        names=headers,
        sep=' ',
        skip_blank_lines=True,
    )
    return metadata, df


def parse_dbd2asc_result(dbd_asc_name, column_output=None):
        # find the end of the metadata preamble
        # This is not neat, but it is a way to keep from choking on large (6GB) ascii files from glider missions.
        fread_stage = 'header'
        meta = {'filename_list': [], 'columns': []}
        prim_header = []
        outcol_indices = []  # List of indices where we find the corresponding data to column_output
        dstruct = []
        colcount = 0
        with open(dbd_asc_name, 'r') as fp:
            logging.info('input file %s opened.' % dbd_asc_name)
            for line in fp:
                line = line.strip('\n').rstrip()
                if fread_stage == 'header' and "segment_filename" not in line:
                    prim_header.append(line)  # add pre-segment_filename lines to the meta header.
                elif fread_stage == 'header':
                    for prim_row in prim_header:
                        meta[prim_row.split(':', 1)[0]] = prim_row.split(':', 1)[1].strip()
                    fread_stage = 'segments'
                if fread_stage == 'segments' and "segment_filename" in line:
                    meta['filename_list'].append(line.split(":")[1].strip())
                elif fread_stage == 'segments':
                    fread_stage = 'data_header'
                if fread_stage == 'data_header' and colcount < 3:
                    meta['columns'].append(line.split(' '))
                    colcount += 1
                elif fread_stage == 'data_header':  # close out the meta columns
                    if len(meta['columns']) == 3:
                        sensors, units, bits = tuple(meta['columns'])
                    else:
                        raise ValueError('Wrong number of data columns {}, exiting.\n{}'
                                         .format(len(meta['columns']), meta['columns']))
                    if column_output:
                        for col in column_output:
                            outcol_indices.append(sensors.index(col))
                        if any([x == -1 for x in outcol_indices]):
                            logging.error('could not find columns specified')
                            return -1
                    fread_stage = 'data'
                if fread_stage == 'data':
                    if column_output:  # If the user's specified what columns they're interested in, and we found them all
                        dline = line.split(' ')
                        dstruct.append([dline[i] for i in outcol_indices])
                    else:
                        dstruct.append(line.split(' '))
        return {'data': dstruct, 'meta': meta}
