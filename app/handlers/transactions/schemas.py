from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

Title = Annotated[str, Field(min_length=1, max_length=200)]
Amount = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class TransactionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title
    amount: Amount


class TransactionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title | None = None
    amount: Amount | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    amount: Decimal
    created_at: datetime
