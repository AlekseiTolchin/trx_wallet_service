import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app as fastapi_app
from app.models.wallets import WalletQuery
from app.backend.db_depends import get_db
from app.schemas import WalletInfoResponse, WalletAddress


@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture
def override_get_db(async_session):
    async def _get_test_db():
        try:
            yield async_session
        finally:
            await async_session.close()
    return _get_test_db


@pytest.fixture
def test_app(app, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


async def mock_get_wallet_info(wallet_address: WalletAddress) -> WalletInfoResponse:
    return WalletInfoResponse(
        address='TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g',
        balance=1000,
        bandwidth=2000,
        energy=3000,
    )


@pytest.mark.asyncio
async def test_create_wallet(test_client, monkeypatch, async_session: AsyncSession, create_test_database):
    monkeypatch.setattr('app.routes.wallets.get_wallet_info', mock_get_wallet_info)

    response = test_client.post('/wallets', json={'address': 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g'})

    assert response.status_code == 200
    assert response.json() == {
        'wallet_address': 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g',
        'wallet_balance': 1000,
        'wallet_bandwidth': 2000,
        'wallet_energy': 3000,
        'status_code': 200,
    }

    result = await async_session.execute(select(WalletQuery))
    wallet = result.scalars().first()

    assert wallet.address == 'TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g'
    assert wallet.balance == 1000
    assert wallet.bandwidth == 2000
    assert wallet.energy == 3000
