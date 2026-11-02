from decimal import Decimal
from uuid import uuid4

import pytest

from app.handlers.transactions.models import (
    PageMetadata,
    Transaction,
    TransactionType,
)
from app.handlers.transactions.repository import InMemoryTransactionRepository


def make_transaction(title: str = "Salary") -> Transaction:
    return Transaction(
        id=uuid4(), title=title, amount=Decimal("10.00"), type=TransactionType.INCOME
    )


def add_transactions(
    repo: InMemoryTransactionRepository, count: int
) -> list[Transaction]:
    transactions = [make_transaction(f"t{i}") for i in range(count)]
    for transaction in transactions:
        repo.add(transaction)
    return transactions


def test_get_by_id_returns_added_transaction(
    repo: InMemoryTransactionRepository,
) -> None:
    transaction = make_transaction()
    repo.add(transaction)

    assert repo.get_by_id(transaction.id) == transaction


def test_get_by_id_returns_none_when_missing(
    repo: InMemoryTransactionRepository,
) -> None:
    assert repo.get_by_id(uuid4()) is None


@pytest.mark.parametrize(
    ("page", "size", "expected_slice"),
    [
        (0, 2, slice(0, 2)),
        (1, 2, slice(2, 4)),
        (2, 2, slice(4, 5)),
        (3, 2, slice(0, 0)),
    ],
)
def test_get_returns_requested_page(
    repo: InMemoryTransactionRepository,
    page: int,
    size: int,
    expected_slice: slice,
) -> None:
    transactions = add_transactions(repo, 5)

    result, metadata = repo.get(page, size)

    assert result == transactions[expected_slice]
    assert metadata == PageMetadata(page=page, size=size, total=5)


def test_get_on_empty_repository(repo: InMemoryTransactionRepository) -> None:
    result, metadata = repo.get(0, 10)

    assert result == []
    assert metadata.total == 0


def test_get_all_ignores_paging(repo: InMemoryTransactionRepository) -> None:
    transactions = add_transactions(repo, 12)

    assert repo.get_all() == transactions


def test_get_all_returns_a_copy(repo: InMemoryTransactionRepository) -> None:
    add_transactions(repo, 1)

    repo.get_all().clear()

    assert len(repo.get_all()) == 1


def test_delete_removes_transaction(repo: InMemoryTransactionRepository) -> None:
    transaction = make_transaction()
    repo.add(transaction)

    repo.delete(transaction.id)

    assert repo.get_by_id(transaction.id) is None


def test_delete_missing_does_nothing(repo: InMemoryTransactionRepository) -> None:
    add_transactions(repo, 1)

    repo.delete(uuid4())

    assert len(repo.get_all()) == 1


def test_update_replaces_transaction(repo: InMemoryTransactionRepository) -> None:
    transaction = make_transaction("Old")
    repo.add(transaction)
    updated = Transaction(
        id=transaction.id,
        title="New",
        amount=transaction.amount,
        type=transaction.type,
    )

    repo.update(updated)

    assert repo.get_by_id(transaction.id) == updated


def test_update_missing_does_not_add(repo: InMemoryTransactionRepository) -> None:
    repo.update(make_transaction())

    assert repo.get_all() == []
