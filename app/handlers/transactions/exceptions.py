from uuid import UUID


class TransactionNotFoundError(Exception):
    def __init__(self, transaction_id: UUID) -> None:
        super().__init__(f"Transaction {transaction_id} not found")
        self.transaction_id = transaction_id
