.PHONY: help start stop restart logs clean build

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

start: ## Start all services
	@echo "🚀 Starting Intelligent Development Platform..."
	@mkdir -p models grafana/dashboards grafana/provisioning/datasources grafana/provisioning/dashboards
	@docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 15
	@echo "✅ Platform is ready!"
	@echo "📊 Grafana: http://localhost:3000 (admin/admin)"
	@echo "🔧 Intelligence Engine: http://localhost:8000"
	@echo "📖 API Docs: http://localhost:8000/docs"

stop: ## Stop all services
	@echo "🛑 Stopping Intelligent Development Platform..."
	@docker-compose down

restart: ## Restart all services
	@echo "🔄 Restarting Intelligent Development Platform..."
	@docker-compose restart

logs: ## Show logs from all services
	@docker-compose logs -f

logs-engine: ## Show logs from intelligence engine
	@docker-compose logs -f intelligence-engine

logs-collector: ## Show logs from data collector
	@docker-compose logs -f data-collector

logs-grafana: ## Show logs from Grafana
	@docker-compose logs -f grafana

build: ## Build all Docker images
	@echo "🏗️  Building Docker images..."
	@docker-compose build

clean: ## Remove all containers, volumes, and data
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@rm -rf models/*.pkl models/*.joblib
	@echo "✅ Cleanup complete!"

status: ## Check status of all services
	@docker-compose ps

shell-engine: ## Open shell in intelligence engine container
	@docker-compose exec intelligence-engine /bin/bash

shell-collector: ## Open shell in data collector container
	@docker-compose exec data-collector /bin/bash

pull: ## Pull latest images
	@docker-compose pull

test: ## Run basic health checks
	@echo "🧪 Running health checks..."
	@curl -s http://localhost:8000/health || echo "❌ Intelligence Engine not responding"
	@curl -s http://localhost:3000/api/health || echo "❌ Grafana not responding"
	@curl -s http://localhost:9090/-/healthy || echo "❌ Prometheus not responding"
	@echo "✅ Health checks complete!"

