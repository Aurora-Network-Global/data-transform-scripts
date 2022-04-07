import os

import pandas as pd


# Hier definiere ich ein paar Standard-Verzeichnisse für input/output-Dateien. Alle
input_excel_dateien = 'data/input/{}.xlsx'
output_folder = 'data/output/'

# Hier definieren wir auftretende Spaltennamen und deren Typ. object steht dabei für Text. Schreibweise und Groß-Klein-Schreibung sind wichtig.
D_TYPES = {'Autoren': object,
           'DOI': object
           }


def read_excel_table(project, filename):
    path_to_file = f'data/input/{project}/{filename}.xlsx'
    table = pd.read_excel(path_to_file, dtype=D_TYPES)
    return table


def write_excel_table(project, filename, rows, temp=False):
    if temp:
        branch = 'test'
    else:
        branch = 'output'
    if not os.path.exists(f'/data/{branch}/{project}'):
        os.makedirs(f'/data/{branch}/{project}')
    output_file = f'/data/{branch}/{project}/{filename}.xlsx'
    new_table = pd.DataFrame(rows)
    new_table.to_excel(output_file)
    return new_table


def read_csv_file(project, filename):
    path_to_file = f'data/input/{project}/{filename}.csv'
    table = pd.read_csv(path_to_file, dtype=D_TYPES)
    return table


def write_csv_file(project, filename, rows, temp=False):
    if temp:
        branch = 'test'
    else:
        branch = 'output'
    if not os.path.exists(f'/data/{branch}/{project}'):
        os.makedirs(f'/data/{branch}/{project}')
    path_to_file = f'data/input/{project}/{filename}.csv'
    new_table = pd.DataFrame(rows)
    new_table.to_csv(path_to_file, sep=',')
