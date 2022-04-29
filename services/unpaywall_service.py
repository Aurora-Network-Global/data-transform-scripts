from model.Unpaywall import Unpaywall
from fast_requests import fast_get
import config


def fast_unpaywall(ids, unpaywall_rows):
    # we can work with dois
    usable_ids = {id_type: ids.get(id_type, []) for id_type in ['doi']}
    for id_type in usable_ids:
        if len(usable_ids[id_type]) == 0:
            print(f'unpaywall: no {id_type}')
    reqs = [{'id': id_value,
             'url': f'https://api.unpaywall.org/my/request/{id_value}',
             'params': {'email': config.EMAIL}}
            for id_type in usable_ids for id_value in usable_ids[id_type]]
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
