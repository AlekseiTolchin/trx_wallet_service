from typing import Annotated, List
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import insert, select, update
from fastapi import APIRouter, Depends, HTTPException, status
from tronpy.async_tron import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound, ApiError

from app.backend.db_depends import get_db
from app.models.wallets import WalletQuery
from app.config import TRON_API_KEY
from app.schemas import WalletAddress, WalletInfoDB, WalletInfoResponse


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
async def wallet_info(db: Annotated[AsyncSession, Depends(get_db)], wallet: WalletAddress):
    try:
        wallet_params = await get_wallet_info(wallet.address)
        wallet_info_db = WalletInfoDB(**wallet_params)

        await db.execute(
            insert(WalletQuery).values(
                balance=wallet_info_db.balance,
                bandwidth=wallet_info_db.bandwidth,
                energy=wallet_info_db.energy,
            )
        )
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }

    except AddressNotFound:
        raise HTTPException(status_code=404, detail="Wallet address not found")


@router.get('/wallets', response_model=Page[WalletInfoResponse])
async def get_wallet_list(db: Annotated[AsyncSession, Depends(get_db)], params: Params = Depends()):
    wallet_queries = select(WalletQuery)
    return await paginate(db, wallet_queries, params)
