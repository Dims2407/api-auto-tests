import pytest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from random import uniform


@pytest.mark.api
class TestDepositAccount:

    def test_deposit_account(self, api_manager, create_user_request):
        amount = round(uniform(1000, 9000), 2)


        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)

        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)
        assert response.balance == amount


    @pytest.mark.parametrize(
        "amount",
        [
            999,
            9001
        ]
    )
    def test_invalid_deposit_account(self, amount, api_manager, create_user_request):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)
        api_manager.user_steps.invalid_deposit_account(create_user_request, deposit_account_request)
