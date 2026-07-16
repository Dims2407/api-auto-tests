from src.main.api.models.base_model import BaseModel


class TransferBetweenAccountsResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float