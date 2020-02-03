

clean:
	docker-compose down

up:
	docker-compose up

models:
	docker-compose -f docker-compose.yml -f docker-compose-models.yml up