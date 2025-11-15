#!/bin/bash

echo "🚀 Starting Intelligent Development Platform..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p models
mkdir -p grafana/dashboards
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards

# Pull images
echo "📦 Pulling Docker images..."
docker-compose pull

# Start services
echo "🔧 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

services=("grafana:3000" "mimir:9009" "loki:3100" "tempo:3200" "intelligence-engine:8000" "postgres:5432")
for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if docker-compose ps | grep -q "$name.*Up"; then
        echo "✅ $name is running"
    else
        echo "❌ $name is not running"
    fi
done

echo ""
echo "🎉 Intelligent Development Platform is ready!"
echo ""
echo "📊 Access points:"
echo "   - Grafana:             http://localhost:3000 (admin/admin)"
echo "   - Intelligence Engine: http://localhost:8000"
echo "   - API Docs:            http://localhost:8000/docs"
echo "   - Prometheus:          http://localhost:9090"
echo ""
echo "📖 Quick commands:"
echo "   - View logs:    docker-compose logs -f"
echo "   - Stop:         docker-compose down"
echo "   - Restart:      docker-compose restart"
echo ""
echo "💡 Check README.md for usage examples and documentation"
echo ""

