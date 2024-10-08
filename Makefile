DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env-non-dev
APP_FILE = docker_compose/app.yml
DB_FILE = docker_compose/db.yml
APP_CONTAINER = main-app
DB_CONTAINER = postgres-db


.PHONY: all
all:
	${DC} -f ${DB_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: db
db:
	${DC} -f ${DB_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${DB_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: db-logs
db-logs:
	${LOGS} ${DB_CONTAINER} -f