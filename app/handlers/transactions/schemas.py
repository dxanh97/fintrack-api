from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.handlers.transactions.models import TransactionType

Title = Annotated[str, Field(min_length=1, max_length=200)]
Amount = Annotated[Decimal, Field(gt=0, max_digits=20, decimal_places=2)]


class TransactionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title
    amount: Amount
    type: TransactionType


class TransactionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title | None = None
    amount: Amount | None = None
    type: TransactionType


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    amount: Decimal
    type: TransactionType
    created_at: datetime


class TransactionPageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transactions: list[TransactionRead]
    total: int
