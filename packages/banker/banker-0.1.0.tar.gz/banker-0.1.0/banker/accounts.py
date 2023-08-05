
import os

from .enums import HTTP 

class Accounts:
    accounts_url : str = "https://ob.nordigen.com/api/v2/accounts/"
    def __init__(self, _request):
        self._request = _request

    def account(self, account_id: str) -> dict:
        """
        Generates an overview for a single account based of an 'account_id'.
        """
        url = os.path.join(self.accounts_url, "{}/".format(account_id))
        return self._request(HTTP.GET, url)

    def account_balance(self, account_id: str) -> dict:
        url = os.path.join(self.accounts_url, "{}/balances/".format(account_id))
        return self._request(HTTP.GET, url)

    def account_details(self, account_id: str) -> dict:
        url = os.path.join(self.accounts_url, "{}/details/".format(account_id))
        return self._request(HTTP.GET, url)

    def transactions(self, account_id: str) -> dict:
        url = os.path.join(self.accounts_url, "{}/transactions/".format(account_id))
        return self._request(HTTP.GET, url)

