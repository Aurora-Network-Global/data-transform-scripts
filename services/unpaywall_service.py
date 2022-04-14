from model.Unpaywall import Unpaywall


def get_oa(doi):
    unpaywall = Unpaywall(doi)
    return unpaywall
