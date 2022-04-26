import os
import requests


class Altmetric:
    """A class representing the results of querying the Altmetric-API for a given DOI."""

    @property
    def mentions(self):
        """
        The mentions of the document.
        """
        try:
            return self._json['posts']
        except KeyError:
            return None
        except AttributeError:
            return None

    def __init__(self, r):
        if r.status_code == 200:
            self._json = r.json()
        else:
            pass

