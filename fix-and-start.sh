#!/bin/bash

echo "🔧 Fixing Intelligent Development Platform issues..."
echo ""

# Stop all services
echo "1. Stopping all services..."
docker-compose down

# Create necessary directories
echo "2. Creating necessary directories..."
mkdir -p models
mkdir -p grafana/dashboards
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p intelligence-engine/models
mkdir -p intelligence-engine/services
mkdir-p intelligence-engine/api

# Remove problematic volumes
echo "3. Cleaning problematic volumes..."
docker volume rm intelligent-developers-platform_tempo-data 2>/dev/null || true
docker volume rm intelligent-developers-platform_mimir-data 2>/dev/null || true
docker volume rm intelligent-developers-platform_loki-data 2>/dev/null || true

# Rebuild services
echo "4. Rebuilding services..."
docker-compose build intelligence-engine data-collector

# Start services
echo "5. Starting services..."
docker-compose up -d

# Wait for services
echo "6. Waiting for services to be ready (60 seconds)..."
sleep 60

# Check status
echo ""
echo "7. Checking service status..."
echo ""

services=("grafana" "mimir" "loki" "tempo" "intelligence-engine" "postgres" "redis")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is NOT running"
    fi
done

echo ""
echo "8. Testing endpoints..."
echo ""

# Test Intelligence Engine
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Intelligence Engine API is responding"
else
    echo "❌ Intelligence Engine API is NOT responding"
    echo "   Check logs: docker-compose logs intelligence-engine"
fi

# Test Grafana
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✅ Grafana is responding"
else
    echo "❌ Grafana is NOT responding"
    echo "   Check logs: docker-compose logs grafana"
fi

# Test Prometheus
if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "✅ Prometheus is responding"
else
    echo "❌ Prometheus is NOT responding"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 Access points:"
echo "   - Grafana:             http://localhost:3000 (admin/admin)"
echo "   - Intelligence Engine: http://localhost:8000"
echo "   - API Docs:            http://localhost:8000/docs"
echo "   - Prometheus:          http://localhost:9090"
echo ""
echo "📖 View logs: docker-compose logs -f"
echo "📖 See TROUBLESHOOTING.md for common issues"
echo ""

