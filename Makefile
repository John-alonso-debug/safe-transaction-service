

################################################################################################

run-celery-beat:
	docker-compose -f ./compose-prod-worker-01-beat.yml up -d
	docker-compose -f ./compose-prod-worker-01-beat.yml logs -f

stop-celery-beat:
	docker-compose -f ./compose-prod-worker-01-beat.yml down


################################################################################################




################################################################################################


