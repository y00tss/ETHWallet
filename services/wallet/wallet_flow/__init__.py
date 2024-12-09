from services.wallet.wallet_flow.eth_flow import EthWalletService
from models.wallet import CurrencyType


class WalletFlow:
    @staticmethod
    def get_wallet_service(currency: CurrencyType, **kwargs):
        print(f"Getting wallet service for currency: {currency}")
        if currency.value == CurrencyType.ETH.value:
            return EthWalletService(**kwargs)
        else:
            raise NotImplementedError(f"Currency: {currency.value} not supported")
