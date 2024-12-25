import logging
import os
import json

class Validator:
    def __init__(self, path, count, name, prefix, schema, lines, clear, threads):
        self.path_to_save_files = self.path_to_save_files_validation(path)
        self.files_count = self.files_count_validation(count)
        self.file_name = name
        self.file_prefix = prefix
        self.data_schema = self.data_schema_validation(schema)
        self.data_lines = self.data_lines_validation(lines)
        self.clear_path = clear
        self.multiprocessing = self.multiprocessing_validation(threads)

    def path_to_save_files_validation(self, path: str):
        if path == '.˜':
            return os.getcwd()
        if os.path.exists(path):
            if os.path.isdir(path):
                logging.info('Path to save files is correct')
                return path
            else:
                logging.error('Path to save files is not a directory')
                exit(1)
        else:
            logging.error('Path to save files does not exist')
            exit(1)

    def files_count_validation(self, count: int):
        if count < 0:
            logging.error('Number of files to generate is a negative number')
            exit(1)
        else:
            logging.info("Number of files to generate is valid")
            return count

    def data_schema_validation(self, schema):
        if schema.endswith('.json'):
            path = schema
            logging.info('Schema was declared by a file')
            if os.path.exists(path):
                with open(path) as f:
                    schema = f.read()
            else:
                logging.error('Json schema in file is not valid')
                exit(1)
        try:
            schema = json.loads(schema)
        except ValueError as e:
            logging.error('Data schema is not correct json schema')
            exit(1)

        logging.info('Data schema is correct json schema')
        return schema

    def data_lines_validation(self, lines: int):
        if lines < 1:
            logging.error('Number of lines for each file is lower than 1')
            exit(1)
        else:
            logging.info('Number of lines for each file is valid')
            return lines


    def multiprocessing_validation(self, threads: int):
        if threads <= 0:
            logging.error('Number of processes is negative or equal to 0')
            exit(1)
        elif threads > os.cpu_count():
            logging.info('Number of processes was replaced by os.cpu_count() values')
            return os.cpu_count()
        else:
            return threads