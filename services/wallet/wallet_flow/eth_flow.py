from datetime import datetime
from web3 import Web3
from database.config import METAMASK_SECRET, ETHERSCAN_API_KEY
from services.exceptions.exceptions import TransactionError
from services.wallet.wallet_flow.wallet_abstract import WalletService
import httpx


class EthWalletService(WalletService):
    def __init__(self, address: str = None, contract_address: str = None):
        self.address = address
        self.contract_address = contract_address
        self.rpc_url = f"https://mainnet.infura.io/v3/{METAMASK_SECRET}"
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))

    async def get_balance(self) -> float:
        """
        Get balance of the wallet
        """
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to blockchain node")

        checksum_address = self.web3.to_checksum_address(self.address)

        if self.contract_address:
            contract = self.web3.eth.contract(
                address=self.web3.to_checksum_address(self.contract_address),
                abi=ERC20_ABI  # noqa
            )
            balance = contract.functions.balanceOf(checksum_address).call()
            decimals = contract.functions.decimals().call()
            return balance / (10 ** decimals)
        else:
            balance = self.web3.eth.get_balance(checksum_address)
            return balance / 10 ** 18

    async def send_transaction(self, to_address: str, amount: float, private_key: str) -> str:  # noqa
        """
        Send transaction from the wallet to the provided address
        """
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to blockchain node")

        balance = await self.get_balance()
        if balance < amount:
            raise TransactionError("Insufficient balance")

        transaction = {
            'to': self.web3.to_checksum_address(to_address),
            'from': self.web3.to_checksum_address(self.address),
            'value': self.web3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': self.web3.to_wei('20', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.address),
            'chainId': 1  # Mainnet
        }

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)

        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return self.web3.to_hex(txn_hash)

    async def get_transaction_receipt(self, txn_hash: str) -> dict:
        """
        Get transaction receipt and status
        """
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to blockchain node")

        try:
            txn_detail = self.web3.eth.get_transaction(txn_hash)
            status = (
                lambda x: "success" if x == 1 else "failed"
            )(self.web3.eth.get_transaction_receipt(txn_hash).get('status'))
        except Exception:
            raise TransactionError("Transaction not found")

        return await self._get_transaction_info(txn_detail, status)

    async def get_transactions(self, limit: int = 10, offset: int = 0) -> dict:
        """
        Get transaction history for the wallet using Etherscan API with pagination.
        """
        api_key = ETHERSCAN_API_KEY

        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": self.address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": api_key
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

        if data["status"] != "1":
            raise TransactionError(
                f"Failed to fetch transactions: {data.get('message')}"
            )

        all_transactions = data["result"]
        total = len(all_transactions)
        paginated_transactions = all_transactions[offset:offset + limit]

        return {
            "total": total,
            "transactions": [
                {
                    "hash": txn["hash"],
                    "from": txn["from"],
                    "to": txn["to"],
                    "value": f"{self.web3.from_wei(int(txn['value']), 'ether')} ETH",
                    "gas": txn["gas"],
                    "gasPrice": self.web3.from_wei(int(txn["gasPrice"]), "gwei"),
                    "blockNumber": int(txn["blockNumber"])
                }
                for txn in paginated_transactions
            ]
        }

    async def _get_transaction_info(self, txn_detail: dict, status: int) -> dict:
        """
        Get transaction details
        """
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to blockchain node")

        value_in_wei = txn_detail.get("value", 0)

        value_in_eth = self.web3.from_wei(value_in_wei, 'ether')

        block_hash = txn_detail.get('blockHash')
        block = self.web3.eth.get_block(block_hash)
        timestamp = block.get('timestamp')
        transaction_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # noqa

        return {
            "blockNumber": txn_detail.get("blockNumber"),
            "transaction_time": transaction_time,
            "status": status,
            "from": txn_detail.get("from"),
            "to": txn_detail.get("to"),
            "gas": txn_detail.get("gas"),
            "value_in_eth": value_in_eth
        }
