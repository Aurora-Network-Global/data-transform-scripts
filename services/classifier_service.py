import json

import requests

sdg_classifier_url = "http://localhost:5000/run_models"


def classifiy_text(text):
    payload = {}
    payload["abstracts"] = [text]
    # ausführen des Aufrufes der Universitätsbibliographie-Suche:
    response = requests.post(url=sdg_classifier_url, json=json.dumps(payload))

    # Die Kodierung der Antwort auf UTF-8 festlegen
    response.encoding = 'utf-8'
    print(response.text)
    # Prüfen, ob die Abfrage erfolgreich war (Status-Code ist dann 200)
    if response.status_code == 200:
        return json.loads(response.text)[0]
    else:
        return []
