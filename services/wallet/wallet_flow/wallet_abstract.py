from typing import Optional


class WalletService:

    @staticmethod
    async def get_balance() -> float:
        raise NotImplementedError

    @staticmethod
    async def send_transaction(self, to_address: str, amount: float,
                               token_contract_address: Optional[str] = None) -> str:
        raise NotImplementedError

    @staticmethod
    async def get_transaction_receipt(self, txn_hash: str) -> dict:
        raise NotImplementedError
