#!/bin/bash
set -o errexit

# Render.com build script for DocuBrain backend
echo "🚀 Starting DocuBrain backend build..."

# Install Python dependencies using the deployment-specific requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements-deploy.txt

# Copy server-deploy.py to server.py for deployment
echo "🔄 Setting up deployment server..."
cp server-deploy.py server.py

echo "✅ Build completed successfully!"