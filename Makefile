app:
	docker-compose -f docker-compose.yaml stop
	docker-compose -f docker-compose.yaml build
	docker-compose -f docker-compose.yaml up

database:
	docker pull postgres:13
	docker stop psql1 || true
	docker rm psql1 || true
	docker run --name postgres-user-api -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres