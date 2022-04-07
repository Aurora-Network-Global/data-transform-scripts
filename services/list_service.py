import os

import logging


def save_identifier_list(project, identifier_list, filename):
    path_folder = 'data/output/{}'.format(project)
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    path_to_file = f'data/output/{project}/{filename}.txt'
    with open(path_to_file, 'w', encoding='utf-8') as list_file:
        for identifier in identifier_list:
            list_file.write(identifier + '\n')
        list_file.close()


def load_identifier_list_of_type(project, filename):
    path_to_file = f'/data/input/{project}/{filename}.txt'
    logging.info(f'loading file {path_to_file}')
    with open(path_to_file, encoding='utf-8') as f:
        ids = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in ids]
