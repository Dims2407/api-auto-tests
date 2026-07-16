import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRequest:
    def test_valid_credit_request(self):
        create_user_request = CreateUserRequest(
            username="Max122",
            password="Pas!sw0rd",
            role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(
                username="admin",
                password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(
            accountId=account_id,
            amount=6500.5)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        assert response.balance == 6500.5
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=5000,
            termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)
        assert response.amount == 5000
        assert response.balance == 11500.5
        assert response.termMonths == 12

    def test_credit_request(self):
        create_user_request = CreateUserRequest(
            username="Max1122",
            password="Pas!sw0rd",
            role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(
                username="admin",
                password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        first_account_id = response.id

        deposit_account_request = DepositAccountRequest(
            accountId=first_account_id,
            amount=6500.5)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        assert response.balance == 6500.5

        credit_request = CreditRequest(
            accountId=first_account_id,
            amount=5000,
            termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)
        assert response.amount == 5000
        assert response.balance == 11500.5
        assert response.termMonths == 12

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        second_account_id = response.id

        credit_request = CreditRequest(
            accountId=second_account_id,
            amount=5000,
            termMonths=12)

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1122",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_not_found()
        ).post(credit_request)


