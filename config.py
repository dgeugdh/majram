# Instagram Bot Configuration
# إعدادات بوت انستجرام

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Instagram Bot"""
    
    # Bot Settings
    BOT_DELAY = int(os.getenv('BOT_DELAY', 2))
    MAX_ACCOUNTS = int(os.getenv('MAX_ACCOUNTS', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # Timeout Settings
    CAPTCHA_TIMEOUT = int(os.getenv('CAPTCHA_TIMEOUT', 60))
    EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 120))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    
    # Web Interface Settings
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # CAPTCHA Settings
    CAPTCHA_SOLVER_API_KEY = os.getenv('CAPTCHA_SOLVER_API_KEY', '')
    CAPTCHA_SOLVER_METHOD = os.getenv('CAPTCHA_SOLVER_METHOD', 'ocr')  # 'ocr' or 'api'
    
    # Email Settings
    TEMP_EMAIL_DOMAINS = [
        'temp-mail.org',
        '10minutemail.com',
        'guerrillamail.com',
        'mailinator.com',
        'tempmail.plus',
        'temp-mail.io'
    ]
    
    # Chrome Settings
    CHROME_OPTIONS = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--disable-extensions',
        '--disable-plugins',
        '--disable-images',
        '--disable-javascript',
        '--disable-web-security',
        '--allow-running-insecure-content',
        '--disable-features=VizDisplayCompositor'
    ]
    
    # User Agent Settings
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    # Instagram URLs
    INSTAGRAM_URLS = {
        'signup': 'https://www.instagram.com/accounts/emailsignup/',
        'login': 'https://www.instagram.com/accounts/login/',
        'home': 'https://www.instagram.com/'
    }
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/instagram_bot.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Security Settings
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_LIST = os.getenv('PROXY_LIST', '').split(',') if os.getenv('PROXY_LIST') else []
    USE_VPN = os.getenv('USE_VPN', 'False').lower() == 'true'
    
    # Performance Settings
    THREAD_POOL_SIZE = int(os.getenv('THREAD_POOL_SIZE', 5))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    @classmethod
    def get_chrome_options(cls):
        """Get Chrome options as a list"""
        return cls.CHROME_OPTIONS.copy()
    
    @classmethod
    def get_random_user_agent(cls):
        """Get a random user agent"""
        import random
        return random.choice(cls.USER_AGENTS)
    
    @classmethod
    def get_temp_email_domain(cls):
        """Get a random temporary email domain"""
        import random
        return random.choice(cls.TEMP_EMAIL_DOMAINS)