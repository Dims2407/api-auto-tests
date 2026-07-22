from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from src.main.api.models.account_transfer_request import TransferBetweenAccountsRequest
from src.main.api.models.account_transfer_response import TransferBetweenAccountsResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse,
    )

    ADMIN_CREATE_CREDIT_USER = EndpointConfiguration(
        request_model=CreateCreditUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse,
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model=DepositAccountRequest,
        url="/account/deposit",
        response_model=DepositAccountResponse
    )

    TRANSFER_BETWEEN_ACCOUNTS = EndpointConfiguration(
        request_model=TransferBetweenAccountsRequest,
        url="/account/transfer",
        response_model=TransferBetweenAccountsResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model=CreditRequest,
        url="/credit/request",
        response_model=CreditResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse
    )
