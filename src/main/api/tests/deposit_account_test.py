import pytest
import requests

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account(self):
        create_user_request = CreateUserRequest(username="Max123311", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max123311", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        assert response.balance == 0
        account_id = response.id


        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=6666.6)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max123311", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        assert response.balance == 6666.6

    @pytest.mark.parametrize(
        "username, amount",
        [
            ("max999", 999),
            ("max9999", 9999)
        ]
    )
    def test_invalid_deposit_account(self,username, amount):
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)

        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_account_request)


