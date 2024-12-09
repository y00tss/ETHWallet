from repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from models.wallet import Wallet


class WalletRepository(BaseRepository[Wallet]):
    def __init__(self, session: AsyncSession):
        super().__init__(Wallet, session)
