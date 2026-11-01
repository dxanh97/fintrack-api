from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.handlers.transactions.repository import (
    InMemoryTransactionRepository,
    TransactionRepository,
)
from app.handlers.transactions.service import TransactionService


@lru_cache
def get_transaction_repository() -> TransactionRepository:
    return InMemoryTransactionRepository()


def get_transaction_service(
    repo: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> TransactionService:
    return TransactionService(repo)


TransactionServiceDep = Annotated[TransactionService, Depends(get_transaction_service)]
