#!/usr/bin/env python3
"""
Instagram Bot Runner Script
تشغيل بوت انستجرام
"""

import os
import sys
import logging
from web_interface import app

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/instagram_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'templates', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import selenium
        import flask
        import requests
        import faker
        print("✅ جميع المتطلبات مثبتة بنجاح")
        return True
    except ImportError as e:
        print(f"❌ خطأ في المتطلبات: {e}")
        print("يرجى تشغيل: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the Instagram bot"""
    print("🤖 بوت انستجرام")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Setup logging
    setup_logging()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("🚀 بدء تشغيل البوت...")
    print("📱 الواجهة متاحة على: http://localhost:5000")
    print("⏹️  اضغط Ctrl+C لإيقاف البوت")
    print("=" * 50)
    
    try:
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⏹️  تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        logging.error(f"Application error: {e}")

if __name__ == "__main__":
    main()