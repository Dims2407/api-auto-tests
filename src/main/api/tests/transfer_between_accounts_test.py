from random import uniform
import pytest
from src.main.api.models.account_transfer_request import TransferBetweenAccountsRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest

@pytest.mark.api
class TestTransferBetweenAccount:
    def test_valid_transfer_between_account(self, api_manager, create_user_request):
        amount = round(uniform(1000, 9000), 2)

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        first_account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=first_account_id, amount=amount)

        response = api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_account_request)
        assert response.balance == amount

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        second_account_id = response.id

        transfer_amount = round(uniform(500, 1000), 2)
        transfer_between_accounts_request = TransferBetweenAccountsRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=transfer_amount)

        transfer_response = api_manager.user_steps.valid_transfer_between_accounts(
            create_user_request,
            transfer_between_accounts_request)

        assert transfer_response.fromAccountId == first_account_id
        assert transfer_response.toAccountId == second_account_id
        assert transfer_response.fromAccountIdBalance == amount - transfer_amount

    def test_invalid_transfer_between_account(self, api_manager, create_user_request):
        """Перевод превышает сумму средств на отправном счету"""
        amount = round(uniform(1000, 9000), 2)

        response = api_manager.user_steps.create_account(create_user_request)
        first_account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=first_account_id, amount=amount)

        api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_account_request)

        response = api_manager.user_steps.create_account(create_user_request)
        second_account_id = response.id

        transfer_amount = round(uniform(10001, 1500), 2)
        transfer_between_accounts_request = TransferBetweenAccountsRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=transfer_amount)

        api_manager.user_steps.invalid_transfer_between_accounts(
            create_user_request,
            transfer_between_accounts_request)

