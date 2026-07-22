from random import uniform
import pytest
from src.main.api.models.credit_request import CreditRequest



@pytest.mark.api
class TestCreditRequest:
    def test_valid_credit_request(self, api_manager, create_credit_user_request):
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_account(create_credit_user_request)

        assert response.balance == 0
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=12)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)

        assert response.amount == amount
        assert response.balance == amount
        assert response.termMonths == 12

    def test_invalid_credit_request(self, api_manager, create_credit_user_request):
        """Взять кредит на второй счет при наличии кредита на первом"""
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_account(create_credit_user_request)

        assert response.balance == 0
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=12)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)

        assert response.amount == amount
        assert response.balance == amount
        assert response.termMonths == 12

        response = api_manager.user_steps.create_account(create_credit_user_request)
        second_account_id = response.id

        credit_request = CreditRequest(
            accountId=second_account_id,
            amount=amount,
            termMonths=12)
        api_manager.user_steps.invalid_credit_request(create_credit_user_request, credit_request)
