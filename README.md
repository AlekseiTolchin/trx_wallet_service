# Микросервис для сети TRON

Микросервис, который выводит информацию по адресу кошелька в сети TRON.

## Как запустить проект

Скачать удаленный репозиторий выполнив команду

```
git clone https://github.com/AlekseiTolchin/trx_wallet_service
```
Docker и Docker-compose должны быть установлены в системе.

В корневой директории проекта создать файл `.env` со следующими настройками:

- `POSTGRES_DB`= tron_db
- `POSTGRES_USER`= tron
- `POSTGRES_PASSWORD`= tron
- `POSTGRES_PORT`= 5432
- `POSTGRES_HOST`= db
- `TEST_DATABASE_URL`= sqlite+aiosqlite:///./test.db
- `TRON_API_KEY`= токен разработчика [developers.tron.network/](https://developers.tron.network/)

Запустить команды:

```
docker-compose build
```

```
docker-compose up
```

Запустить тесты:

```
docker-compose exec web pytest
```

Ссылки для тестирования:

http://127.0.0.1:8000/docs/ - `документация API`  

При написании кода и тестировании использовался адрес кошелька из официальной документации
API - `TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g`
