import logging
import os
from multiprocessing import Pool

from config import args
from validator import Validator
from file import File
from files_names_manager import clear_path, names, prefixes


def create_file(settings, filename):
    file = File(filename, settings.data_schema, settings.data_lines)
    file_path = os.path.join(settings.path_to_save_files, file.filename)

    with open(file_path, 'w') as new_file:
        new_file.write(file.result)
    return file.filename


def main_function(my_args):
    logging.getLogger().setLevel(logging.INFO)

    settings = Validator(my_args.path_to_save_files,
                         my_args.files_count,
                         my_args.file_name,
                         my_args.file_prefix,
                         my_args.data_schema,
                         my_args.data_lines,
                         my_args.clear_path,
                         my_args.multiprocessing)

    if settings.clear_path and settings.files_count > 0:
        clear_path(settings.file_name, settings.path_to_save_files)

    if settings.files_count == 0:
        output = File('', settings.data_schema, settings.data_lines)
        print(output.result)
        logging.info('Files count = 0 -> result printed on console')
        exit(0)

    file_names = names(prefixes(settings.files_count, settings.file_prefix), settings.file_name)

    with Pool(settings.multiprocessing) as pool:
        pool.starmap(create_file, [(settings, filename) for filename in file_names])


if __name__ == '__main__':
    main_function(args)