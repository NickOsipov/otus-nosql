SHELL := /bin/bash

include .env

.EXPORT_ALL_VARIABLES:

minio_up:
	cd infra/minio && docker-compose up -d

minio_down:
	cd infra/minio && docker-compose down

clickhouse_up:
	cd infra/clickhouse && docker-compose up -d

clickhouse_down:
	cd infra/clickhouse && docker-compose down

mongodb_up:
	cd infra/mongodb && docker-compose up -d

mongodb_down:
	cd infra/mongodb && docker-compose down