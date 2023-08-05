import os

DINKIM_FILE_EXTENSIONS = ['.dbd', '.ebd', '.sbd', '.tbd', '.nbd']
FLIGHT_FILE_EXTENSIONS = ['.dbd', '.sbd', '.mbd']
SCIENCE_FILE_EXTENSIONS = ['.ebd', '.tbd', '.nbd']
DINKUM_MATCH = {'.DBD': '.EBD', '.SBD': '.TBD', '.MBD': '.NBD',
                '.EBD': '.DBD', '.TBD': '.SBD', '.NBD': '.MBD'}


def find_all_dinkum_files(input_directory):
    """Find all files in a directory with dinkim file extensions"""
    all_file_names = os.listdir(input_directory)
    dinkum_names = []
    for file in all_file_names:
        if is_dinkum_name(file):
            dinkum_names.append(os.path.join(input_directory, file))

    return dinkum_names


def is_dinkum_name(file_name):
    _, extension = os.path.splitext(file_name.lower())
    return extension in DINKIM_FILE_EXTENSIONS


def is_flight_file(file_name):
    _, extension = os.path.splitext(file_name.lower())
    return extension in FLIGHT_FILE_EXTENSIONS


def is_science_file(file_name):
    _, extension = os.path.splitext(file_name.lower())
    return extension in SCIENCE_FILE_EXTENSIONS