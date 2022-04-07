from model.Altmetric import Altmetric
from services import classifier_service, unpaywall_service
from services import table_service

if __name__ == '__main__':

    project = 'test'
    filename = 'test_classification'

    # reading in data from /data/input:
    table = table_service.read_csv_file(project=project, filename=filename)

    # initializing empty results list
    new_rows = []
    for index, row in table.iterrows():

        # important: always set empty fields, if no values can be obtained! otherwise there are problems with the pandas
        # csv export

        # -----------------------------------------------------------------------------------------------
        # for classification: build text to be classified
        abstract = ''
        if type(row['Titel']) is not float:
            abstract = row['Titel']

        if type(row['Abstract']) is not float:
            abstract = abstract + '. ' + row['Abstract']

        # run classifier
        classification = classifier_service.classifiy_text(abstract)

        # add the results to the row
        for i in range(1, 18):
            try:
                row[f'sdg_classifier_{i}'] = classification[i - 1]
            except KeyError:
                row[f'sdg_classifier_{i}'] = ''

        # -----------------------------------------------------------------------------------------------
        # for Unpaywall:
        if type(row['DOI'] is not float):
            try:
                row['oa-color'] = unpaywall_service.get_oa_color(row['DOI'])
            except KeyError:
                row['oa-color'] = ''
            except AttributeError:
                row['oa-color'] = ''

        # -----------------------------------------------------------------------------------------------
        # for altmetric:
        if type(row['DOI'] is not float):
            altmetric = Altmetric(row['DOI'])
            try:
                row['altmetric-policies-count'] = altmetric.cited_by_policies_count
                row['altmetric-posts-count'] = altmetric.cited_by_posts_count
                row['altmetric-feeds-count'] = altmetric.cited_by_feeds_count
                row['altmetric-tweeters-count'] = altmetric.cited_by_tweeters_count
            except KeyError:
                row['altmetric-policies-count'] = ''
                row['altmetric-posts-count'] = ''
                row['altmetric-feeds-count'] = ''
                row['altmetric-tweeters-count'] = ''
            except AttributeError:
                row['altmetric-policies-count'] = ''
                row['altmetric-posts-count'] = ''
                row['altmetric-feeds-count'] = ''
                row['altmetric-tweeters-count'] = ''
        # add row to results list
        new_rows.append(row)

    # write results list to csv file
    table_service.write_csv_file(project=project, filename=filename, rows=new_rows)