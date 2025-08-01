#!/usr/bin/env python3
"""
Instagram Account Creator Bot - Main Runner Script

This script provides a simple way to run the Instagram bot application.
It includes setup checks and provides both web interface and command line options.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "instagram_bot.log"),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'selenium',
        'undetected_chromedriver',
        'flask',
        'requests',
        'faker',
        'pillow',
        'opencv-python',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_chrome():
    """Check if Chrome browser is available"""
    import subprocess
    
    try:
        # Try to get Chrome version
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Chrome browser found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    try:
        # Try alternative Chrome command
        result = subprocess.run(['chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Chrome browser found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Chrome browser not found")
    print("Please install Google Chrome browser")
    return False

def run_web_interface():
    """Run the web interface"""
    print("🚀 Starting Instagram Bot Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        from web_interface import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

def run_command_line():
    """Run the bot in command line mode"""
    print("🤖 Starting Instagram Bot in command line mode...")
    
    try:
        from instagram_bot import InstagramBot
        
        bot = InstagramBot()
        
        if bot.setup_driver():
            print("✅ Browser setup successful")
            
            # Generate user data
            user_data = bot.generate_random_user_data()
            user_data['email'] = bot.get_temporary_email()
            
            print(f"📧 Using email: {user_data['email']}")
            print(f"👤 Username: {user_data['username']}")
            print(f"🔐 Password: {user_data['password']}")
            
            # Create account
            print("🔄 Creating Instagram account...")
            if bot.create_instagram_account(user_data):
                print("✅ Account created successfully!")
                print(f"📱 Username: @{user_data['username']}")
                print(f"📧 Email: {user_data['email']}")
                print(f"🔐 Password: {user_data['password']}")
            else:
                print("❌ Failed to create account")
            
            bot.close_driver()
        else:
            print("❌ Failed to setup browser")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def run_test():
    """Run a test to verify bot functionality"""
    print("🧪 Running bot test...")
    
    try:
        from instagram_bot import InstagramBot
        from temp_email_service import MockEmailService
        
        # Test email service
        email_service = MockEmailService()
        email = email_service.generate_email()
        print(f"✅ Email service test: {email}")
        
        # Test bot setup
        bot = InstagramBot()
        if bot.setup_driver():
            print("✅ Browser setup test passed")
            bot.close_driver()
        else:
            print("❌ Browser setup test failed")
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Instagram Account Creator Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Start web interface
  python run.py --web             # Start web interface
  python run.py --cli             # Run in command line mode
  python run.py --test            # Run tests
        """
    )
    
    parser.add_argument(
        '--web', 
        action='store_true', 
        help='Start web interface (default)'
    )
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Run in command line mode'
    )
    parser.add_argument(
        '--test', 
        action='store_true', 
        help='Run tests'
    )
    parser.add_argument(
        '--check', 
        action='store_true', 
        help='Check dependencies and setup'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    print("🤖 Instagram Account Creator Bot")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Chrome
    if not check_chrome():
        sys.exit(1)
    
    # Run based on arguments
    if args.check:
        print("✅ Setup check completed")
        return
    
    if args.test:
        run_test()
    elif args.cli:
        run_command_line()
    else:
        # Default to web interface
        run_web_interface()

if __name__ == "__main__":
    main()