import pytest
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallets import WalletQuery


@pytest.mark.asyncio
async def test_insert_wallet_query(async_session: AsyncSession, create_test_database):
    wallet_data = {
        'address': 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g',
        'balance': 1000,
        'bandwidth': 2000,
        'energy': 3000,
    }

    await async_session.execute(
        insert(WalletQuery).values(**wallet_data)
    )
    await async_session.commit()

    result = await async_session.execute(select(WalletQuery))
    wallet = result.scalars().first()

    assert wallet.address == 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g'
    assert wallet.balance == 1000
    assert wallet.bandwidth == 2000
    assert wallet.energy == 3000
