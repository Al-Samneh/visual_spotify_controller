#!/bin/bash
# Quick launcher for Spotify Camera Controller

echo "🎵 Starting Spotify Camera Controller..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Running setup..."
    python setup.py
fi

# Run the application
echo "🚀 Launching application..."
python spotify_controller.py