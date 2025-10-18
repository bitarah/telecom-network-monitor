#!/bin/bash

# 5G Network Monitor - Stop Script
# Stops all running containers

set -e

echo "🛑 Stopping 5G Network Monitor..."
echo ""

# Stop all services
echo "📦 Stopping containers..."
docker-compose down

echo ""
echo "✅ All containers stopped successfully!"
echo ""
echo "💡 To remove volumes and clean up completely, run:"
echo "   docker-compose down -v"
echo ""
