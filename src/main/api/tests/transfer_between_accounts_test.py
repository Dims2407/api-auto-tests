import pytest

from src.main.api.models.account_transfer_request import TransferBetweenAccountsRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.transfer_between_accounts_requester import TransferBetweenAccountsRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferBetweenAccount:
    def test_valid_transfer_between_account(self):
        create_user_request = CreateUserRequest(
            username="Max1111",
            password="Pas!sw0rd",
            role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(
                username="admin",
                password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1111",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        first_account_id = response.id

        deposit_account_request = DepositAccountRequest(
            accountId=first_account_id,
            amount=6666.6)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1111",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        assert response.balance == 6666.6

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1111",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        second_account_id = response.id

        transfer_between_accounts_request = TransferBetweenAccountsRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=5000.6)
        transfer_response = TransferBetweenAccountsRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max1111",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_between_accounts_request)

        assert transfer_response.fromAccountId == first_account_id
        assert transfer_response.toAccountId == second_account_id
        assert transfer_response.fromAccountIdBalance == 1666

    def test_invalid_transfer_between_account(self):
        create_user_request = CreateUserRequest(
            username="Max0",
            password="Pas!sw0rd",
            role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(
                username="admin",
                password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max0",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        first_account_id = response.id

        deposit_account_request = DepositAccountRequest(
            accountId=first_account_id,
            amount=6666.6)

        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max0",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)

        assert response.balance == 6666.6

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max0",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        second_account_id = response.id

        transfer_between_accounts_request = TransferBetweenAccountsRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=8000.6)
        TransferBetweenAccountsRequester(
            request_spec=RequestSpecs.auth_headers(
                username="Max0",
                password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable()
        ).post(transfer_between_accounts_request)


