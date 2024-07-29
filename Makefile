### Main commands

# Configure env var
env:
	cp -r .env.template .env

# Build and run docker containers 🐳
docker_build_and_run:
	docker-compose -f docker-compose.yaml --build

# Build and run without cache
docker_clean_build_and_run:
	docker-compose -f docker-compose.yaml build --no-cache
	make docker_run

# Run containers
docker_run:
	docker-compose -f docker-compose.yaml up

# Stop containers
docker_stop:
	docker-compose -f docker-compose.yaml stop

# Stop and remove containers with volumes
docker_down_and_clean_volumes:
	docker-compose -f docker-compose.yaml down -v

# Purge all cached docker data
docker_prune:
	docker container prune -f
	docker image prune --all -f 
	docker volume prune -f