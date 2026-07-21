import pytest
from src.main.api.models.deposit_account_request import DepositAccountRequest



@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account(self, api_manager, create_user_request):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=6666.6)

        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)
        assert response.balance == 6666.6

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
