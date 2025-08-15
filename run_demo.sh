#!/bin/bash

# OSSGameForge Demo Script - Linux/macOS
# Quickly start the application in demo mode

set -e

echo "🚀 Starting OSSGameForge Demo..."
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

# Set demo mode environment variables
export MOCK_MODE=true
export USE_LOCAL_MODEL=false

echo "🔧 Configuration:"
echo "  - Mock Mode: Enabled"
echo "  - Local Model: Disabled (using fallback)"
echo ""

# Stop any existing containers
echo "🧹 Cleaning up any existing containers..."
docker-compose down 2>/dev/null || true

# Start the services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend might still be starting up..."
fi

echo ""
echo "================================"
echo "✨ OSSGameForge Demo is running!"
echo ""
echo "📍 Access points:"
echo "  - API: http://localhost:8000"
echo "  - API Documentation: http://localhost:8000/docs"
echo "  - MinIO Console: http://localhost:9001"
echo "    Username: minioadmin"
echo "    Password: minioadmin"
echo ""
echo "📖 Quick Start Guide:"
echo "  1. Visit the API docs to explore endpoints"
echo "  2. Upload assets with user consent"
echo "  3. Generate game scenes with AI"
echo "  4. Export to HTML5 runner"
echo ""
echo "🛑 To stop the demo:"
echo "  docker-compose down"
echo ""
echo "Happy game creation! 🎮"