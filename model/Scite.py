import os
import requests


class Scite:
    """A class representing the results of querying the Unpaywall-API for a given DOI."""

    @property
    def total(self):
        """
        The doi of the document.
        """
        try:
            return self._json['total']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def supporting(self):
        """
        The doi of the document.
        """
        try:
            return self._json['supporting']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def contradicting(self):
        """
        The doi of the document.
        """
        try:
            return self._json['contradicting']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def mentioning(self):
        """
        The doi of the document.
        """
        try:
            return self._json['mentioning']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def unclassified(self):
        """
        The doi of the document.
        """
        try:
            return self._json['unclassified']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def citingPublications(self):
        """
        The doi of the document.
        """
        try:
            return self._json['citingPublications']
        except KeyError:
            return None
        except AttributeError:
            return None

    def __init__(self, r):
        if r.status_code == 200:
            self._json = r.json()
        else:
            pass

