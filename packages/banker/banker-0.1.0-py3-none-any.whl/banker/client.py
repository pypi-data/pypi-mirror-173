
import yaml
import requests
import os
from enum import Enum
from datetime import datetime

from .accounts import Accounts
from .institutions import Institutions
from .requisitions import Requisitions
from .agreements import Agreements

from .enums import HTTP

class Client(Institutions, Accounts, Requisitions, Agreements):
    base_url: str = "https://ob.nordigen.com/api/v2/"
    def __init__(self):
        super().__init__(self._request)
        self.auth_path = "./auth.yaml"

    def accounts(self) -> dict:
        """
        Obtains a dictionary with all associated banks and connected accounts.
        """
        return {res["institution_id"]: res["accounts"] for res in self.requisitions()["results"] if res["accounts"]}

    def load_auth(self) -> dict:
        """
        Loads the authentication file if it exists.
        """
        try:
            with open(self.auth_path, "r") as f:
                return yaml.safe_load(f)

        except FileNotFoundError:
            return {}

    def save_auth(self, auth: dict) -> None:
        with open (self.auth_path, "w") as f:
            yaml.safe_dump(auth, f)

    def add_keys(self, secret_id: str, secret_key: str) -> None:
        """
        Adds keys to a auth.yaml file which is located at the same folder as the file that runs this method.
        If no auth.yaml file exist, it will be created.
        """
        auth = self.load_auth()
        auth["secret_id"] = secret_id
        auth["secret_key"] = secret_key
        self.save_auth(auth)
        self.generate_access_token()

    def _request(self, method: HTTP, url: str, data: dict = {}, headers: dict = {}, params: dict = {}, validate: bool = True):
        # We need to verify the authorization token before trying to access the API.
        if validate:
            self.validate_access_token()

        headers = self.load_headers()
    
        if method == HTTP.GET:
          response = requests.get(url, params = params, headers = headers)

        elif method == HTTP.POST:
          response = requests.post(url, data = data, headers = headers)

        elif method == HTTP.DELETE:
            response = requests.delete(url, data = data, headers = headers) 

        if response.ok:
          return response.json()

        return response.status_code

    def load_headers(self) -> dict:
        """ Loads headers if we have a access token, otherwise just empty. """
        if access_token := self.access_token():
          return {"Authorization": "Bearer {}".format(access_token)}

        return {}

    def validate_access_token(self):
        """
        Checks if the current access token is valid. If it's not, tries to create a new token from a
        refresh token. If both tokens are invalid, generate new tokens.
        """
        if self.is_access_token_valid():
          return

        if self.refresh_access_token():
            return
    
        # Both access -and refresh token are invalid.
        self.generate_access_token()

    def generate_access_token(self, verbose: bool = False) -> None:
        """
        Generates a new access -and refresh token which is added to the auth.yaml file.
        Args:
            verbose (bool): If specified, the new access -and refresh token are returned. 
        """
        auth = self.load_auth()
        if "secret_id" not in auth:
            raise ValueError("'secret_id' has not been inserted. Use 'add_keys(..) method'.")

        url = os.path.join(self.base_url, "token/new/")
        payload = {key: auth[key] for key in ["secret_id", "secret_key"]}
        output = self._request(HTTP.POST, url, data = payload, validate = False)
        auth["access_token"] = output["access"]
        auth["refresh_token"] = output["refresh"]
        auth["access_expires"] = self.time_now() + output["access_expires"] - 60
        auth["refresh_expires"] = self.time_now() + output["refresh_expires"] - 60
        self.save_auth(auth)
        if verbose:
            return output

    def refresh_access_token(self) -> bool:
        """ 
        Creates a new access token from a refresh token if the refresh token is valid. 
        Returns: A boolean indicating if a new access token has been generated.
        """
        url = os.path.join(self.base_url, "token/refresh/")
        if self.is_refresh_token_valid():
            payload = {"refresh": self.refresh_token()}
            output = self._request(HTTP.POST, url, data = payload, validate = False)
            auth = self.load_auth()
            auth["access_token"] = output["access"]
            auth["access_expires"] = self.time_now() + output["access_expires"] - 60
            self.save_auth(auth)
            return True

        return False

    def access_token(self) -> str:
        return self.load_auth().get("access_token")

    def access_expires(self) -> str:
        return self.load_auth().get("access_expires")

    def refresh_token(self) -> str:
        return self.load_auth().get("refresh_token")

    def refresh_expires(self) -> str:
        return self.load_auth().get("refresh_expires")

    def is_access_token_valid(self) -> bool:
        return self.access_expires() > self.time_now()

    def is_refresh_token_valid(self) -> bool:
        return self.refresh_expires() > self.time_now()
    
    def time_now(self) -> float:
        return datetime.timestamp(datetime.now())