from typing import Annotated
import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.async_tron import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider
from tronpy.exceptions import AddressNotFound, BadAddress

from app.backend.db_depends import get_db
from app.models.wallets import WalletQuery
from app.config import TRON_API_KEY
from app.schemas import WalletAddress, WalletInfoResponse


router = APIRouter()


async def get_wallet_info(wallet_address: WalletAddress) -> WalletInfoResponse:
    provider = AsyncHTTPProvider(api_key=TRON_API_KEY)
    async with AsyncTron(provider=provider) as client:
        tasks = [
            client.get_account_resource(wallet_address),
            client.get_account_balance(wallet_address),
            client.get_bandwidth(wallet_address),
            client.get_account(wallet_address)
        ]

        results = await asyncio.gather(*tasks)

    account_resource, balance, bandwidth, account_info = results
    energy = account_resource['EnergyLimit']
    address = account_info['address']

    return WalletInfoResponse(
        address=address,
        balance=balance,
        bandwidth=bandwidth,
        energy=energy
    )


@router.post('/wallets/info', status_code=status.HTTP_200_OK)
async def create_wallet_info(
        db: Annotated[AsyncSession, Depends(get_db)],
        wallet_address: WalletAddress) -> dict:
    try:
        wallet_params = await get_wallet_info(wallet_address.address)

        await db.execute(
            insert(WalletQuery).values(
                address=wallet_params.address,
                balance=wallet_params.balance,
                bandwidth=wallet_params.bandwidth,
                energy=wallet_params.energy,
            )
        )
        await db.commit()

        return {
            'wallet_address': wallet_params.address,
            'wallet_balance': wallet_params.balance,
            'wallet_bandwidth': wallet_params.bandwidth,
            'wallet_energy': wallet_params.energy,
            'status_code': status.HTTP_200_OK,
        }

    except AddressNotFound:
        raise HTTPException(
            status_code=404,
            detail='Wallet address not found')
    except BadAddress:
        raise HTTPException(
            status_code=400,
            detail='Invalid wallet address format')


@router.get('/wallets/list', response_model=Page[WalletInfoResponse])
async def get_wallet_list(
        db: Annotated[AsyncSession, Depends(get_db)],
        params: Params = Depends()) -> Page[WalletInfoResponse]:
    wallet_queries = select(WalletQuery)
    return await paginate(db, wallet_queries, params)
