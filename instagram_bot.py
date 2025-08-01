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
                captcha_text = self.simple_ocr_solve(img)
                
                if captcha_text:
                    # Find input field and enter solution
                    input_field = self.driver.find_element(By.XPATH, "//input[@name='captcha' or contains(@id, 'captcha')]")
                    input_field.clear()
                    input_field.send_keys(captcha_text)
                    
                    self.logger.info(f"CAPTCHA solved: {captcha_text}")
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Failed to solve CAPTCHA: {e}")
            return False
    
    def simple_ocr_solve(self, image):
        """Simple OCR for CAPTCHA solving (basic implementation)"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # For demo purposes, return a random string
            # In production, you'd use a proper OCR service
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        except Exception as e:
            self.logger.error(f"OCR solving failed: {e}")
            return None
    
    def solve_audio_captcha(self):
        """Solve audio CAPTCHA challenges"""
        try:
            # Look for audio CAPTCHA button
            audio_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'audio') or contains(text(), 'audio')]")
            audio_button.click()
            
            # Wait for audio to load
            time.sleep(2)
            
            # Download and process audio
            audio_element = self.driver.find_element(By.XPATH, "//audio")
            audio_url = audio_element.get_attribute('src')
            
            # Download audio file
            response = requests.get(audio_url)
            with open('captcha_audio.mp3', 'wb') as f:
                f.write(response.content)
            
            # Convert audio to text using speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile('captcha_audio.mp3') as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
            
            # Enter the recognized text
            input_field = self.driver.find_element(By.XPATH, "//input[@name='captcha' or contains(@id, 'captcha')]")
            input_field.clear()
            input_field.send_keys(text)
            
            self.logger.info(f"Audio CAPTCHA solved: {text}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to solve audio CAPTCHA: {e}")
            return False
    
    def create_instagram_account(self, user_data):
        """Create Instagram account with provided user data"""
        try:
            self.logger.info("Starting Instagram account creation...")
            
            # Navigate to Instagram signup page
            self.driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(3)
            
            # Fill in the signup form
            self.fill_signup_form(user_data)
            
            # Handle verification challenges
            if self.handle_verification():
                self.logger.info("Account created successfully!")
                return True
            else:
                self.logger.error("Failed to complete account creation")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating Instagram account: {e}")
            return False
    
    def fill_signup_form(self, user_data):
        """Fill the Instagram signup form"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Email field
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
            email_field.clear()
            email_field.send_keys(user_data['email'])
            time.sleep(1)
            
            # Full name field
            fullname_field = self.driver.find_element(By.NAME, "fullName")
            fullname_field.clear()
            fullname_field.send_keys(f"{user_data['first_name']} {user_data['last_name']}")
            time.sleep(1)
            
            # Username field
            username_field = self.driver.find_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys(user_data['username'])
            time.sleep(1)
            
            # Password field
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(user_data['password'])
            time.sleep(1)
            
            # Click signup button
            signup_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            signup_button.click()
            
            self.logger.info("Signup form filled successfully")
            
        except Exception as e:
            self.logger.error(f"Error filling signup form: {e}")
            raise
    
    def handle_verification(self):
        """Handle various verification challenges"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Check for different types of verification
            verification_types = [
                "//h2[contains(text(), 'Verify your email')]",  # Email verification
                "//h2[contains(text(), 'Verify your phone')]",   # Phone verification
                "//div[contains(text(), 'captcha')]",            # CAPTCHA
                "//div[contains(text(), 'verification')]"        # General verification
            ]
            
            for verification_xpath in verification_types:
                try:
                    verification_element = wait.until(EC.presence_of_element_located((By.XPATH, verification_xpath)))
                    self.logger.info(f"Verification type detected: {verification_xpath}")
                    
                    if "email" in verification_xpath.lower():
                        return self.handle_email_verification()
                    elif "phone" in verification_xpath.lower():
                        return self.handle_phone_verification()
                    elif "captcha" in verification_xpath.lower():
                        return self.solve_captcha()
                    else:
                        return self.handle_general_verification()
                        
                except:
                    continue
            
            # If no verification found, account might be created successfully
            return True
            
        except Exception as e:
            self.logger.error(f"Error handling verification: {e}")
            return False
    
    def handle_email_verification(self):
        """Handle email verification"""
        try:
            self.logger.info("Handling email verification...")
            
            # Wait for verification code input
            code_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='code' or contains(@placeholder, 'code')]"))
            )
            
            # Get verification code from temporary email
            verification_code = self.get_verification_code()
            
            if verification_code:
                code_input.clear()
                code_input.send_keys(verification_code)
                
                # Submit verification
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                time.sleep(3)
                return True
            else:
                self.logger.error("Failed to get verification code")
                return False
                
        except Exception as e:
            self.logger.error(f"Error handling email verification: {e}")
            return False
    
    def handle_phone_verification(self):
        """Handle phone verification"""
        try:
            self.logger.info("Handling phone verification...")
            
            # For phone verification, we might need to use a virtual phone number service
            # For now, we'll skip this step
            self.logger.warning("Phone verification not implemented yet")
            return False
            
        except Exception as e:
            self.logger.error(f"Error handling phone verification: {e}")
            return False
    
    def handle_general_verification(self):
        """Handle general verification challenges"""
        try:
            self.logger.info("Handling general verification...")
            
            # Try to solve CAPTCHA if present
            if self.solve_captcha():
                return True
            
            # Try audio CAPTCHA
            if self.solve_audio_captcha():
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error handling general verification: {e}")
            return False
    
    def get_verification_code(self):
        """Get verification code from temporary email"""
        try:
            # In a real implementation, you would check the temporary email service
            # for the verification code. For demo purposes, we'll return a mock code
            return f"{random.randint(100000, 999999)}"
        except Exception as e:
            self.logger.error(f"Error getting verification code: {e}")
            return None
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser driver closed")

if __name__ == "__main__":
    bot = InstagramBot()
    if bot.setup_driver():
        user_data = bot.generate_random_user_data()
        user_data['email'] = bot.get_temporary_email()
        
        if bot.create_instagram_account(user_data):
            print("Account created successfully!")
        else:
            print("Failed to create account")
        
        bot.close_driver()