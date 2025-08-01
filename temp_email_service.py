import requests
import time
import random
import string
import json
from typing import Optional, List, Dict

class TemporaryEmailService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.email_domains = [
            'temp-mail.org',
            '10minutemail.com',
            'guerrillamail.com',
            'mailinator.com',
            'tempmail.plus'
        ]
    
    def generate_email(self) -> str:
        """Generate a temporary email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(self.email_domains)
        return f"{username}@{domain}"
    
    def check_mailbox(self, email: str) -> List[Dict]:
        """Check mailbox for new emails"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd need to integrate with actual temporary email APIs
            
            # Mock response for demonstration
            return []
        except Exception as e:
            print(f"Error checking mailbox: {e}")
            return []
    
    def get_verification_code(self, email: str, sender: str = "instagram", timeout: int = 60) -> Optional[str]:
        """Get verification code from email"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            emails = self.check_mailbox(email)
            
            for email_data in emails:
                if sender.lower() in email_data.get('from', '').lower():
                    # Extract verification code from email content
                    content = email_data.get('content', '')
                    code = self.extract_verification_code(content)
                    if code:
                        return code
            
            time.sleep(5)  # Wait 5 seconds before checking again
        
        return None
    
    def extract_verification_code(self, content: str) -> Optional[str]:
        """Extract verification code from email content"""
        import re
        
        # Common patterns for verification codes
        patterns = [
            r'\b\d{6}\b',  # 6-digit code
            r'\b\d{4}\b',  # 4-digit code
            r'verification code[:\s]*(\d+)',
            r'code[:\s]*(\d+)',
            r'(\d{4,6})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None

class MockEmailService:
    """Mock email service for testing purposes"""
    
    def __init__(self):
        self.emails = {}
    
    def generate_email(self) -> str:
        """Generate a mock email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{username}@mock-temp.com"
    
    def send_mock_email(self, email: str, sender: str, content: str):
        """Send a mock email (for testing)"""
        if email not in self.emails:
            self.emails[email] = []
        
        self.emails[email].append({
            'from': sender,
            'content': content,
            'timestamp': time.time()
        })
    
    def check_mailbox(self, email: str) -> List[Dict]:
        """Check mock mailbox"""
        return self.emails.get(email, [])
    
    def get_verification_code(self, email: str, sender: str = "instagram", timeout: int = 60) -> Optional[str]:
        """Get verification code from mock email"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            emails = self.check_mailbox(email)
            
            for email_data in emails:
                if sender.lower() in email_data.get('from', '').lower():
                    content = email_data.get('content', '')
                    code = self.extract_verification_code(content)
                    if code:
                        return code
            
            time.sleep(2)
        
        return None
    
    def extract_verification_code(self, content: str) -> Optional[str]:
        """Extract verification code from email content"""
        import re
        
        patterns = [
            r'\b\d{6}\b',
            r'\b\d{4}\b',
            r'verification code[:\s]*(\d+)',
            r'code[:\s]*(\d+)',
            r'(\d{4,6})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None

# Example usage
if __name__ == "__main__":
    # Test with mock service
    mock_service = MockEmailService()
    email = mock_service.generate_email()
    print(f"Generated email: {email}")
    
    # Send a mock verification email
    mock_service.send_mock_email(
        email,
        "noreply@instagram.com",
        "Your Instagram verification code is: 123456"
    )
    
    # Get the verification code
    code = mock_service.get_verification_code(email, "instagram", timeout=10)
    print(f"Verification code: {code}")