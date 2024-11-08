SHELL := /bin/bash

include .env

.EXPORT_ALL_VARIABLES:

minio_up:
	cd infrastructure/minio && docker-compose up -d

minio_down:
	cd infrastructure/minio && docker-compose down

clickhouse_up:
	cd infrastructure/clickhouse && docker-compose up -d

clickhouse_down:
	cd infrastructure/clickhouse && docker-compose down

mongodb_up:
	cd infrastructure/mongodb && docker-compose up -d

mongodb_down:
	cd infrastructure/mongodb && docker-compose down