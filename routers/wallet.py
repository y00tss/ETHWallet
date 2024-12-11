from fastapi import (
    APIRouter, Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.wallet import WalletCreateRequest, WalletResponse
from repository.wallet import WalletRepository
from services.utils.base_config import current_user
from services.wallet.builder import WalletMapper
from database.database import get_async_session
from services.exceptions.exceptions import ExceptionHandler
from services.wallet.wallet_flow import WalletFlow

router = APIRouter()


@router.get("/", status_code=200)
async def get_wallets(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Get all wallets related to user
    """
    try:
        return await WalletRepository(session).get_all(user_id=user.id)
    except Exception as e:
        ExceptionHandler.handle(e)


@router.get("/{id}", response_model=WalletResponse)
async def get_wallet_by_id(
        id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Get wallet by id
    """
    try:
        return await WalletRepository(session).get_by_id(id=id, user_id=user.id)
    except Exception as e:
        ExceptionHandler.handle(e)


@router.get("/{id}/balance")
async def get_wallet_balance(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Get wallet balance
    """
    try:
        wallet = await WalletRepository(session).get_by_id(id=id, user_id=user.id)

        balance = await WalletFlow.get_wallet_service(
            currency=wallet.currency, address=wallet.address
        ).get_balance()

        return {"balance": balance}

    except Exception as e:
        ExceptionHandler.handle(e)


@router.post("/", status_code=201)
async def create_wallet(
        wallet_request: WalletCreateRequest,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Create wallet
    """
    try:
        wallet_data = WalletMapper.get_wallet_builder(
            wallet_type="HD", currency=wallet_request.currency
        )
        wallet_data.update(wallet_request.dict())
        valid_wallet_data = {
            key: wallet_data[key]
            for key in ["user_id", "address", "currency", "wallet_type", "balance", "created_at", "private_key"]  # noqa
            if key in wallet_data
        }
        valid_wallet_data["user_id"] = user.id

        wallet = await WalletRepository(session).create(valid_wallet_data)
        return wallet
    except Exception as e:
        ExceptionHandler.handle(e)


@router.delete("/{id}")
async def delete_wallet(
        id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Delete wallet by id
    """
    try:
        await WalletRepository(session).delete(id=id, user_id=user.id)
        return {"detail": "Wallet deleted"}
    except Exception as e:
        ExceptionHandler.handle(e)
