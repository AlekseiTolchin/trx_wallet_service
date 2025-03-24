from typing import Annotated
import asyncio

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from tronpy.async_tron import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound, ApiError

from app.backend.db_depends import get_db
from app.config import TRON_API_KEY
from app.schemas import WalletInfo


router = APIRouter()


async def get_wallet_info(wallet_address: str):
    provider = AsyncHTTPProvider(api_key=TRON_API_KEY)
    async with AsyncTron(provider=provider) as client:
        tasks = [
            client.get_account_resource(wallet_address),
            client.get_account_balance(wallet_address),
            client.get_bandwidth(wallet_address),
        ]

        results = await asyncio.gather(*tasks)

    account_resource, balance, bandwidth = results
    energy = account_resource['EnergyLimit']

    return {
        'balance': balance,
        'bandwidth': bandwidth,
        'energy': energy,
    }


@router.post('/wallets')
async def wallet_info(wallet_address: WalletInfo):

    try:
        wallet_params = await get_wallet_info(wallet_address.address)
        return wallet_params

    except AddressNotFound:
        raise HTTPException(status_code=404, detail="Wallet address not found")
