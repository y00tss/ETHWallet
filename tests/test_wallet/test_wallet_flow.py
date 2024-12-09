import pytest
from services.wallet.wallet_flow import WalletFlow
from services.wallet.wallet_flow.eth_flow import EthWalletService
from tests.fixtures import eth_wallet_service_kwargs, tron_currency, eth_currency


def test_get_wallet_service_for_eth(eth_wallet_service_kwargs, eth_currency):
    wallet_service = WalletFlow.get_wallet_service(eth_currency, **eth_wallet_service_kwargs)

    assert isinstance(wallet_service, EthWalletService)


def test_wallet_service_for_unsupported_currency(tron_currency):
    with pytest.raises(NotImplementedError):
        WalletFlow.get_wallet_service(tron_currency)
