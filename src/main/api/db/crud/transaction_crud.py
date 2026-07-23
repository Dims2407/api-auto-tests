from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrud:
    """Наличие записи в БД о зачислении средств"""

    @staticmethod
    def get_amount(db: Session, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(amount=amount).first()


