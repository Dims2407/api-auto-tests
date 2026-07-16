from src.main.api.models.credit_repay_response import RepayCreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.requests.requester import Requester
from requests import Response
from http import HTTPStatus
import requests


class RepayCreditRequester(Requester):
    def post(self, repay_credit_request: RepayCreditRequest) -> RepayCreditResponse | Response:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return RepayCreditResponse(**response.json())
        return response