from random import uniform
import pytest
from sqlalchemy.orm import Session
from src.main.api.db.engine import SessionLocal

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestCreditRepay:
    def test_valid_credit_repay(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
        amount = round(uniform(5000, 15000), 2)

        response = api_manager.user_steps.create_credit_account(create_credit_user_request)
        account_id = response.id

        credit_request = CreditRequest(
            accountId=account_id,
            amount=amount,
            termMonths=12)
        response = api_manager.user_steps.valid_credit_request(create_credit_user_request, credit_request)
        credit_id = response.creditId

        credit_from_db = Credit.get_credit(db_session, account_id=account_id)
        assert credit_from_db.term_months == response.termMonths
        assert credit_from_db.balance == -amount

        account_from_db = Account.get_account_by_id(db_session, account_id)
        assert account_from_db.balance == response.balance


        credit_repay_request = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )
        response = api_manager.user_steps.valid_credit_repay_request(create_credit_user_request, credit_repay_request)

        assert response.creditId == credit_id
        assert response.amountDeposited == amount

        with SessionLocal() as verify_session:
            credit_from_db = Credit.get_credit(verify_session, account_id=account_id)
            assert credit_from_db.account_id == credit_repay_request.accountId
            assert credit_from_db.balance == 0

            account_from_db = Account.get_account_by_id(verify_session, account_id)
            assert account_from_db.balance == 0





    def test_invalid_credit_repay(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, db_session: Session):
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

        credit_from_db = Credit.get_credit(db_session, account_id=account_id)
        assert credit_from_db.term_months == response.termMonths
        assert credit_from_db.balance == -amount

        account_from_db = Account.get_account_by_id(db_session, account_id)
        assert account_from_db.balance == response.balance

        over_amount = round(uniform(15000, 20000), 2)
        credit_repay_request = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=over_amount
        )
        api_manager.user_steps.invalid_credit_repay_request(create_credit_user_request, credit_repay_request)

        """При невалидной попытке погасить кредит, баланс не изменяется"""
        with SessionLocal() as verify_session:
            credit_from_db = Credit.get_credit(verify_session, account_id=account_id)
            assert credit_from_db.account_id == credit_repay_request.accountId
            assert credit_from_db.balance == -amount

            account_from_db = Account.get_account_by_id(verify_session, account_id)
            assert account_from_db.balance == amount
