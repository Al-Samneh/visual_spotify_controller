#!/usr/bin/env python3
"""
Setup script for Spotify Camera Controller
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)
    print(f"Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

def setup_env_file():
    """Help user set up environment file"""
    env_file = Path(".env")
    
    if env_file.exists():
        print(".env file already exists")
        return
    
    print("\nSetting up Spotify API credentials...")
    print("1. Go to https://developer.spotify.com/dashboard/")
    print("2. Create a new app")
    print("3. Add 'https://127.0.0.1:8080/callback' to Redirect URIs")
    print("4. Copy your Client ID and Client Secret")
    
    # Open Spotify Developer Dashboard
    webbrowser.open("https://developer.spotify.com/dashboard/")
    
    client_id = input("\nEnter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("Client ID and Secret are required")
        sys.exit(1)
    
    # Create .env file
    env_content = f"""# Spotify API credentials
SPOTIFY_CLIENT_ID={client_id}
SPOTIFY_CLIENT_SECRET={client_secret}
SPOTIFY_REDIRECT_URI=https://127.0.0.1:8080/callback
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(".env file created successfully")

def main():
    """Main setup function"""
    print("Spotify Camera Controller Setup")
    print("=" * 40)
    
    check_python_version()
    install_dependencies()
    setup_env_file()
    
    print("\nSetup complete!")
    print("Run 'python spotify_controller.py' to start the app")
    print("\nGesture Controls:")
    print("Index finger: Play/Pause")
    print("Peace sign: Next track")
    print("Three fingers: Previous track")
    print("Open palm: Volume up")
    print("Closed fist: Volume down")

if __name__ == "__main__":
    main()