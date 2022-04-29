from model.Scite import Scite
from fast_requests import fast_get
import config


def fast_scite(ids, scite_rows):
    # we can work with dois and isbns
    usable_ids = {id_type: ids.get(id_type, []) for id_type in ['doi', 'isbn']}
    for id_type in usable_ids:
        if len(usable_ids[id_type]) == 0:
            print(f'scite: no {id_type}')
    reqs = [{'id': id_value,
             'url': f'https://api.scite.ai/tallies/{id_value}',
             'params': {'email': config.EMAIL}}
            for id_type in usable_ids for id_value in usable_ids[id_type]]
    rate_limit = (5, 1)
    (results, message), elapsed = fast_get(reqs, accept_codes=[200, 404], max_retry=3, rate_limit=rate_limit)
    # fill rows
    for doi in results:
        scite_row = {'ID': doi}
        scite = Scite(results[doi])
        scite_row['Total'] = scite.total
        scite_row['Supporting'] = scite.supporting
        scite_row['Contradicting'] = scite.contradicting
        scite_row['Mentioning'] = scite.mentioning
        scite_row['Unclassified'] = scite.unclassified
        scite_row['Citing'] = scite.citingPublications
        scite_rows.append(scite_row)
