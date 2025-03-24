from pydantic import BaseModel


class WalletInfo(BaseModel):
    address: str
