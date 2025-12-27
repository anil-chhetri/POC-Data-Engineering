# -------------------------
# Docker Compose Commands
# -------------------------
help:
	@echo "Available commands:"
	@echo "  make dbt      - Build and start the dbt services"
	@echo "  make kafka    - Build and start the Kafka services"
	@echo "  make down     - Stop and remove all services and networks"
	@echo "  make ps       - List running services"

dbt:
	docker compose -f docker-compose.dbt.yml up --build --force-recreate --wait

kafka:
	docker compose -f docker-compose.yml up --build --force-recreate --wait

down:
	docker compose down --volumes --remove-orphans
	docker network prune -f

ps:
	docker compose ps

.PHONY: help dbt kafka down ps