from model.Unpaywall import Unpaywall


def get_oa_color(doi):
    unpaywall = Unpaywall(doi)
    return unpaywall.oa_color
