import pytest
from requests import Session
from src.main.api.db.crud.transaction_crud import TransactionCrud as Transaction
from src.main.api.models.deposit_account_request import DepositAccountRequest
from random import uniform

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account(self, db_session: Session,api_manager, create_user_request):
        amount = round(uniform(1000, 9000), 2)

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)
        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)
        assert response.balance == amount

        get_deposit_from_db = Transaction.get_balance(db_session, deposit_account_request.amount)
        assert response.balance == get_deposit_from_db.amount, "Зачисления не произошло"
        assert get_deposit_from_db.transaction_type == "deposit"



    @pytest.mark.parametrize(
        "amount",
        [
            999,
            9001
        ]
    )
    def test_invalid_deposit_account(self, amount, db_session, api_manager, create_user_request):
        """Пополнение невалидными суммами из параметризации"""
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        account_id = response.id

        deposit_account_request = DepositAccountRequest(accountId=account_id, amount=amount)
        api_manager.user_steps.invalid_deposit_account(create_user_request, deposit_account_request)

        get_deposit_from_db = Transaction.get_balance(db_session, deposit_account_request.amount)
        assert get_deposit_from_db is None, "Произошло ошибочное пополнение"
