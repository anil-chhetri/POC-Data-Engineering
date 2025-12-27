# -------------------------
# Docker Compose Commands
# -------------------------
help:
	@echo "make compose-up-dbt        - Build and start dbt services"
	@echo "make compose-up-kafka      - Build and start Kafka services"
	@echo "make compose-clean         - Stop and remove all services, volumes, and orphan containers"
	@echo "make compose-build         - Build all services defined in the Docker Compose files"
	@echo "make compose-ps            - List the status of all services"


compose-up-dbt:
	docker compose -f docker-compose-dbt.yml --build --force-recreate --wait

compose-up-kafka:
	docker compose -f docker-compose.yml --build --force-recreate --wait

compose-clean:
	docker compose down --volumes --remove-orphans
	docker network prune -f

compose-build:
	docker compose build

compose-ps:
	docker compose ps

.PHONY: compose-up-dbt compose-up-kafka compose-clean compose-build compose-ps