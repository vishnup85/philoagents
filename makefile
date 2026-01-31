infrastructure-up:
	docker compose up -d local_dev_atlas

infrastructure-api-up:
	docker compose up --build -d

check-docker-image:
	@if [ -z "$$(docker images -q philoagents-api 2> /dev/null)" ]; then \
		echo "Error: philoagents-api Docker image not found."; \
		echo "Please run 'make infrastructure-build' first to build the required images."; \
		exit 1; \
	fi

create-long-term-memory:
	@docker compose ps local_dev_atlas | grep -q "Up" || (echo "MongoDB service is not running. Starting it..." && docker compose up -d local_dev_atlas && sleep 5)
	cd philoagents-api && uv run python -m tools.create_long_term_memory

create-long-term-memory-docker:check-docker-image
	@docker compose ps local_dev_atlas | grep -q "Up" || (echo "MongoDB service is not running. Starting it..." && docker compose up -d local_dev_atlas && sleep 5)
	docker run --rm --network philoagents-network --env-file philoagents-api/.env -e MONGODB_URI=mongodb://philoagents:philoagents@local_dev_atlas:27017/?directConnection=true -v ./philoagents-api/data:/app/data philoagents-api uv run python -m tools.create_long_term_memory