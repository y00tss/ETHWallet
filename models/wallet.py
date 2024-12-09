from datetime import datetime
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, Integer, String,
    TIMESTAMP, ForeignKey,
    MetaData

)

metadata = MetaData()


class CurrencyType(PyEnum):
    ETH = "ETH"
    TRX = "Tron"


class WalletType(PyEnum):
    HDWallet = "HDWallet"
    AnotherWallet = "AnotherWallet"


class StatusType(PyEnum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    address = Column(String, unique=True, index=True, nullable=False)
    currency = Column(Enum(CurrencyType), nullable=False)
    private_key = Column(String, nullable=True)
    wallet_type = Column(Enum(WalletType), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="wallets")

    def __repr__(self):
        return f"<Wallet {self.address}>"
