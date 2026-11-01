from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.handlers.transactions.dependencies import TransactionServiceDep
from app.handlers.transactions.schemas import (
    SummaryRead,
    TransactionCreate,
    TransactionPageRead,
    TransactionRead,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionPageRead)
async def get_transactions(
    service: TransactionServiceDep,
    page: Annotated[int, Query(ge=0)] = 0,
    size: Annotated[int, Query(ge=1, le=1000)] = 10,
):
    (transactions, page_metadata) = service.get(page, size)
    return TransactionPageRead(
        transactions=transactions,
        total=page_metadata.total,
    )


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
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


@router.get("/summary", response_model=SummaryRead)
async def get_summary(
    service: TransactionServiceDep,
):
    summary = service.summary()
    return summary
