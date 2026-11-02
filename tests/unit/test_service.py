from decimal import Decimal
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from app.handlers.transactions.exceptions import TransactionNotFoundError
from app.handlers.transactions.models import TransactionType
from app.handlers.transactions.repository import InMemoryTransactionRepository
from app.handlers.transactions.schemas import TransactionCreate, TransactionUpdate
from app.handlers.transactions.service import TransactionService


def create_data(
    amount: str = "10.00",
    type: TransactionType = TransactionType.INCOME,
    title: str = "Salary",
) -> TransactionCreate:
    return TransactionCreate(title=title, amount=Decimal(amount), type=type)


def test_create_returns_and_stores_transaction(service: TransactionService) -> None:
    created = service.create(create_data(amount="12.34"))

    assert created.title == "Salary"
    assert created.amount == Decimal("12.34")
    assert created.type == TransactionType.INCOME
    assert service.get_by_id(created.id) == created


def test_create_generates_a_new_id_each_time(service: TransactionService) -> None:
    first = service.create(create_data())
    second = service.create(create_data())

    assert first.id != second.id


def test_get_by_id_raises_when_missing(service: TransactionService) -> None:
    missing_id = uuid4()

    with pytest.raises(TransactionNotFoundError) as exc_info:
        service.get_by_id(missing_id)

    assert exc_info.value.transaction_id == missing_id
    assert str(exc_info.value) == f"Transaction {missing_id} not found"


def test_get_returns_page_and_metadata(service: TransactionService) -> None:
    created = [service.create(create_data(title=f"t{i}")) for i in range(3)]

    transactions, metadata = service.get(page=1, size=2)

    assert transactions == created[2:]
    assert metadata.total == 3


def test_delete_removes_transaction(service: TransactionService) -> None:
    created = service.create(create_data())

    service.delete(created.id)

    with pytest.raises(TransactionNotFoundError):
        service.get_by_id(created.id)


def test_delete_raises_when_missing(service: TransactionService) -> None:
    with pytest.raises(TransactionNotFoundError):
        service.delete(uuid4())


def test_delete_missing_never_reaches_repository_delete() -> None:
    repo = create_autospec(InMemoryTransactionRepository, instance=True)
    repo.get_by_id.return_value = None
    service = TransactionService(repo)

    with pytest.raises(TransactionNotFoundError):
        service.delete(uuid4())

    repo.delete.assert_not_called()


def test_update_changes_only_sent_fields(service: TransactionService) -> None:
    created = service.create(create_data())

    updated = service.update(created.id, TransactionUpdate(title="Bonus"))

    assert updated.title == "Bonus"
    assert updated.amount == created.amount
    assert updated.type == created.type
    assert updated.id == created.id
    assert updated.created_at == created.created_at


def test_update_is_saved(service: TransactionService) -> None:
    created = service.create(create_data())

    service.update(created.id, TransactionUpdate(amount=Decimal("99.99")))

    assert service.get_by_id(created.id).amount == Decimal("99.99")


def test_update_ignores_none_values(service: TransactionService) -> None:
    created = service.create(create_data())

    updated = service.update(created.id, TransactionUpdate(title=None))

    assert updated.title == created.title


def test_update_raises_when_missing(service: TransactionService) -> None:
    with pytest.raises(TransactionNotFoundError):
        service.update(uuid4(), TransactionUpdate(title="x"))


def test_summary_with_no_transactions(service: TransactionService) -> None:
    summary = service.summary()

    assert summary.income == Decimal(0)
    assert summary.expense == Decimal(0)
    assert summary.balance == Decimal(0)


def test_summary_income_only(service: TransactionService) -> None:
    service.create(create_data("100.50", TransactionType.INCOME))

    summary = service.summary()

    assert summary.income == Decimal("100.50")
    assert summary.expense == Decimal(0)
    assert summary.balance == Decimal("100.50")


def test_summary_balance_can_be_negative(service: TransactionService) -> None:
    service.create(create_data("20.00", TransactionType.EXPENSE))

    summary = service.summary()

    assert summary.income == Decimal(0)
    assert summary.expense == Decimal("20.00")
    assert summary.balance == Decimal("-20.00")


def test_summary_mixes_income_and_expenses(service: TransactionService) -> None:
    service.create(create_data("1000.50", TransactionType.INCOME))
    service.create(create_data("200.00", TransactionType.INCOME))
    service.create(create_data("3.25", TransactionType.EXPENSE))

    summary = service.summary()

    assert summary.income == Decimal("1200.50")
    assert summary.expense == Decimal("3.25")
    assert summary.balance == Decimal("1197.25")


def test_summary_stays_exact_with_decimal(service: TransactionService) -> None:
    service.create(create_data("0.10", TransactionType.INCOME))
    service.create(create_data("0.20", TransactionType.INCOME))

    assert service.summary().income == Decimal("0.30")


def test_summary_counts_every_transaction_not_one_page(
    service: TransactionService,
) -> None:
    for _ in range(12):
        service.create(create_data("1.00", TransactionType.INCOME))

    assert service.summary().income == Decimal("12.00")
