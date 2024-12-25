import os
import shutil
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from ..main import main_function

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testing_files')


class Arg():
    def __init__(self, path, prefix, threads):
        self.path_to_save_files = path
        self.files_count = 4
        self.file_name = 'test_file'
        self.file_prefix = prefix
        self.data_schema = '{"name":"str:Test"}'
        self.data_lines = 10
        self.clear_path = True
        self.multiprocessing = threads


# Also checks if files are saved to the given path
def test_multiprocessing_files_count():

    if not os.path.exists(path):
        os.makedirs(path)

    args1 = Arg(path, 'count', 2)
    main_function(args1)
    created_files = os.listdir(args1.path_to_save_files)

    assert len(created_files) == args1.files_count, f"Created {len(created_files)} files instead of {args1.files_count}"

    shutil.rmtree(args1.path_to_save_files)


# My test
def test_file_lines():
    if not os.path.exists(path):
        os.makedirs(path)

    args2 = Arg(path, 'count', 1)
    main_function(args2)
    created_files = os.listdir(args2.path_to_save_files)

    for filename in created_files:
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        assert len(lines) == args2.data_lines, f'File {filename} has {len(lines)} lines instead of {args2.data_lines}'

    shutil.rmtree(args2.path_to_save_files)


def test_clear_path_true():
    if not os.path.exists(path):
        os.makedirs(path)

    args3 = Arg(path, 'uuid', 2)
    main_function(args3)

    args4 = Arg(path, 'count', 2)
    main_function(args4)

    correct_names = ['test_file_0.json', 'test_file_1.json',
                     'test_file_2.json', 'test_file_3.json']

    created_files = os.listdir(args4.path_to_save_files)
    for filename in created_files:
        assert filename in correct_names, f'File: {filename} should have been removed'

    shutil.rmtree(args4.path_to_save_files)