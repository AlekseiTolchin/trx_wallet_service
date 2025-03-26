from pydantic import BaseModel, Field, field_validator
import re


class WalletAddress(BaseModel):
    address: str = Field(..., description='The wallet address')

    @field_validator('address')
    @classmethod
    def validate_tron_address(cls, v: str) -> str:
        if not re.match(r'^T[A-Za-z1-9]{33}$', v):
            raise ValueError('Invalid wallet address format')
        return v


class WalletInfoResponse(BaseModel):
    address: str | None = Field(default=None, description='The wallet address')
    balance: float = Field(..., description='The wallet balance')
    bandwidth: int = Field(..., description='The wallet bandwidth')
    energy: int = Field(..., description='The wallet energy limit')
