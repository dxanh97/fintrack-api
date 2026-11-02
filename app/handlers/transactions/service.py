from dataclasses import replace
from decimal import Decimal
from uuid import UUID, uuid4

from app.handlers.transactions.exceptions import TransactionNotFoundError
from app.handlers.transactions.models import PageMetadata, Transaction, TransactionType
from app.handlers.transactions.repository import TransactionRepository
from app.handlers.transactions.schemas import (
    SummaryRead,
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)


class TransactionService:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def create(self, data: TransactionCreate) -> TransactionRead:
        transaction = Transaction(
            id=uuid4(), title=data.title, amount=data.amount, type=data.type
        )
        self._repo.add(transaction)
        return TransactionRead.model_validate(transaction)

    def get_by_id(self, transaction_id: UUID) -> TransactionRead:
        transaction = self._repo.get_by_id(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(transaction_id)
        return TransactionRead.model_validate(transaction)

    def get(self, page: int, size: int) -> tuple[list[TransactionRead], PageMetadata]:
        transactions, page_metadata = self._repo.get(page, size)
        return (
            [TransactionRead.model_validate(t) for t in transactions],
            page_metadata,
        )

    def delete(self, transaction_id: UUID) -> None:
        self.get_by_id(transaction_id)
        self._repo.delete(transaction_id)

    def update(self, transaction_id: UUID, data: TransactionUpdate) -> TransactionRead:
        transaction = self._repo.get_by_id(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(transaction_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        updated_transaction = replace(transaction, **changes)
        self._repo.update(updated_transaction)
        return TransactionRead.model_validate(updated_transaction)

    def summary(self) -> SummaryRead:
        transactions = self._repo.get_all()
        income = sum(
            (t.amount for t in transactions if t.type == TransactionType.INCOME),
            Decimal(0),
        )
        expense = sum(
            (t.amount for t in transactions if t.type == TransactionType.EXPENSE),
            Decimal(0),
        )
        balance = income - expense
        return SummaryRead(income=income, expense=expense, balance=balance)
