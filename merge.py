import pandas as pd
import sys
import glob


project = str(sys.argv[1])
which_apis = str(sys.argv[2])

apis = []
for i in which_apis:
    if i == '1':
        apis.append('unpaywall')
    if i == '2':
        apis.append('altmetric')
    if i == '3':
        apis.append('scite')


def parse_id(identifier):
    return identifier.split('|')[0].split(';')[0].strip().lower()


# read and combine publication tables
path = f'data/input/{project}'
pubs = pd.DataFrame()
for filename in glob.glob(f'{path}/*.csv'):
    pub = pd.read_csv(filename)
    pub['Uni'] = filename.split('.')[0].split('\\')[-1]
    pubs = pd.concat([pubs, pub])
# merge identifiers: ISBN only if no DOI
pubs['ID'] = pubs['DOI'].fillna(pubs['ISBN'])
# parse
pubs['ID'] = pubs['ID'].apply(lambda x: parse_id(x) if not pd.isna(x) else x)
# save
pubs.to_csv(f'data/output/{project}/publications.csv', index=False)

# combine api tables
for api in apis:
    table = pd.DataFrame()
    for uni in pubs['Uni'].unique():
            aux = pd.read_csv(f'data/output/{project}/{uni}/{uni}_{api}.csv')
            # remove duplicates
            if not table.empty:
                id_column = aux.columns[0]
                table = table[~table[id_column].isin(aux[id_column])]
            table = pd.concat([table, aux])
    # save
    table.to_csv(f'data/output/{project}/{api}.csv', index=False)
    # create a counts table for altmetric mentions
    if api == 'altmetric':
        counts = table.copy()
        counts = counts.groupby(['ID', 'Mention type'], as_index=True).count()
        counts.to_csv(f'data/output/{project}/altmetric_counts.csv', index=True)

