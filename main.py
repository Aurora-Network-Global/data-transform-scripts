import pandas as pd
import os
import time
import sys
from model.Altmetric2 import Altmetric
from model.Unpaywall import Unpaywall
from services import classifier_service, ubo_service
from services import table_service
from multiprocessing import Process
from fast_requests import fast_get

import config
email = os.environ.get("UNPAYWALL_EMAIL")
api_key = os.environ.get("ALTMETRIC_API_KEY")

project = 'dashboard'
filename = str(sys.argv[1])
classification = False


def parse_id(identifier):
    return identifier.split('|')[0].split(';')[0].strip().lower()


def fast_unpaywall(dois, unpaywall_rows):
    reqs = [{'id': doi,
             'url': f'https://api.unpaywall.org/my/request/{doi}',
             'params': {'email': email}}
            for doi in dois]
    rate_limit = (10, 1)
    (results, message), elapsed = fast_get(reqs, accept_codes=[200, 404], max_retry=3, rate_limit=rate_limit)
    # fill rows
    for doi in results:
        unpaywall_row = {'DOI': doi}
        oa_data = Unpaywall(results[doi])
        unpaywall_row['Open access status'] = oa_data.is_oa
        unpaywall_row['Open access color'] = oa_data.oa_color
        unpaywall_row['Open Access URL'] = oa_data.free_fulltext_url
        unpaywall_rows.append(unpaywall_row)


def fast_altmetric(identifiers, altmetric_rows):
    reqs = [{'id': id_value,
             'url': f'https://api.altmetric.com/v1/fetch/{id_type}/{id_value}',
             'params': {'key': api_key}}
            for id_type in identifiers for id_value in identifiers[id_type]]
    rate_limit = (10, 1)
    (results, message), elapsed = fast_get(reqs, accept_codes=[200, 404], max_retry=3, rate_limit=rate_limit)
    # fill rows
    for id_value in results:
        altmetric = Altmetric(results[id_value])
        # process mentions
        mentions = altmetric.mentions
        if mentions is not None:
            for mention_type in mentions:
                if mention_type == 'policy':
                    for m in mentions[mention_type]:
                        altmetric_row = {'ID': id_value,
                                         'Mention type': mention_type,
                                         'Mention title': m.get('title', ''),
                                         'Mention author': m.get('source', {}).get('name', ''),
                                         'Mention URL': m.get('url', '')
                                         }
                        altmetric_rows.append(altmetric_row)
                elif mention_type == 'news':
                    for m in mentions[mention_type]:
                        altmetric_row = {'ID': id_value,
                                         'Mention type': mention_type,
                                         'Mention title': m.get('title', ''),
                                         'Mention author': m.get('author', {}).get('name', ''),
                                         'Mention URL': m.get('url', '')
                                         }
                        altmetric_rows.append(altmetric_row)
                elif mention_type == 'patent':
                    for m in mentions[mention_type]:
                        altmetric_row = {'ID': id_value,
                                         'Mention type': mention_type,
                                         'Mention title': m.get('title', ''),
                                         'Mention author': m.get('jurisdiction', ''),
                                         'Mention URL': m.get('url', '')
                                         }
                        altmetric_rows.append(altmetric_row)


if __name__ == '__main__':

    # initializing empty results list
    sdg_rows = []
    unpaywall_rows = []
    altmetric_rows = []

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

        jobs = []
        t0 = time.time()
        p1 = Process(target=fast_unpaywall(dois, unpaywall_rows))
        jobs.append(p1)
        p1.start()
        p2 = Process(target=fast_altmetric({'doi': dois, 'isbn': isbns}, altmetric_rows))
        jobs.append(p2)
        p2.start()
        # wait for processes to finish
        for job in jobs:
            job.join()
        t1 = time.time()
        print(f'it took {t1-t0} seconds to process {len(dois)} DOIs and {len(isbns)} ISBNs using the APIs')
        # save temp tables
        table_service.write_csv_file(project=f'{project}/{filename}', filename=filename + f'_unpaywall_{i}', rows=unpaywall_rows)
        table_service.write_csv_file(project=f'{project}/{filename}', filename=filename + f'_altmetric_{i}', rows=altmetric_rows)
        # reset the lists
        unpaywall_rows = []
        altmetric_rows = []

    # SDG classification (not in chunks)
    if classification:
        for index, row in table.iterrows():
                sdg_row = row
                if type(sdg_row['DOI']) is not float:
                    sdg_row['abstract'] = ubo_service.get_abstract(sdg_row['DOI'])
                # -----------------------------------------------------------------------------------------------
                # for classification: build text to be classified
                abstract = ''
                if type(sdg_row['Titel']) is not float:
                    abstract = sdg_row['Titel']

                if type(sdg_row['Abstract']) is not float:
                    abstract = abstract + '. ' + sdg_row['Abstract']

                # run classifier
                classification = classifier_service.classifiy_text(abstract)

                # add the results to the row
                for i in range(1, 18):
                    try:
                        sdg_row[f'sdg_classifier_{i}'] = classification[i - 1]
                    except KeyError:
                        sdg_row[f'sdg_classifier_{i}'] = ''

                sdg_rows.append(sdg_row)

    # append temp tables
    table_upw = pd.DataFrame()
    table_alt = pd.DataFrame()
    for i in range(start * n, len(table), n):
        # dataframes are allowed to be empty
        try:
            temp_table_upw = pd.read_csv(f'data/output/{project}/{filename}/{filename}_unpaywall_{i}.csv')
            table_upw = pd.concat([table_upw, temp_table_upw])
        except pd.errors.EmptyDataError:
            pass
        try:
            temp_table_alt = pd.read_csv(f'data/output/{project}/{filename}/{filename}_altmetric_{i}.csv')
            table_alt = pd.concat([table_alt, temp_table_alt])
        except pd.errors.EmptyDataError:
            pass

    # write results list to csv file
    table_upw.to_csv(f'data/output/{project}/{filename}/{filename + "_unpaywall"}.csv', index=False)
    table_alt.to_csv(f'data/output/{project}/{filename}/{filename + "_altmetric"}.csv', index=False)
