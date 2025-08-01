import requests
import time
import random
import string
from typing import Optional, Dict, List
import logging

class TemporaryEmailService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def generate_email(self) -> str:
        """Generate a temporary email address"""
        try:
            # Generate random username
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            # Use a temporary email service
            email = f"{username}@temp-mail.org"
            
            self.logger.info(f"Generated temporary email: {email}")
            return email
            
        except Exception as e:
            self.logger.error(f"Failed to generate email: {e}")
            return None
    
    def check_email(self, email: str) -> List[Dict]:
        """Check for emails in the temporary email inbox"""
        try:
            # This is a mock implementation
            # In a real scenario, you would integrate with a temporary email API
            time.sleep(2)  # Simulate API call delay
            
            # Mock email response
            emails = []
            if random.random() > 0.7:  # 30% chance of having emails
                emails.append({
                    'from': 'noreply@instagram.com',
                    'subject': 'Confirm your Instagram account',
                    'body': 'Click here to confirm your account: https://instagram.com/confirm/123456',
                    'timestamp': time.time()
                })
            
            return emails
            
        except Exception as e:
            self.logger.error(f"Failed to check email: {e}")
            return []
    
    def get_verification_link(self, email: str) -> Optional[str]:
        """Extract verification link from emails"""
        try:
            emails = self.check_email(email)
            
            for email_data in emails:
                if 'instagram' in email_data['subject'].lower():
                    # Extract verification link from email body
                    body = email_data['body']
                    if 'https://instagram.com/confirm/' in body:
                        start = body.find('https://instagram.com/confirm/')
                        end = body.find(' ', start)
                        if end == -1:
                            end = len(body)
                        return body[start:end]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get verification link: {e}")
            return None
    
    def wait_for_verification_email(self, email: str, timeout: int = 60) -> Optional[str]:
        """Wait for verification email and return the link"""
        try:
            self.logger.info(f"Waiting for verification email to {email}")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                verification_link = self.get_verification_link(email)
                if verification_link:
                    self.logger.info(f"Verification link found: {verification_link}")
                    return verification_link
                
                time.sleep(5)  # Check every 5 seconds
            
            self.logger.warning(f"No verification email received within {timeout} seconds")
            return None
            
        except Exception as e:
            self.logger.error(f"Error waiting for verification email: {e}")
            return None

class MockEmailService:
    """Mock email service for testing purposes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emails = {}
    
    def generate_email(self) -> str:
        """Generate a mock email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@mock-temp.com"
        self.emails[email] = []
        self.logger.info(f"Generated mock email: {email}")
        return email
    
    def add_mock_email(self, email: str, from_addr: str, subject: str, body: str):
        """Add a mock email to the inbox"""
        if email not in self.emails:
            self.emails[email] = []
        
        self.emails[email].append({
            'from': from_addr,
            'subject': subject,
            'body': body,
            'timestamp': time.time()
        })
    
    def check_email(self, email: str) -> List[Dict]:
        """Check mock email inbox"""
        return self.emails.get(email, [])
    
    def get_verification_link(self, email: str) -> Optional[str]:
        """Get verification link from mock emails"""
        emails = self.check_email(email)
        
        for email_data in emails:
            if 'instagram' in email_data['subject'].lower():
                body = email_data['body']
                if 'https://instagram.com/confirm/' in body:
                    start = body.find('https://instagram.com/confirm/')
                    end = body.find(' ', start)
                    if end == -1:
                        end = len(body)
                    return body[start:end]
        
        return None
    
    def wait_for_verification_email(self, email: str, timeout: int = 60) -> Optional[str]:
        """Wait for verification email in mock service"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            verification_link = self.get_verification_link(email)
            if verification_link:
                return verification_link
            time.sleep(2)
        return None

# Factory function to get email service
def get_email_service(use_mock: bool = False):
    """Get email service instance"""
    if use_mock:
        return MockEmailService()
    else:
        return TemporaryEmailService()

if __name__ == "__main__":
    # Test the email service
    email_service = get_email_service(use_mock=True)
    
    # Generate email
    email = email_service.generate_email()
    print(f"Generated email: {email}")
    
    # Add mock verification email
    if isinstance(email_service, MockEmailService):
        email_service.add_mock_email(
            email,
            'noreply@instagram.com',
            'Confirm your Instagram account',
            'Click here to confirm your account: https://instagram.com/confirm/123456'
        )
    
    # Check for verification link
    link = email_service.wait_for_verification_email(email, timeout=10)
    if link:
        print(f"Verification link: {link}")
    else:
        print("No verification link found")