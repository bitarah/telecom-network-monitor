#!/bin/bash

# 5G Network Monitor - Start Script
# Starts frontend (detached) and backend (attached with logs)

set -e

echo "🚀 Starting 5G Network Monitor..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🎨 Starting frontend (React Dashboard) in background..."
docker-compose up -d frontend

echo ""
echo "⏳ Waiting for frontend to be ready..."
sleep 3

echo ""
echo "✅ Frontend started successfully!"
echo "   Dashboard: http://localhost:5173"
echo ""

echo "🤖 Starting backend (Gradio ML App) with logs..."
echo "   ML Analytics: http://localhost:7860"
echo ""
echo "─────────────────────────────────────────────"
echo "📊 Backend Logs (Press Ctrl+C to stop):"
echo "─────────────────────────────────────────────"
echo ""

# Start backend in attached mode (shows logs)
# This will keep the terminal open and display logs
docker-compose up backend
