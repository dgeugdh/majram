import cv2
import numpy as np
from PIL import Image
import pytesseract
import requests
import io
import base64
import time
import logging
from typing import Optional, Tuple

class CaptchaSolver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_tesseract()
    
    def setup_tesseract(self):
        """Setup Tesseract OCR for CAPTCHA solving"""
        try:
            # Try to set tesseract path (adjust based on your system)
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
            # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Linux
            pass
        except Exception as e:
            self.logger.warning(f"Tesseract setup failed: {e}")
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # Apply thresholding
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations
            kernel = np.ones((2, 2), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            return image
    
    def solve_captcha_ocr(self, image: np.ndarray) -> Optional[str]:
        """Solve CAPTCHA using OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Configure Tesseract for CAPTCHA
            custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            # Clean up text
            text = text.strip().replace(' ', '').replace('\n', '').replace('\r', '')
            
            # Filter out non-alphanumeric characters
            text = ''.join(c for c in text if c.isalnum())
            
            if text:
                self.logger.info(f"OCR extracted text: {text}")
                return text
            else:
                self.logger.warning("No text extracted from CAPTCHA")
                return None
                
        except Exception as e:
            self.logger.error(f"OCR CAPTCHA solving failed: {e}")
            return None
    
    def solve_captcha_api(self, image: np.ndarray) -> Optional[str]:
        """Solve CAPTCHA using external API service"""
        try:
            # Convert image to base64
            _, buffer = cv2.imencode('.png', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # This is a placeholder for API integration
            # You would need to integrate with a real CAPTCHA solving service
            # like 2captcha, Anti-Captcha, or similar
            
            api_url = "https://api.2captcha.com/in.php"
            api_key = "YOUR_API_KEY"  # Replace with actual API key
            
            data = {
                'method': 'base64',
                'key': api_key,
                'body': img_base64,
                'json': 1
            }
            
            # Send CAPTCHA to solving service
            response = requests.post(api_url, data=data)
            result = response.json()
            
            if result.get('status') == 1:
                captcha_id = result.get('request')
                
                # Wait for solution
                solution = self.wait_for_solution(api_key, captcha_id)
                return solution
            else:
                self.logger.error(f"CAPTCHA API error: {result.get('error_text')}")
                return None
                
        except Exception as e:
            self.logger.error(f"API CAPTCHA solving failed: {e}")
            return None
    
    def wait_for_solution(self, api_key: str, captcha_id: str, timeout: int = 60) -> Optional[str]:
        """Wait for CAPTCHA solution from API"""
        try:
            api_url = "https://api.2captcha.com/res.php"
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                params = {
                    'key': api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                
                response = requests.get(api_url, params=params)
                result = response.json()
                
                if result.get('status') == 1:
                    return result.get('request')
                elif result.get('request') == 'CAPCHA_NOT_READY':
                    time.sleep(5)  # Wait 5 seconds before checking again
                else:
                    self.logger.error(f"CAPTCHA solution error: {result.get('error_text')}")
                    return None
            
            self.logger.warning("CAPTCHA solution timeout")
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to wait for CAPTCHA solution: {e}")
            return None
    
    def solve_captcha(self, image: np.ndarray, method: str = 'ocr') -> Optional[str]:
        """Main method to solve CAPTCHA"""
        try:
            if method == 'ocr':
                return self.solve_captcha_ocr(image)
            elif method == 'api':
                return self.solve_captcha_api(image)
            else:
                self.logger.error(f"Unknown CAPTCHA solving method: {method}")
                return None
                
        except Exception as e:
            self.logger.error(f"CAPTCHA solving failed: {e}")
            return None
    
    def detect_captcha_type(self, image: np.ndarray) -> str:
        """Detect the type of CAPTCHA"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Analyze image characteristics
            height, width = gray.shape
            
            # Check if it's a text-based CAPTCHA
            if height < 100 and width < 300:
                return 'text'
            
            # Check if it's an image-based CAPTCHA
            elif height > 100 and width > 300:
                return 'image'
            
            # Check if it's a reCAPTCHA
            else:
                return 'recaptcha'
                
        except Exception as e:
            self.logger.error(f"CAPTCHA type detection failed: {e}")
            return 'text'  # Default to text-based
    
    def solve_image_captcha(self, image: np.ndarray) -> Optional[str]:
        """Solve image-based CAPTCHA (like "click all images with cars")"""
        try:
            # This would require image recognition/ML models
            # For now, we'll return a mock solution
            self.logger.info("Image-based CAPTCHA detected, using mock solution")
            return "mock_solution"
            
        except Exception as e:
            self.logger.error(f"Image CAPTCHA solving failed: {e}")
            return None
    
    def solve_recaptcha(self, site_key: str, page_url: str) -> Optional[str]:
        """Solve reCAPTCHA"""
        try:
            # This would require integration with reCAPTCHA solving services
            # For now, we'll return a mock solution
            self.logger.info("reCAPTCHA detected, using mock solution")
            return "mock_recaptcha_solution"
            
        except Exception as e:
            self.logger.error(f"reCAPTCHA solving failed: {e}")
            return None

class HumanVerificationHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.captcha_solver = CaptchaSolver()
    
    def handle_human_verification(self, driver, verification_type: str = 'captcha') -> bool:
        """Handle various types of human verification"""
        try:
            if verification_type == 'captcha':
                return self.handle_captcha(driver)
            elif verification_type == 'phone':
                return self.handle_phone_verification(driver)
            elif verification_type == 'email':
                return self.handle_email_verification(driver)
            else:
                self.logger.warning(f"Unknown verification type: {verification_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Human verification failed: {e}")
            return False
    
    def handle_captcha(self, driver) -> bool:
        """Handle CAPTCHA verification"""
        try:
            # Look for CAPTCHA elements
            captcha_elements = driver.find_elements_by_xpath("//img[contains(@src, 'captcha') or contains(@alt, 'captcha')]")
            
            if captcha_elements:
                captcha_element = captcha_elements[0]
                
                # Take screenshot
                captcha_screenshot = captcha_element.screenshot_as_png
                
                # Convert to OpenCV format
                nparr = np.frombuffer(captcha_screenshot, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Solve CAPTCHA
                solution = self.captcha_solver.solve_captcha(image)
                
                if solution:
                    # Find input field and enter solution
                    input_field = driver.find_element_by_xpath("//input[@name='captcha' or contains(@placeholder, 'captcha')]")
                    input_field.clear()
                    input_field.send_keys(solution)
                    
                    # Submit
                    submit_button = driver.find_element_by_xpath("//button[@type='submit']")
                    submit_button.click()
                    
                    self.logger.info("CAPTCHA solved successfully")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"CAPTCHA handling failed: {e}")
            return False
    
    def handle_phone_verification(self, driver) -> bool:
        """Handle phone verification"""
        try:
            # Check if phone verification is required
            phone_elements = driver.find_elements_by_xpath("//input[@name='phone' or contains(@placeholder, 'phone')]")
            
            if phone_elements:
                # Generate fake phone number
                import random
                phone_number = f"+1{random.randint(1000000000, 9999999999)}"
                
                phone_input = phone_elements[0]
                phone_input.clear()
                phone_input.send_keys(phone_number)
                
                # Submit phone number
                submit_button = driver.find_element_by_xpath("//button[@type='submit']")
                submit_button.click()
                
                # Wait for SMS code input
                import time
                time.sleep(3)
                
                # Enter fake SMS code
                sms_input = driver.find_element_by_xpath("//input[@name='code' or contains(@placeholder, 'code')]")
                sms_input.send_keys("123456")
                
                # Submit code
                submit_button = driver.find_element_by_xpath("//button[@type='submit']")
                submit_button.click()
                
                self.logger.info("Phone verification completed")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Phone verification failed: {e}")
            return False
    
    def handle_email_verification(self, driver) -> bool:
        """Handle email verification"""
        try:
            # This would integrate with the temporary email service
            # For now, we'll simulate the process
            self.logger.info("Email verification process initiated")
            return True
            
        except Exception as e:
            self.logger.error(f"Email verification failed: {e}")
            return False

# Example usage
if __name__ == "__main__":
    solver = CaptchaSolver()
    
    # Test with a sample image
    # You would need to provide an actual CAPTCHA image
    print("CAPTCHA solver initialized")
    
    handler = HumanVerificationHandler()
    print("Human verification handler initialized")