from model.Altmetric2 import Altmetric
from model.Unpaywall import Unpaywall
from services import classifier_service, ubo_service
from services import table_service


if __name__ == '__main__':

    project = 'test'
    filename = 'aberdeen_subset'
    classification = False

    # reading in data from /data/input:
    table = table_service.read_csv_file(project=project, filename=filename)

    # initializing empty results list
    sdg_rows = []
    unpaywall_rows = []
    altmetric_rows = []
    for index, row in table.iterrows():
        if classification:
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

        # -----------------------------------------------------------------------------------------------
        # for unpaywall:
        if type(row['DOI']) is not float:
            unpaywall_row = {'DOI': row['DOI']}
            oa_data = Unpaywall(row['DOI'])
            unpaywall_row['Open access status'] = oa_data.is_oa
            unpaywall_row['Open access color'] = oa_data.oa_color
            unpaywall_row['Open Access URL'] = oa_data.free_fulltext_url

            unpaywall_rows.append(unpaywall_row)

        # -----------------------------------------------------------------------------------------------
        # for altmetric:
        if type(row['DOI']) is not float:
            altmetric = Altmetric(row['DOI'])
            # process mentions
            mentions = altmetric.mentions
            if mentions is not None:
                for mention_type in mentions:
                    if mention_type == 'policy':
                        for m in mentions[mention_type]:
                            altmetric_row = {'DOI': row['DOI'],
                                             'Mention type': mention_type,
                                             'Mention title': m.get('title', ''),
                                             'Mention author': m.get('source', {}).get('name', ''),
                                             'Mention URL': m.get('url', '')
                                             }
                            altmetric_rows.append(altmetric_row)
                    elif mention_type == 'news':
                        for m in mentions[mention_type]:
                            altmetric_row = {'DOI': row['DOI'],
                                             'Mention type': mention_type,
                                             'Mention title': m.get('title', ''),
                                             'Mention author': m.get('author', {}).get('name', ''),
                                             'Mention URL': m.get('url', '')
                                             }
                            altmetric_rows.append(altmetric_row)

    # write results list to csv file
    table_service.write_csv_file(project=project, filename=filename+'_unpaywall', rows=unpaywall_rows)
    table_service.write_csv_file(project=project, filename=filename+'_altmetric', rows=altmetric_rows)
