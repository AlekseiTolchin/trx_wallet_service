from pydantic import BaseModel, Field


class WalletAddress(BaseModel):
    address: str


class WalletInfoResponse(BaseModel):
    balance: int
    bandwidth: int
    energy: int


class WalletInfoDB(BaseModel):
    balance: float
    bandwidth: int
    energy: int
