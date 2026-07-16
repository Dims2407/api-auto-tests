from src.main.api.models.account_transfer_response import TransferBetweenAccountsResponse
from src.main.api.models.account_transfer_request import TransferBetweenAccountsRequest
from src.main.api.requests.requester import Requester
from requests import Response
from http import HTTPStatus
import requests


class TransferBetweenAccountsRequester(Requester):
    def post(self, transfer_between_accounts_request: TransferBetweenAccountsRequest) -> TransferBetweenAccountsResponse | Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_between_accounts_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return TransferBetweenAccountsResponse(**response.json())
        return response