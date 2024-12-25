import argparse
import configparser
import os

config = configparser.ConfigParser()
config.read('default.ini')
defaults = config['DEFAULT']

defaults['DataSchema'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), defaults['DataSchema'])

parser = argparse.ArgumentParser(
    prog='Python Basics Capstone Project by JPiwo',
    description='Universal console utility that generates data in JSON format. '
                'Designed to help checking correctness of data transformations and validations on pipelines.',
    epilog="That's all! Thank you"
)

parser.add_argument('--path_to_save_files', type=str, default=defaults['PathToSaveFiles'],
                    help='Where all the files need to be save. Default: project folder')

parser.add_argument('--files_count', type=int, default=defaults['FilesCount'],
                    help='How many json files to generate. Default: 4 files')

parser.add_argument('--file_name', type=str, default=defaults['FileName'],
                    help='Base file name. If there is no prefix, the final file name will be '
                         'file_name.json. With prefix full file name will be file_name_file_prefix.json')

parser.add_argument('--file_prefix', type=str, choices=['count', 'random', 'uuid'],
                    default= defaults['FilePrefix'],
                    help='What prefix for file name to use if more than 1 file needs to be generated.'
                         'Default: count')

parser.add_argument('--data_schema', type=str, default=defaults['DataSchema'],
                    help='It is a string with json schema. It could be loaded in two ways: '
                         '1) with path to json file with schema'
                         '2) with schema entered to command line'
                         'Default: schema from file schema_example.json included in this project')

parser.add_argument('--data_lines', type=int, default=defaults['DataLines'],
                    help='Count of data lines for each file. Default value: 100. Does not apply if files'
                         'number is set to 0.')

parser.add_argument('-c', '--clear_path', action='store_true',
                    help='If this flag is on, before the script starts creating new data files,'
                         'all files in path_to_save_files that match file_name will be deleted')

parser.add_argument('-m', '--multiprocessing', type=int, default=defaults['Multiprocessing'],
                    help='The number of processes used to create files. Divides the "files_count" value'
                         'equally and starts N processes to create an equal number of files in parallel.'
                         'Optional argument. Default value: 2')

args = parser.parse_args()