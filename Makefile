pwd=$(shell pwd)
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
start: ## start server
	docker-compose up -d
stop: ## stop server
	docker-compose down
restart: stop start ## restart server
