pwd=$(shell pwd)
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

start: ## start server
	docker-compose up -d

stop: ## stop server
	docker-compose down

restart: stop start ## restart server

build: ## Build the Docker image
	docker-compose build

up: ## Start the development server
	docker-compose up

down: ## Stop the development server
	docker-compose down

rebuild: ## Rebuild and start the development server
	docker-compose up --build

install: ## Install dependencies or update the project
	docker-compose run web npm install

lint: ## Run linter
	docker-compose run web npm run lint

production-build: ## Build the project for production
	docker-compose run web npm run build

dev: ## Run the development server
	docker-compose run web npm run dev