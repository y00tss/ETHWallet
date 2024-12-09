import pytest
from tests.fixtures import (
    eth_currency, eth_wallet_service_kwargs,
    eth_wallet_service, mock_eth_wallet_service,
    transaction_hash
)


@pytest.mark.asyncio
async def test_get_balance(mock_eth_wallet_service):
    """Get balance from mock wallet service"""
    balance = await mock_eth_wallet_service.get_balance()
    assert balance == 10.0


@pytest.mark.asyncio
async def test_get_balance_real(eth_wallet_service):
    """Get balance from real wallet service"""
    balance = await eth_wallet_service.get_balance()
    assert balance < 0.5


@pytest.mark.asyncio
async def test_get_transactions(mock_eth_wallet_service):
    """Get transactions from mock wallet service"""
    transactions = await mock_eth_wallet_service.get_transactions()
    assert transactions["total"] == 1
    assert transactions["transactions"][0]["hash"] == "0x123"
    assert transactions["transactions"][0]["from"] == "0xFromAddress"
    assert transactions["transactions"][0]["to"] == "0xToAddress"
    assert transactions["transactions"][0]["value"] == "1.0 ETH"
    assert transactions["transactions"][0]["gas"] == 21000
    assert transactions["transactions"][0]["gasPrice"] == "20 gwei"
    assert transactions["transactions"][0]["blockNumber"] == 123456


@pytest.mark.asyncio
async def test_get_transaction_receipt(transaction_hash, eth_wallet_service):
    """Get transaction receipt from my REAL transaction hash"""
    result = await eth_wallet_service.get_transaction_receipt(transaction_hash)

    assert result["status"] == "success", "Status should be 'success'"
    assert result["blockNumber"] == 15840565, "Block number should be 15840565"
    assert result["to"] == "0xaBEA9132b05A70803a4E85094fD0e1800777fBEF", "To address should match"
    assert result["transaction_time"] == "2022-10-27 16:20:35", "Transaction time should match"
