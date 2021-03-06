import os
import requests


class Unpaywall:
    """A class representing the results of querying the Unpaywall-API for a given DOI."""

    @property
    def doi(self):
        """
        The doi of the document.
        """
        try:
            return self._json['doi']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def doi_resolver(self):
        """
        The doi resolver of the document.
        """
        try:
            return self._json['doi_resolver']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def evidence(self):
        """
        The evidence of the document.
        """
        try:
            return self._json['evidence']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def free_fulltext_url(self):
        """
        The url of the free fulltext of the document.
        """
        try:
            if self._json['best_oa_location']:
                return self._json['best_oa_location']['url']
            else:
                return False
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def is_boai_license(self):
        """
        If a boai license exists for the document.
        """
        try:
            return self._json['is_boai_license']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def is_free_to_read(self):
        """
        If the document is free to read.
        """
        try:
            return self._json['is_free_to_read']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def is_oa(self):
        """
        open access status
        """
        try:
            return self._json['is_oa']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def is_subscription_journal(self):
        """
        If the document is published in a subscription journal.
        """
        try:
            return self._json['is_subscription_journal']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def license(self):
        """
        The license of the document.
        """
        try:
            return self._json['license']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def oa_color(self):
        """
        The open access color of the document.
        """
        try:
            return self._json['oa_status']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def reported_noncompliant_copies(self):
        """
        The reported noncompliant copies of the document.
        """
        try:
            return self._json['reported_noncompliant_copies']
        except KeyError:
            return None
        except AttributeError:
            return None

    @property
    def title(self):
        """
        The title of the document.
        """
        try:
            return self._json['title']
        except KeyError:
            return None
        except AttributeError:
            return None

    def __init__(self, r):
        if r.status_code == 200:
            self._json = r.json()
        else:
            pass

