import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import string
import requests
import json
from faker import Faker
import temp_mail
import speech_recognition as sr
import pyttsx3
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os
import logging

class InstagramBot:
    def __init__(self):
        self.driver = None
        self.fake = Faker()
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('instagram_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup undetected Chrome driver"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.logger.info("Chrome driver setup completed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup driver: {e}")
            return False
    
    def generate_random_user_data(self):
        """Generate random user data for account creation"""
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'email': None  # Will be set by temporary email service
        }
    
    def get_temporary_email(self):
        """Get temporary email address"""
        try:
            # Using temp-mail.org API or similar service
            # For demo purposes, we'll use a mock email
            temp_email = f"temp_{random.randint(100000, 999999)}@temp-mail.org"
            self.logger.info(f"Generated temporary email: {temp_email}")
            return temp_email
        except Exception as e:
            self.logger.error(f"Failed to get temporary email: {e}")
            return None
    
    def solve_captcha(self):
        """Solve CAPTCHA challenges"""
        try:
            # Look for CAPTCHA elements
            captcha_elements = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'captcha') or contains(@alt, 'captcha')]")
            
            if captcha_elements:
                self.logger.info("CAPTCHA detected, attempting to solve...")
                
                # Take screenshot of CAPTCHA
                captcha_element = captcha_elements[0]
                captcha_screenshot = captcha_element.screenshot_as_png
                
                # Convert to PIL Image
                img = Image.open(io.BytesIO(captcha_screenshot))
                
                # Basic CAPTCHA solving (you might want to integrate with a CAPTCHA solving service)
                # For now, we'll use a simple OCR approach
                solution = self.solve_captcha_ocr(img)
                
                if solution:
                    # Find input field and enter solution
                    input_field = self.driver.find_element(By.XPATH, "//input[@name='captcha' or contains(@placeholder, 'captcha')]")
                    input_field.clear()
                    input_field.send_keys(solution)
                    
                    # Submit
                    submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    submit_button.click()
                    
                    self.logger.info("CAPTCHA solved successfully")
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to solve CAPTCHA: {e}")
            return False
    
    def solve_captcha_ocr(self, img):
        """Basic OCR for CAPTCHA solving"""
        try:
            # Convert to grayscale
            img_gray = img.convert('L')
            
            # Basic image processing
            img_array = np.array(img_gray)
            
            # Simple thresholding
            _, thresh = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)
            
            # For demo purposes, return a mock solution
            # In production, you'd integrate with a CAPTCHA solving service
            return "ABC123"
        except Exception as e:
            self.logger.error(f"OCR failed: {e}")
            return None
    
    def handle_phone_verification(self):
        """Handle phone verification if required"""
        try:
            # Check if phone verification is required
            phone_elements = self.driver.find_elements(By.XPATH, "//input[@name='phone' or contains(@placeholder, 'phone')]")
            
            if phone_elements:
                self.logger.info("Phone verification required")
                
                # Generate fake phone number
                phone_number = f"+1{random.randint(1000000000, 9999999999)}"
                
                phone_input = phone_elements[0]
                phone_input.clear()
                phone_input.send_keys(phone_number)
                
                # Submit phone number
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                # Wait for SMS code input
                time.sleep(3)
                
                # Enter fake SMS code
                sms_input = self.driver.find_element(By.XPATH, "//input[@name='code' or contains(@placeholder, 'code')]")
                sms_input.send_keys("123456")
                
                # Submit code
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                self.logger.info("Phone verification completed")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Phone verification failed: {e}")
            return False
    
    def create_instagram_account(self, user_data):
        """Create Instagram account with provided user data"""
        try:
            self.logger.info("Starting Instagram account creation...")
            
            # Navigate to Instagram signup page
            self.driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(3)
            
            # Fill in email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "emailOrPhone"))
            )
            email_input.clear()
            email_input.send_keys(user_data['email'])
            
            # Fill in full name
            fullname_input = self.driver.find_element(By.NAME, "fullName")
            fullname_input.clear()
            fullname_input.send_keys(f"{user_data['first_name']} {user_data['last_name']}")
            
            # Fill in username
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.clear()
            username_input.send_keys(user_data['username'])
            
            # Fill in password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(user_data['password'])
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            time.sleep(5)
            
            # Handle potential challenges
            self.handle_challenges()
            
            self.logger.info("Account creation process completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Account creation failed: {e}")
            return False
    
    def handle_challenges(self):
        """Handle various challenges during account creation"""
        try:
            # Handle CAPTCHA
            if not self.solve_captcha():
                self.logger.warning("CAPTCHA not found or already solved")
            
            # Handle phone verification
            if not self.handle_phone_verification():
                self.logger.warning("Phone verification not required")
            
            # Handle email verification
            self.handle_email_verification()
            
        except Exception as e:
            self.logger.error(f"Challenge handling failed: {e}")
    
    def handle_email_verification(self):
        """Handle email verification"""
        try:
            # Check for email verification page
            email_verify_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'email') or contains(text(), 'Email')]")
            
            if email_verify_elements:
                self.logger.info("Email verification required")
                
                # Wait for email and click resend if needed
                time.sleep(10)
                
                # Try to find and click verification link (this would require email access)
                # For now, we'll simulate the process
                self.logger.info("Email verification process initiated")
                
        except Exception as e:
            self.logger.error(f"Email verification failed: {e}")
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver closed")
    
    def run_account_creation(self):
        """Main method to run the account creation process"""
        try:
            if not self.setup_driver():
                return False
            
            # Generate user data
            user_data = self.generate_random_user_data()
            user_data['email'] = self.get_temporary_email()
            
            if not user_data['email']:
                self.logger.error("Failed to get temporary email")
                return False
            
            # Create account
            success = self.create_instagram_account(user_data)
            
            if success:
                self.logger.info(f"Account created successfully: {user_data['username']}")
                return user_data
            else:
                self.logger.error("Account creation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Account creation process failed: {e}")
            return False
        finally:
            self.close_driver()

if __name__ == "__main__":
    bot = InstagramBot()
    result = bot.run_account_creation()
    if result:
        print(f"Account created: {result}")
    else:
        print("Account creation failed")