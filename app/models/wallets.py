from sqlalchemy import Column, Integer, String

from app.backend.db import Base


class WalletQuery(Base):
    __tablename__ = 'wallet_queries'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    balance = Column(Integer)
    bandwidth = Column(Integer)
    energy = Column(Integer)
