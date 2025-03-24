from fastapi import FastAPI

from app.routers import wallets


app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Tron'}


app.include_router(wallets.router)
