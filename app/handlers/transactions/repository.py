from typing import Protocol
from uuid import UUID

from app.handlers.transactions.models import Transaction


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...
    def get(self, transaction_id: UUID) -> Transaction | None: ...
    def list_all(self) -> list[Transaction]: ...
    def delete(self, transaction_id: UUID) -> None: ...
    def update(self, transaction: Transaction) -> None: ...


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: dict[UUID, Transaction] = {}

    def add(self, transaction: Transaction) -> None:
        self._transactions[transaction.id] = transaction

    def get(self, transaction_id: UUID) -> Transaction | None:
        return self._transactions.get(transaction_id)

    def list_all(self) -> list[Transaction]:
        return list(self._transactions.values())

    def delete(self, transaction_id: UUID) -> None:
        if transaction_id in self._transactions:
            del self._transactions[transaction_id]

    def update(self, transaction: Transaction) -> None:
        if transaction.id in self._transactions:
            self._transactions[transaction.id] = transaction
