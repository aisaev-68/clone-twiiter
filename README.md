## Twitter Clone

### Функциональные возможности:
1. Пользователь может добавить новый твит.
2. Пользователь может удалить свой твит.
3. Пользователь может зафоловить другого пользователя.
4. Пользователь может отписаться от другого пользователя.
5. Пользователь может отмечать твит как понравившийся.
6. Пользователь может убрать отметку «Нравится».
7. Пользователь может получить ленту из твитов отсортированных в
порядке убывания по популярности от пользователей, которых он
фоловит.
8. Твит может содержать картинку

### Переменные среды
Переименовать файл .env.example в .env и установите свои данные

### Команды для сборки и запуска

1. Соберрать образ и запустить сервис: 
```
docker-compose up -d --build
```
2. Инициализируйте данные: 
```
docker-compose exec webapp python db/init_db.py 
docker-compose restart
```
3. Просмотр статуса службы:
```
docker-compose ps -a
```

### Другие команды работы с docker

1. Перезапустить службу:
```
 docker-compose restart
```
2. Запустить службу:
```
docker-compose start <имя службы>
```
3. Остановить службу:
```
docker-compose stop <имя службы>
```
4. Закрыть службу и удалить контейнер:
```
docker container stop $(docker container ls -aq) &&  
docker container rm $(docker container ls -aq) &&  
docker system prune --all --volumes

```
docker-compose --file docker-compose-dev.yml up
docker-compose --file docker-compose-dev.yml up
docker-compose exec fastapi alembic upgrade head

docker-compose exec fastapi python initial_data.py
docker-compose exec fastapi pytest .
