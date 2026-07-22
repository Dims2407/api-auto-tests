from random import uniform
import pytest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest

@pytest.mark.api
class TestCreditRepay:
    def test_valid_credit_repay(self, api_manager, create_credit_user_request):
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=12)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)
        credit_id = response.creditId

        credit_repay_request = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )
        response = api_manager.user_steps.valid_credit_repay_request(create_credit_user_request, credit_repay_request)

        assert response.creditId == credit_id
        assert response.amountDeposited == amount

    def test_invalid_credit_repay(self, api_manager, create_credit_user_request):
        """Погасить на сумму превышающую остаток по кредиту"""
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=12)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)
        credit_id = response.creditId

        over_amount = round(uniform(15000, 20000), 2)
        credit_repay_request = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=over_amount
        )
        api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)
