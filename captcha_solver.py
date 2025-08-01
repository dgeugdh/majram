import cv2
import numpy as np
from PIL import Image
import io
import base64
import requests
import time
import logging
from typing import Optional, Tuple
import pytesseract
from io import BytesIO

class CaptchaSolver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale if not already
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # Apply thresholding
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations to clean up
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {e}")
            return np.array(image)
    
    def solve_captcha_ocr(self, image: Image.Image) -> Optional[str]:
        """Solve CAPTCHA using OCR"""
        try:
            # Preprocess the image
            processed_img = self.preprocess_image(image)
            
            # Convert back to PIL Image for OCR
            pil_img = Image.fromarray(processed_img)
            
            # Use pytesseract for OCR
            try:
                text = pytesseract.image_to_string(pil_img, config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            except Exception as e:
                self.logger.warning(f"Pytesseract failed, using fallback: {e}")
                # Fallback: try with different configuration
                text = pytesseract.image_to_string(pil_img, config='--psm 7')
            
            # Clean the text
            text = text.strip().replace(' ', '').replace('\n', '').replace('\r', '')
            
            # Filter out non-alphanumeric characters
            text = ''.join(c for c in text if c.isalnum())
            
            if len(text) >= 4 and len(text) <= 8:  # Reasonable CAPTCHA length
                self.logger.info(f"OCR solved CAPTCHA: {text}")
                return text
            else:
                self.logger.warning(f"OCR result seems invalid: {text}")
                return None
                
        except Exception as e:
            self.logger.error(f"OCR CAPTCHA solving failed: {e}")
            return None
    
    def solve_captcha_api(self, image: Image.Image, api_key: str = None) -> Optional[str]:
        """Solve CAPTCHA using external API service"""
        try:
            # Convert image to base64
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Use 2captcha API (you need to sign up and get API key)
            if api_key:
                url = "http://2captcha.com/in.php"
                data = {
                    'key': api_key,
                    'method': 'base64',
                    'body': img_base64,
                    'json': 1
                }
                
                response = requests.post(url, data=data)
                result = response.json()
                
                if result.get('status') == 1:
                    captcha_id = result['request']
                    
                    # Wait for solution
                    for _ in range(30):  # Wait up to 30 seconds
                        time.sleep(2)
                        
                        check_url = "http://2captcha.com/res.php"
                        check_data = {
                            'key': api_key,
                            'action': 'get',
                            'id': captcha_id,
                            'json': 1
                        }
                        
                        check_response = requests.get(check_url, params=check_data)
                        check_result = check_response.json()
                        
                        if check_result.get('status') == 1:
                            solution = check_result['request']
                            self.logger.info(f"API solved CAPTCHA: {solution}")
                            return solution
                        elif check_result.get('request') != 'CAPCHA_NOT_READY':
                            self.logger.error(f"API CAPTCHA solving failed: {check_result}")
                            break
                    
                    self.logger.error("API CAPTCHA solving timeout")
                    return None
                else:
                    self.logger.error(f"API CAPTCHA submission failed: {result}")
                    return None
            else:
                self.logger.warning("No API key provided for CAPTCHA solving")
                return None
                
        except Exception as e:
            self.logger.error(f"API CAPTCHA solving failed: {e}")
            return None
    
    def solve_captcha_manual(self, image: Image.Image) -> Optional[str]:
        """Manual CAPTCHA solving (for testing)"""
        try:
            # Save image to file for manual inspection
            filename = f"captcha_{int(time.time())}.png"
            image.save(filename)
            
            self.logger.info(f"CAPTCHA image saved as {filename}")
            self.logger.info("Please solve the CAPTCHA manually and enter the solution:")
            
            # In a real implementation, you might want to show the image in a GUI
            # For now, we'll return a mock solution
            return "ABC123"
            
        except Exception as e:
            self.logger.error(f"Manual CAPTCHA solving failed: {e}")
            return None
    
    def solve_captcha(self, image: Image.Image, method: str = 'ocr', api_key: str = None) -> Optional[str]:
        """Main CAPTCHA solving method"""
        try:
            self.logger.info(f"Attempting to solve CAPTCHA using method: {method}")
            
            if method == 'ocr':
                return self.solve_captcha_ocr(image)
            elif method == 'api':
                return self.solve_captcha_api(image, api_key)
            elif method == 'manual':
                return self.solve_captcha_manual(image)
            else:
                self.logger.error(f"Unknown CAPTCHA solving method: {method}")
                return None
                
        except Exception as e:
            self.logger.error(f"CAPTCHA solving failed: {e}")
            return None
    
    def detect_captcha_type(self, image: Image.Image) -> str:
        """Detect the type of CAPTCHA"""
        try:
            img_array = np.array(image)
            
            # Check if it's a text-based CAPTCHA
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Analyze image characteristics
            height, width = gray.shape
            
            # Simple heuristics for CAPTCHA type detection
            if width > height * 2:  # Wide image - likely text CAPTCHA
                return 'text'
            elif width < height:  # Tall image - might be image selection
                return 'image'
            else:
                return 'text'  # Default to text
                
        except Exception as e:
            self.logger.error(f"CAPTCHA type detection failed: {e}")
            return 'text'  # Default fallback

class MockCaptchaSolver:
    """Mock CAPTCHA solver for testing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.solutions = {
            'test1': 'ABC123',
            'test2': 'XYZ789',
            'test3': 'DEF456'
        }
    
    def solve_captcha(self, image: Image.Image, method: str = 'mock') -> Optional[str]:
        """Mock CAPTCHA solving"""
        try:
            # Generate a mock solution based on image hash
            img_hash = hash(image.tobytes()) % 1000
            solution = f"CAPTCHA{img_hash:03d}"
            
            self.logger.info(f"Mock CAPTCHA solved: {solution}")
            return solution
            
        except Exception as e:
            self.logger.error(f"Mock CAPTCHA solving failed: {e}")
            return None

# Factory function to get CAPTCHA solver
def get_captcha_solver(use_mock: bool = False):
    """Get CAPTCHA solver instance"""
    if use_mock:
        return MockCaptchaSolver()
    else:
        return CaptchaSolver()

if __name__ == "__main__":
    # Test the CAPTCHA solver
    solver = get_captcha_solver(use_mock=True)
    
    # Create a mock image
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple test image
    img = Image.new('RGB', (200, 50), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    draw.text((10, 10), "ABC123", fill='black', font=font)
    
    # Solve the CAPTCHA
    solution = solver.solve_captcha(img)
    print(f"CAPTCHA solution: {solution}")