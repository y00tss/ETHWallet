from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class CurrencyType(str, Enum):
    ETH = "ETH"
    TRX = "Tron"


class WalletType(str, Enum):
    HDWallet = "HDWallet"
    AnotherWallet = "AnotherWallet"


class WalletCreateRequest(BaseModel):
    currency: CurrencyType
    wallet_type: WalletType


class WalletResponse(BaseModel):
    address: str
    currency: str
    created_at: datetime

    class Config:
        orm_mode = True


class CurrencyRequest(BaseModel):
    currency: CurrencyType
