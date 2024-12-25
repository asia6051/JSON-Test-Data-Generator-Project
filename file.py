import logging
import random
import uuid
import time
import ast
import json


class File:
    def __init__(self, filename, schema, lines):
        self.timestamp_warning_flag = 1 # prevents covering all console with one warning
        self.filename = filename
        self.schema = schema
        self.lines = lines
        self.result = self.generate_file_content()


    def int_value(self, value: str):
        if value == 'int:':
            return None
        elif value == 'int:rand':
            return random.randint(0, 10000)
        elif value.startswith('int:rand('):
            # find brackets and coma
            start_index = value.index('(') + 1
            comma_index = value.index(',')
            end_index = value.index(')')

            # cut fragment of string
            lower_bound_str = value[start_index:comma_index]
            upper_bound_str = value[comma_index + 1:end_index]

            # convert bound to int
            lower_bound = int(lower_bound_str)
            upper_bound = int(upper_bound_str)

            return random.randint(lower_bound, upper_bound)
        else:
            colon_index = value.index(':')
            element = value[colon_index + 1:]
            try:
                result = int(element)
            except ValueError:
                logging.error(f'{element} could not be convert to int')
                exit(1)
            return result

    def str_value(self, value: str):
        if value == 'str:':
            return ""
        elif value == 'str:rand':
            return str(uuid.uuid4())
        elif value.startswith('str:rand('):
            logging.error('str:rand type is not allowed')
            exit(1)
        else:
            colon_index = value.index(':')
            element = value[colon_index + 1:]
            try:
                result = str(element)
            except ValueError:
                logging.error(f'{element} could not be convert to int')
                exit(1)
            return result

    def generate_values(self):
        my_values = list()

        for value in self.schema.values():
            value = str(value)
            if value.startswith('int:'):
                my_values.append(self.int_value(value))

            elif value.startswith('str:'):
                my_values.append(self.str_value(value))

            elif value.startswith('timestamp:'):
                if value != 'timestamp:' and self.timestamp_warning_flag:
                    logging.warning('timestamp does not support any values')
                    self.timestamp_warning_flag = 0
                my_values.append(time.time())

            elif value.startswith('['):
                choices = ast.literal_eval(value) #ast literal eval
                my_values.append(random.choice(choices))

            else:
                logging.error(f'Not recognized type in schema: {value}')

        logging.info('New values are generated')
        return my_values

    def generate_file_content(self):
        json_lines = []

        for _ in range(self.lines):
            values = self.generate_values()
            result = {}
            for i, (key, _) in enumerate(self.schema.items()):
                result[key] = values[i]

            json_lines.append(json.dumps(result))

        return '\n'.join(json_lines)