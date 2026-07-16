from src.main.api.models.base_model import BaseModel


class TransferBetweenAccountsRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float