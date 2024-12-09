# import pytest
# from bip_utils import Bip44Coins
# from services.wallet.builder import WalletMapper, HDWalletBuilder
#
#
# @pytest.fixture
# def create_hd_wallet():
#     currency = "eth"
#     wallet = HDWalletBuilder.build(currency)
#     return wallet
#
#
# def test_hd_wallet_builder_and_mapper_should_success(create_hd_wallet):
#     wallet = create_hd_wallet
#
#     assert "mnemonic" in wallet
#     assert "address" in wallet
#     assert "private_key" in wallet
#
#     assert wallet["address"]
#     assert wallet["private_key"]
#
#     coin_map = {
#         "eth": Bip44Coins.ETHEREUM,
#         "bnb": Bip44Coins.BINANCE_CHAIN,
#         "trx": Bip44Coins.TRON,
#     }
#     coin = coin_map.get("eth")
#     assert coin == Bip44Coins.ETHEREUM
#
#
# def test_wallet_mapper():
#     wallet_data = WalletMapper.get_wallet_builder(wallet_type="HD", currency="eth")
#
#     assert "mnemonic" in wallet_data
#     assert "address" in wallet_data
#     assert "private_key" in wallet_data
#
#     with pytest.raises(ValueError, match="Invalid wallet type"):
#         WalletMapper.get_wallet_builder(wallet_type="InvalidType", currency="eth")
#
#     wallet_bnb = WalletMapper.get_wallet_builder(wallet_type="HD", currency="bnb")
#     wallet_trx = WalletMapper.get_wallet_builder(wallet_type="HD", currency="trx")
#
#     assert wallet_bnb["address"]
#     assert wallet_trx["address"]
#
#     with pytest.raises(ValueError, match="Unsupported currency"):
#         WalletMapper.get_wallet_builder(wallet_type="HD", currency="unsupported_currency")