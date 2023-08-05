

import os

from .enums import HTTP

class Agreements:
    agreements_url: str = "https://ob.nordigen.com/api/v2/agreements/enduser/"
    def __init__(self, _request):
        self._request = _request

    def agreements(self) -> dict:
        """
        Obtain all agreements for the user.
        """
        return self._request(HTTP.GET, self.agreements_url)