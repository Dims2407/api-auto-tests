from random import uniform
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account



@pytest.mark.api
class TestCreditRequest:
    def test_valid_credit_request(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
        amount = round(uniform(5000, 15000), 2)


        response = api_manager.user_steps.create_credit_account(create_credit_user_request)

        assert response.balance == 0
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=8)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)

        assert response.amount == amount
        assert response.balance == amount
        assert response.termMonths == 8

        credit_from_db = Credit.get_credit(db_session, account_id=account_id)
        assert credit_from_db.term_months == response.termMonths

        account_from_db = Account.get_account_by_id(db_session, account_id)
        assert account_from_db.balance == response.balance



    def test_invalid_credit_request(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
        """Взять кредит на второй счет при наличии кредита на первом"""
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_credit_account(create_credit_user_request)

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


        credit_from_db = Credit.get_credit(db_session, account_id=account_id)
        assert credit_from_db.term_months == response.termMonths

        account_from_db = Account.get_account_by_id(db_session, account_id)
        assert account_from_db.balance == response.balance


        response = api_manager.user_steps.create_credit_account(create_credit_user_request)
        second_account_id = response.id

        credit_request = CreditRequest(
            accountId=second_account_id,
            amount=amount,
            termMonths=12)
        api_manager.user_steps.invalid_credit_request(create_credit_user_request, credit_request)

        second_credit_from_db = Credit.get_credit(db_session, account_id=second_account_id)
        assert second_credit_from_db is None, "Ошибочное зачисление кредита"

        account_from_db = Account.get_account_by_id(db_session, second_account_id)
        assert account_from_db.balance == 0, "Ошибочное зачисление на второй счет"