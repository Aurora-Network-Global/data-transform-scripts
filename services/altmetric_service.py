from model.Altmetric2 import Altmetric
from fast_requests import fast_get
import config


def fast_altmetric(ids, altmetric_rows):
    # we can work with dois and isbns
    usable_ids = {id_type: ids.get(id_type, []) for id_type in ['doi', 'isbn']}
    for id_type in usable_ids:
        if len(usable_ids[id_type]) == 0:
            print(f'altmetric: no {id_type}')
    reqs = [{'id': id_value,
             'url': f'https://api.altmetric.com/v1/fetch/{id_type}/{id_value}',
             'params': {'key': config.ALTMETRIC_API_KEY}}
            for id_type in usable_ids for id_value in usable_ids[id_type]]
    rate_limit = (5, 1)
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
