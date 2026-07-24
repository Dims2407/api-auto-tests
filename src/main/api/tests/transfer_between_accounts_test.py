from random import uniform
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.account_transfer_request import TransferBetweenAccountsRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestTransferBetweenAccount:
    def test_valid_transfer_between_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
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

        """Сопоставление с данными из БД"""
        transfer_from_db = Transaction.get_amount(db_session, amount=transfer_amount)
        assert transfer_from_db.amount == transfer_amount
        assert transfer_from_db.from_account_id == first_account_id
        assert transfer_from_db.to_account_id == second_account_id

        """Чек баланс в БД после перевода"""
        account_from_db = Account.get_account_by_id(db_session, first_account_id)
        assert account_from_db.balance == transfer_response.fromAccountIdBalance

    def test_invalid_transfer_between_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
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

        transfer_amount = round(uniform(10001, 15000), 2)
        transfer_between_accounts_request = TransferBetweenAccountsRequest(
            fromAccountId=first_account_id,
            toAccountId=second_account_id,
            amount=transfer_amount)

        api_manager.user_steps.invalid_transfer_between_accounts(
            create_user_request,
            transfer_between_accounts_request)

        transfer_from_db = Transaction.get_amount(db_session, transfer_between_accounts_request.amount)
        assert transfer_from_db is None, "Ошибочный перевод"

