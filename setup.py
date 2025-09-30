#!/usr/bin/env python3
"""
Setup script for Video Terminal Tool
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is 3.7+"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ FFmpeg not found!")
    print("📥 Please install FFmpeg:")
    print("   Windows: Download from https://ffmpeg.org/download.html")
    print("   macOS: brew install ffmpeg")
    print("   Linux: sudo apt install ffmpeg")
    return False

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Installing Python packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def main():
    """Main setup function"""
    print("🎬 Video Terminal Tool Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("\n⚠️  Setup incomplete. Please install FFmpeg first.")
        return
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Setup incomplete. Please check the error messages above.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("🚀 Run the tool with: python video_tool.py")

if __name__ == "__main__":
    main()