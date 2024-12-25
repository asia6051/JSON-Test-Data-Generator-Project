import os
import logging
import random
import uuid


def clear_path(my_name, my_path):
    for filename in os.listdir(my_path):
        if filename.startswith(my_name):
            file_path = os.path.join(my_path, filename)
            try:
                os.remove(file_path)
                logging.info(f'{filename} was deleted')
            except Exception as e:
                logging.error(f'Problem with {filename} deletion: {e}')
    logging.info('Path was cleared')


def names(my_prefixes, file_name):
    files_names = list()
    for prefix in my_prefixes:
        files_names.append(file_name + '_' + str(prefix) + '.json')
    logging.info('File names are generated')
    return files_names


def prefixes(files_count, prefix):
    if prefix == 'count':
        logging.info('Generating prefixes with count')
        return list(range(files_count))

    elif prefix == 'random':
        logging.info('Generating prefixes with random')
        return random.sample(range(files_count * 3), files_count)

    elif prefix == 'uuid':
        uuids = set()

        while len(uuids) < files_count:
            new_uuid = uuid.uuid4()
            uuids.add(new_uuid)

        logging.info('Generating prefixes with UUID')
        return list(uuids)