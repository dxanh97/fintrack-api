from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class Transaction:
    id: UUID
    title: str
    amount: Decimal
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
