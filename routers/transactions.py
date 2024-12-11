from fastapi import (
    APIRouter, Depends,
    Query, Path
)
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from repository.wallet import WalletRepository
from services.utils.base_config import current_user
from schemas.wallet import CurrencyRequest, CurrencyType
from database.database import get_async_session
from services.exceptions.exceptions import ExceptionHandler
from services.wallet.wallet_flow import WalletFlow

router = APIRouter()


@router.get("/{wallet_id}", status_code=200)
async def get_address(
        wallet_id: int = Path(..., description="Input wallet ID for receiving the address"), # noqa
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Get address of the wallet for depositing
    """
    try:
        wallet = await WalletRepository(session).get_by_id(id=wallet_id, user_id=user.id) # noqa
        return {"address": wallet.address, "currency": wallet.currency}
    except Exception as e:
        ExceptionHandler.handle(e)


@router.get("/{wallet_id}/transactions", status_code=200)
async def get_transactions(
        wallet_id: int = Path(..., description="Input wallet ID for receiving following transactions"), # noqa
        limit: int = Query(10, ge=1, le=100, description="Number of transactions"),
        offset: int = Query(0, ge=0, description="Offset for pagination"),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Get transactions for a wallet with pagination
    """
    try:
        # Validate wallet ownership
        wallet = await WalletRepository(session).get_by_id(id=wallet_id, user_id=user.id) # noqa

        wallet_service = WalletFlow.get_wallet_service(
            currency=wallet.currency, address=wallet.address
        )

        return await wallet_service.get_transactions(limit=limit, offset=offset)

    except Exception as e:
        ExceptionHandler.handle(e)


@router.post("/{wallet_id}/send")
async def send_transaction(
        wallet_id: int,  # wallet_id from which transaction will be sent
        to_address: str,
        amount: float,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Send transaction from wallet
    """
    try:
        wallet = await WalletRepository(session).get_by_id(id=wallet_id, user_id=user.id) # noqa
        wallet_service = WalletFlow.get_wallet_service(
            currency=wallet.currency, address=wallet.address
        )
        txn_hash = await wallet_service.send_transaction(
            to_address=to_address, amount=amount, private_key=wallet.private_key
        )
        return {"transaction_hash": txn_hash}
    except Exception as e:
        ExceptionHandler.handle(e)


@router.post("/{hash}")
async def get_transaction_data(
        hash: str,
        currency_request: CurrencyRequest,
):
    """
    Get the transaction data
    """
    try:
        currency_enum = CurrencyType(currency_request.currency)
        wallet_service = WalletFlow.get_wallet_service(currency=currency_enum)

        return await wallet_service.get_transaction_receipt(hash)

    except Exception as e:
        ExceptionHandler.handle(e)
