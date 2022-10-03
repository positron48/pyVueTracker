pwd=$(shell pwd)
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
build: ## build front
	docker run --rm -v ${pwd}:/app -w /app/frontend node:14 /bin/bash -c "npm install && npm run build"
start: ## start server
	docker-compose up -d
stop: ## stop server
	docker-compose down
restart: stop start ## restart server
