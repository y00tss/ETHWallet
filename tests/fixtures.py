import pytest
from schemas.wallet import CurrencyType
from services.wallet.wallet_flow.eth_flow import EthWalletService
from unittest.mock import MagicMock


@pytest.fixture
def eth_wallet_service_kwargs():
    return {
        "contract_address": "sdgsdsfgdsadfg",
    }


@pytest.fixture
def tron_currency():
    return CurrencyType.TRX


@pytest.fixture
def eth_currency():
    return CurrencyType.ETH


@pytest.fixture
def eth_wallet_service():
    return EthWalletService(address="0x57b48c461b323Fc9B6CEFcA5878Ba6Bf95E6E8c5", contract_address=None)


@pytest.fixture
def mock_eth_wallet_service():
    wallet_service = MagicMock(spec=EthWalletService)
    wallet_service.get_balance.return_value = 10.0
    wallet_service.get_transactions.return_value = {
        "total": 1,
        "transactions": [
            {
                "hash": "0x123",
                "from": "0xFromAddress",
                "to": "0xToAddress",
                "value": "1.0 ETH",
                "gas": 21000,
                "gasPrice": "20 gwei",
                "blockNumber": 123456
            }
        ]
    }
    return wallet_service


@pytest.fixture
def transaction_hash():
    return "0x52514eee9112b68bb60858cb589602fb28ee10ae0d18fde07ad0faa50747721f"