import pytest

from app.handlers.transactions.repository import InMemoryTransactionRepository
from app.handlers.transactions.service import TransactionService


@pytest.fixture
def repo() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def service(repo: InMemoryTransactionRepository) -> TransactionService:
    return TransactionService(repo)
