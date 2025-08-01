# Instagram Account Creator Bot

A sophisticated Instagram account creation bot with human verification and temporary email integration. This bot automates the process of creating Instagram accounts while handling various verification challenges.

## Features

### 🤖 Core Functionality
- **Automated Account Creation**: Creates Instagram accounts with random user data
- **Human Verification**: Handles CAPTCHA challenges (visual and audio)
- **Temporary Email Integration**: Uses temporary email services for verification
- **Undetected Browser**: Uses undetected-chromedriver to avoid detection
- **Real-time Monitoring**: Web interface with live status updates

### 🛡️ Anti-Detection Features
- **Undetected Chrome Driver**: Bypasses bot detection mechanisms
- **Random Delays**: Implements random delays between actions
- **Fake User Agent**: Uses realistic browser fingerprints
- **Human-like Behavior**: Simulates human interaction patterns

### 📧 Email Verification
- **Temporary Email Service**: Integrates with multiple temporary email providers
- **Verification Code Extraction**: Automatically extracts codes from emails
- **Multiple Email Domains**: Supports various temporary email domains

### 🎯 CAPTCHA Solving
- **Visual CAPTCHA**: OCR-based solving for image CAPTCHAs
- **Audio CAPTCHA**: Speech recognition for audio challenges
- **Multiple Solving Methods**: Fallback mechanisms for different CAPTCHA types

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- Linux/Windows/macOS

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd instagram-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome WebDriver**
   ```bash
   # The bot uses undetected-chromedriver which handles this automatically
   # Make sure Chrome browser is installed on your system
   ```

4. **Run the application**
   ```bash
   python web_interface.py
   ```

5. **Access the web interface**
   - Open your browser and go to `http://localhost:5000`
   - The web interface will be available with full functionality

## Usage

### Web Interface

1. **Start the Bot**
   - Set the number of accounts to create (1-10)
   - Configure delay between accounts (5-60 seconds)
   - Click "Start Bot"

2. **Monitor Progress**
   - Real-time status updates
   - Live log display
   - Created accounts list

3. **Stop the Bot**
   - Click "Stop Bot" to halt the process
   - Bot will safely close browser instances

### Command Line Usage

```python
from instagram_bot import InstagramBot

# Create bot instance
bot = InstagramBot()

# Setup browser
if bot.setup_driver():
    # Generate user data
    user_data = bot.generate_random_user_data()
    user_data['email'] = bot.get_temporary_email()
    
    # Create account
    if bot.create_instagram_account(user_data):
        print("Account created successfully!")
    else:
        print("Failed to create account")
    
    # Clean up
    bot.close_driver()
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Bot Configuration
BOT_DELAY_MIN=5
BOT_DELAY_MAX=15
MAX_ACCOUNTS_PER_SESSION=10

# Email Service Configuration
TEMP_EMAIL_DOMAINS=temp-mail.org,10minutemail.com,guerrillamail.com

# CAPTCHA Service (optional)
CAPTCHA_SOLVER_API_KEY=your_api_key_here
```

### Advanced Configuration

#### Custom User Data Generation
```python
# Modify the generate_random_user_data method in instagram_bot.py
def generate_random_user_data(self):
    # Custom logic for generating user data
    pass
```

#### Custom CAPTCHA Solving
```python
# Integrate with external CAPTCHA solving services
def solve_captcha_with_service(self, captcha_image):
    # Implementation for 2captcha, Anti-Captcha, etc.
    pass
```

## Project Structure

```
instagram-bot/
├── instagram_bot.py          # Main bot class
├── temp_email_service.py     # Temporary email service
├── web_interface.py          # Flask web application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── templates/
│   └── index.html           # Web interface template
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── app.js           # Frontend JavaScript
└── logs/
    └── instagram_bot.log    # Bot logs
```

## Features in Detail

### Human Verification Integration

The bot includes sophisticated human verification handling:

1. **Visual CAPTCHA Detection**
   - Automatically detects CAPTCHA images
   - Uses OCR for text recognition
   - Supports multiple CAPTCHA formats

2. **Audio CAPTCHA Support**
   - Downloads audio CAPTCHA files
   - Uses speech recognition for conversion
   - Handles various audio formats

3. **Verification Code Handling**
   - Monitors temporary email for codes
   - Extracts codes using regex patterns
   - Supports multiple email providers

### Temporary Email Integration

The bot supports multiple temporary email services:

- **temp-mail.org**
- **10minutemail.com**
- **guerrillamail.com**
- **mailinator.com**
- **tempmail.plus**

### Anti-Detection Mechanisms

1. **Browser Fingerprinting**
   - Undetected Chrome driver
   - Custom user agent strings
   - Disabled automation flags

2. **Human-like Behavior**
   - Random delays between actions
   - Natural typing patterns
   - Mouse movement simulation

3. **Session Management**
   - Proper cookie handling
   - Session persistence
   - IP rotation support (manual)

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   ```bash
   # Make sure Chrome is installed
   google-chrome --version
   
   # Update Chrome to latest version
   sudo apt update && sudo apt upgrade google-chrome-stable
   ```

2. **Dependency Issues**
   ```bash
   # Reinstall dependencies
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   chmod +x web_interface.py
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Testing

Test individual components:

```python
# Test email service
from temp_email_service import MockEmailService
email_service = MockEmailService()
email = email_service.generate_email()
print(f"Generated email: {email}")

# Test bot setup
from instagram_bot import InstagramBot
bot = InstagramBot()
if bot.setup_driver():
    print("Driver setup successful")
    bot.close_driver()
```

## Security Considerations

### Important Notes

1. **Terms of Service**: This tool is for educational purposes only. Ensure compliance with Instagram's Terms of Service.

2. **Rate Limiting**: Implement appropriate delays to avoid being flagged as spam.

3. **IP Management**: Consider using VPN or proxy services for large-scale operations.

4. **Account Security**: Generated accounts should be properly secured and managed.

### Best Practices

- Use realistic delays between account creation
- Implement proper error handling
- Monitor for detection mechanisms
- Keep the bot updated with latest Instagram changes

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where appropriate
- Write meaningful commit messages

## License

This project is for educational purposes only. Users are responsible for complying with all applicable laws and terms of service.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs in `instagram_bot.log`
3. Create an issue with detailed information
4. Include system information and error messages

## Changelog

### Version 1.0.0
- Initial release
- Basic account creation functionality
- Web interface
- CAPTCHA solving
- Temporary email integration

### Planned Features
- Phone verification support
- Proxy integration
- Advanced CAPTCHA solving
- Account management dashboard
- Multi-threading support