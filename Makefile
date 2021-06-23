

################################################################################################

run-infra:
	docker-compose -f ./compose-prod-infra.yml up -d

run-base:
	docker-compose -f ./compose-prod-base.yml up -d

run-nginx:
	docker-compose -f ./compose-prod-lb.yml up -d

run-worker:
	docker-compose -f ./compose-prod-worker.yml up -d
	docker-compose -f ./compose-prod-worker.yml logs -f

run-all: run-infra run-base run-nginx run-worker




################################################################################################

stop-all:
	docker-compose -f ./compose-prod-worker.yml down
	docker-compose -f ./compose-prod-lb.yml down
	docker-compose -f ./compose-prod-base.yml down
	#
	docker-compose -f ./compose-prod-infra.yml down
	docker ps


################################################################################################

log-server:
	docker-compose -f ./compose-prod-base.yml logs -f

log-worker:
	docker-compose -f ./compose-prod-worker.yml logs -f
