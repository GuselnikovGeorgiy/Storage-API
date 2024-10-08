# Разработка API для управления складом

## ТЗ

* Разработать RESTAPI с использованием FastAPI для управления процессами на складе.
* API должно управлять товарами, складскими запасами и заказами.
* Использовать SQLAlchemy 2 версии для взаимодействия с PostgreSQL.
* Реализовать эндпоинты для товаров: создание, получение, обновление, удаление.
* Реализовать эндпоинты для заказов: создание, получение, обновление.
* При создании заказа проверять наличие достаточного количества товара на складе, 
обновлять количество товара на складе при создании заказа. Возвращать ошибки с соответствующими сообщениями

## Необходимые инструменты

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Poetry](https://pypi.org/project/poetry/)

## Запуск в Docker
1. **Склонировать репозиторий:**

   ```bash
   git clone https://github.com/GuselnikovGeorgiy/Storage-API.git
   cd your_repository
   ```

2. Установить Docker, Docker-compose, Makefile пакеты.

3. Создать в корневой папке проекта файл `.env`, в котором нужно задать 
переменные окружения, по аналогии с файлом `.env.example`
```
MODE=DEV

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres

TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=postgres
TEST_DB_PASS=postgres
TEST_DB_NAME=test_db
```
Аналогично сделать для .env-non-dev.

### Реализованные команды

* **`make all` - поднять приложение**
* **`make all-down` - остановить приложение**

* `make app-logs` - посмотреть логи в контейнере с приложением
* `make db-logs` - посмотреть логи в контейнере с базой
* `make app-shell` - зайти в баш-консоль контейнера с приложением

4. Запустить контейнеры с приложением
```bash
   make all
```

##    Запуск локально

1. Склонировать репозиторий
2. Создайте файлы .env и заполните его исходя из .env.example
3. Установить poetry ```pip install poetry```
4. Создайте и активируйте виртуальное окружение ```python3 -m venv venv & source venv/bin/activate```
5. Установите пакеты из poetry ```poetry install```
6. Создайте базу с параметрами, введенными в .env
- Опционально: создайте тестовую базу
  - Прогнать тесты можно командой ```pytest```
7. Запустите приложение ```uvicorn app.main:create_app --host 127.0.0.1 --port 8000 --reload```

