from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routes import wallets


app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Tron'}


app.include_router(wallets.router)
add_pagination(app)
