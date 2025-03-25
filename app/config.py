from environs import Env

env = Env()
env.read_env()

POSTGRES_DB = env('POSTGRES_DB')
POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
POSTGRES_HOST = env('POSTGRES_HOST')
POSTGRES_PORT = env('POSTGRES_PORT')

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

TRON_API_KEY = env('TRON_API_KEY')
