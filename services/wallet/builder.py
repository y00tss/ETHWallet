"""
Wallet Builder
"""
from bip_utils import (
    Bip39MnemonicGenerator,  # Генератор мнемоники
    Bip39SeedGenerator,  # Генератор seed из мнемоники
    Bip44,  # Алгоритм BIP-44
    Bip44Coins  # Список поддерживаемых валют
)
from typing import Dict


class WalletMapper:

    @staticmethod
    def get_wallet_builder(wallet_type: str, **kwargs) -> Dict[str, str]:
        match wallet_type:
            case "HD":
                return HDWalletBuilder.build(**kwargs)
            case "Simple":
                return AnotherWalletBuilder.build(**kwargs)
            case _:
                raise ValueError("Invalid wallet type")


class HDWalletBuilder:
    """Builder for HD wallets"""

    @staticmethod
    def build(currency: str) -> Dict[str, str]:
        """
        :param currency
        :return: dict
        """
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
        seed = Bip39SeedGenerator(mnemonic).Generate()

        coin_map = {
            "eth": Bip44Coins.ETHEREUM,
            "bnb": Bip44Coins.BINANCE_CHAIN,
            "trx": Bip44Coins.TRON,
        }

        coin = coin_map.get(currency.lower())
        if not coin:
            raise ValueError(f"Unsupported currency: {currency}")

        bip44_wallet = Bip44.FromSeed(seed, coin)
        address = bip44_wallet.PublicKey().ToAddress()
        private_key = bip44_wallet.PrivateKey().Raw().ToHex()

        return {
            "mnemonic": mnemonic,
            "address": address,
            "private_key": private_key,
        }

    @staticmethod
    def delete():
        pass


class AnotherWalletBuilder:
    """Builder for simple wallets"""

    @staticmethod
    def build(currency: str) -> Dict[str, str]:
        raise NotImplementedError("Simple wallet generation is not implemented yet.")

    @staticmethod
    def delete():
        raise NotImplementedError("Simple wallet deletion is not implemented yet.")
