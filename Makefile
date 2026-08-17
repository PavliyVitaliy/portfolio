COMPOSE ?= docker compose

.PHONY: up stop down logs test frontend-build production-up production-stop

up:
	$(COMPOSE) up --detach --build

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs --follow

test:
	$(COMPOSE) -f docker-compose.test.yaml up --detach portfolio-mongo-db-test
	$(COMPOSE) -f docker-compose.test.yaml run --rm --no-deps --build portfolio-backend-test pytest
	$(COMPOSE) -f docker-compose.test.yaml stop portfolio-mongo-db-test

frontend-build:
	cd frontend && npm run build

production-up:
	$(COMPOSE) -f docker-compose.production.yaml up --detach --build

production-stop:
	$(COMPOSE) -f docker-compose.production.yaml stop
