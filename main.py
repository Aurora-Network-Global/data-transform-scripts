from services import classifier_service
from services import table_service

if __name__ == '__main__':

    project = 'test'
    filename = 'test_classification'

    # einlesen einer test.xlsx-Datei aus /data/input:
    table = table_service.read_csv_file(project=project, filename=filename)
    # Durchlauf durch die Zeilen und Ausgabe der Spalte 'DOI'
    new_rows = []
    for index, row in table.iterrows():

        abstract = ''
        if type(row['Titel']) is not float:
            abstract = row['Titel']

        if type(row['Abstract']) is not float:
            abstract = abstract + '. ' + row['Abstract']

        classification = classifier_service.classifiy_text(abstract)
        # Prüfen, ob die Abfrage erfolgreich war (Status-Code ist dann 200)
        for i in range(1, 18):
            try:
                row[f'sdg_classifier_{i}'] = classification[i-1]
            except KeyError:
                row[f'sdg_classifier_{i}'] = ''
        new_rows.append(row)
    table_service.write_csv_file(project=project, filename=filename, rows=new_rows)