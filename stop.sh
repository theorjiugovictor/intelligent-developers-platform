#!/bin/bash

echo "🛑 Stopping Intelligent Development Platform..."

# Stop all services
docker-compose down

echo ""
echo "✅ All services stopped"
echo ""
echo "💡 To remove all data and volumes, run:"
echo "   docker-compose down -v"
echo ""

