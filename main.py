import pandas as pd
import time
import sys
from services import unpaywall_service, altmetric_service, scite_service, table_service
from multiprocessing import Process


project = str(sys.argv[1])
filename = str(sys.argv[2])
which_apis = str(sys.argv[3])

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


if __name__ == '__main__':

    # reading in data from /data/input:
    table = table_service.read_csv_file(project=project, filename=filename)

    # process csv in chunks
    n = 10000
    start = 0  # start chunk (adjust in case of interruptions)

    for i in range(start*n, len(table), n):
        table_chunk = table.iloc[i:i+n, :]
        dois = list(table_chunk['DOI'][~pd.isna(table_chunk['DOI'])].apply(parse_id))
        table_nodoi = table_chunk.copy()[pd.isna(table_chunk['DOI'])]
        isbns = list(table_nodoi['ISBN'][~pd.isna(table_nodoi['ISBN'])].apply(parse_id))

        ids = {'doi': dois, 'isbn': isbns}

        all_rows = {}
        jobs = []
        t0 = time.time()
        for api in apis:
            api_rows = []
            all_rows[api] = api_rows
            service = eval(f'{api}_service')
            p = Process(target=getattr(service, f'fast_{api}')(ids, api_rows))
            jobs.append(p)
            p.start()
        # wait for processes to finish
        for job in jobs:
            job.join()
        t1 = time.time()
        print(f'it took {t1-t0} seconds to process {len(dois)} DOIs and {len(isbns)} ISBNs using the APIs')
        # save temp tables
        for api in all_rows:
            table_service.write_csv_file(project=f'{project}/{filename}',
                                         filename=filename + f'_{api}_{i}', rows=all_rows[api])

    # append temp tables
    tables = {}
    for api in apis:
        tables[api] = pd.DataFrame()
        for i in range(start * n, len(table), n):
            # dataframes are allowed to be empty
            try:
                temp_table_upw = pd.read_csv(f'data/output/{project}/{filename}/{filename}_{api}_{i}.csv')
                tables[api] = pd.concat([tables[api], temp_table_upw])
            except pd.errors.EmptyDataError:
                pass
        # write results list to csv file
        tables[api].to_csv(f'data/output/{project}/{filename}/{filename}_{api}.csv', index=False)

