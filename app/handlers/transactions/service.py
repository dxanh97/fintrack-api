from dataclasses import replace
from uuid import UUID, uuid4

from app.handlers.transactions.models import Transaction
from app.handlers.transactions.repository import TransactionRepository
from app.handlers.transactions.schemas import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, repo: TransactionRepository) -> None:
        self._repo = repo

    def create(self, data: TransactionCreate) -> Transaction:
        transaction = Transaction(id=uuid4(), title=data.title, amount=data.amount)
        self._repo.add(transaction)
        return transaction

    def get(self, transaction_id: UUID) -> Transaction:
        transaction = self._repo.get(transaction_id)
        if transaction is None:
            print(f"Transaction with ID {transaction_id} not found.")
            # raise TransactionNotFoundError(transaction_id)
        return transaction

    def list_all(self) -> list[Transaction]:
        return self._repo.list_all()

    def delete(self, transaction_id: UUID) -> None:
        transaction = self._repo.get(transaction_id)
        if transaction is None:
            print(f"Transaction with ID {transaction_id} not found.")
            # raise TransactionNotFoundError(transaction_id)
        self._repo.delete(transaction_id)

    def update(self, transaction_id: UUID, data: TransactionUpdate) -> Transaction:
        transaction = self.get(transaction_id)
        if transaction is None:
            print(f"Transaction with ID {transaction_id} not found.")
            # raise TransactionNotFoundError(transaction_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        updated_transaction = replace(transaction, **changes)
        self._repo.update(updated_transaction)
        return updated_transaction
