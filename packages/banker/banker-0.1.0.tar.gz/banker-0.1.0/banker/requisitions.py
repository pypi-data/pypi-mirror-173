

import os

from .enums import HTTP

class Requisitions:
    requisitions_url: str = "https://ob.nordigen.com/api/v2/requisitions/"
    def __init__(self, _request):
        self._request = _request

    def requisitions(self) -> dict:
        """
        Obtain all requisitions.
        """
        return self._request(HTTP.GET, self.requisitions_url)

    def submit_requisition(self, institution_id: str) -> dict:
        """
        Submits a requisition which is a request to link all accounts within a bank to the api. 
        Args:
            institution_id (str). A valid institution_id which can be obtained by using
            client.search_institution({str})
        Returns:
            A link which one need to follow and and agree in order to connect to the API.
        """
        redirect = "http://www.nordigen.com"
        data = {"redirect": redirect, "institution_id": institution_id}
        output = self._request(HTTP.POST, self.requisitions_url, data = data)
        return output["link"]

    def delete_requisition(self, requisition_id: str):
        url = os.path.join(self.requisitions_url, "{}/".format(requisition_id))
        return self._request(HTTP.DELETE, url)