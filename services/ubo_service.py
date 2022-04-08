from xml import etree

import requests

ubo_base_dir = 'https://bibliographie.ub.uni-due.de/servlets/solr/select?q=%28id_doi%3A"{}"AND+status%3A%22confirmed%22%29&fl=*&sort=year+desc&rows=10&version=4.5&mask=search.xed&XSL.Style=xml'


def get_abstract(doi):
    url = ubo_base_dir.format(doi)
    # ausführen des Aufrufes der Universitätsbibliographie-Suche:
    response = requests.get(url=url, headers={'Accept': 'application/xml'})
    # Die Kodierung der Antwort auf UTF-8 festlegen
    response.encoding = 'utf-8'

    # Prüfen, ob die Abfrage erfolgreich war (Status-Code ist dann 200)
    if response.status_code == 200:
        mycore = etree.fromstring(response.text)
        mycore.get


