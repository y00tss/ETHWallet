from services.wallet.wallet_flow.eth_flow import EthWalletService
from models.wallet import CurrencyType


class WalletFlow:
    @staticmethod
    def get_wallet_service(currency: CurrencyType, **kwargs):
        if currency.value == CurrencyType.ETH.value:
            return EthWalletService(**kwargs)
        else:
            raise NotImplementedError(f"Currency: {currency.value} not supported")
