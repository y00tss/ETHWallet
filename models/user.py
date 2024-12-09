from datetime import datetime
from database.database import Base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column, Integer, String,
    TIMESTAMP, Boolean, MetaData
)

metadata = MetaData()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    wallets = relationship("Wallet", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
