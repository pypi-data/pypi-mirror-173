
import os

from .enums import HTTP

class Institutions:
    institutions_url: str = "https://ob.nordigen.com/api/v2/institutions/"
    def __init__(self, _request):
        self._request = _request

    def institutions(self, country_code: str = "se") -> dict:
        return self._request(HTTP.GET, self.institutions_url, params = {"country": "se"})

    def search_institution(self, institution: str, country_code: str = "se") -> dict:
        """
        Search for a specific institution. The institution doesn't have to match exactly.
        """
        institutions = self.institutions()
        return [ins for ins in institutions if institution in ins.get("name").lower()]