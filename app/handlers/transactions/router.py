from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.handlers.transactions.dependencies import TransactionServiceDep
from app.handlers.transactions.schemas import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
async def get_transactions(
    service: TransactionServiceDep,
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
):
    transactions = service.list_all()
    return transactions


@router.post("", response_model=TransactionRead)
async def create_transaction(
    service: TransactionServiceDep,
    transaction: TransactionCreate,
):
    created_transaction = service.create(transaction)
    return created_transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: UUID,
    service: TransactionServiceDep,
    transaction: TransactionUpdate,
):
    updated_transaction = service.update(transaction_id, transaction)
    return updated_transaction


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: UUID,
    service: TransactionServiceDep,
):
    service.delete(transaction_id)
