### To setup project

1. Install docker with docker compose
2. Setup .env file. Default values are:
```DATABASE_NAME=dbname
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpass
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
TWEET_MAX_LENGTH=500
```
3. run `docker-compose up`

docker-compose exec fastapi alembic init -t async migrations
docker-compose exec fastapi alembic revision --autogenerate -m "init"
docker-compose exec fastapi alembic revision --autogenerate -m "init_db"
docker-compose exec fastapi alembic upgrade head