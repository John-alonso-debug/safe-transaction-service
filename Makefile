

################################################################################################

run-infra:
	docker-compose -f ./compose-prod-infra.yml up -d
	docker ps

run-base:
	docker-compose -f ./compose-prod-base.yml up -d
	docker ps


run-nginx:
	docker-compose -f ./compose-prod-lb.yml up -d
	docker ps

run-worker:
	docker-compose -f ./compose-prod-worker.yml up -d
	docker-compose -f ./compose-prod-worker.yml logs -f

run-all: run-infra run-base run-nginx run-worker



build-worker:
	docker-compose -f ./compose-prod-worker.yml build


################################################################################################

stop-all:
	docker-compose -f ./compose-prod-worker.yml down --remove-orphans
	docker-compose -f ./compose-prod-lb.yml down --remove-orphans
	docker-compose -f ./compose-prod-base.yml down --remove-orphans
	#
	docker-compose -f ./compose-prod-infra.yml down --remove-orphans
	docker ps

stop-worker:
	docker-compose -f ./compose-prod-worker.yml down  --remove-orphans
	docker ps

stop-server:
	docker-compose -f ./compose-prod-base.yml down  --remove-orphans
	docker ps

stop-infra:
	docker-compose -f ./compose-prod-infra.yml down --remove-orphans
	docker ps

build-all:
	docker-compose -f ./compose-prod-worker.yml build --force-rm
	docker-compose -f ./compose-prod-lb.yml build --force-rm
	docker-compose -f ./compose-prod-base.yml build --force-rm
	#
	docker-compose -f ./compose-prod-infra.yml build --force-rm
	docker images


################################################################################################

log-server:
	docker-compose -f ./compose-prod-base.yml logs -f

log-worker:
	docker-compose -f ./compose-prod-worker.yml logs -f


stop-old:
	docker-compose -f ./docker-compose.yml down
	docker ps
