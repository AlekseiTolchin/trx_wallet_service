from environs import Env

env = Env()
env.read_env()


TRON_API_KEY = env('TRON_API_KEY')