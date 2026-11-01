from typing import Protocol
from uuid import UUID

from app.handlers.transactions.models import PageMetadata, Transaction


class TransactionRepository(Protocol):
    def add(self, transaction: Transaction) -> None: ...
    def get_by_id(self, transaction_id: UUID) -> Transaction | None: ...
    def get(self, page: int, size: int) -> tuple[list[Transaction], PageMetadata]: ...
    def delete(self, transaction_id: UUID) -> None: ...
    def update(self, transaction: Transaction) -> None: ...


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: dict[UUID, Transaction] = {}

    def add(self, transaction: Transaction) -> None:
        self._transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        return self._transactions.get(transaction_id)

    def get(self, page: int, size: int) -> tuple[list[Transaction], PageMetadata]:
        transactions = list(self._transactions.values())
        if size == -1:
            metadata = PageMetadata(
                page=0, size=len(transactions), total=len(transactions)
            )
            return transactions, metadata

        start = page * size
        end = start + size
        page_transactions = transactions[start:end]
        metadata = PageMetadata(page=page, size=size, total=len(transactions))
        return page_transactions, metadata

    def delete(self, transaction_id: UUID) -> None:
        if transaction_id in self._transactions:
            del self._transactions[transaction_id]

    def update(self, transaction: Transaction) -> None:
        if transaction.id in self._transactions:
            self._transactions[transaction.id] = transaction
