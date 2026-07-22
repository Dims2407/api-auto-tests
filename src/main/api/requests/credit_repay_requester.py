from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.requests.requester import Requester
from requests import Response
from http import HTTPStatus
import requests


class RepayCreditRequester(Requester):
    def post(self, credit_repay_request: CreditRepayRequest) -> CreditRepayResponse | Response:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=credit_repay_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return CreditRepayResponse(**response.json())
        return response