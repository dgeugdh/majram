"""
Human Verification Module for Instagram Bot
وحدة التحقق البشري لبوت انستقرام
"""

import time
import random
import string
import logging
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import pyttsx3
import os

class HumanVerificationSystem:
    """نظام التحقق البشري المتقدم"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.recognition_engine = None
        self.speech_engine = None
        self.setup_speech_recognition()
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def setup_speech_recognition(self):
        """إعداد التعرف على الكلام"""
        try:
            self.recognition_engine = sr.Recognizer()
            self.speech_engine = pyttsx3.init()
            self.logger.info("تم إعداد نظام التعرف على الكلام")
        except Exception as e:
            self.logger.warning(f"فشل في إعداد التعرف على الكلام: {e}")
    
    def detect_verification_type(self, driver) -> str:
        """اكتشاف نوع التحقق"""
        try:
            # البحث عن أنواع مختلفة من التحقق
            verification_types = {
                'captcha': "//img[contains(@src, 'captcha') or contains(@alt, 'captcha')]",
                'recaptcha': "//iframe[contains(@src, 'recaptcha')]",
                'phone': "//input[@name='phone' or contains(@placeholder, 'phone')]",
                'email': "//*[contains(text(), 'email') or contains(text(), 'Email')]",
                'sms': "//input[@name='code' or contains(@placeholder, 'code')]",
                'image': "//img[contains(@src, 'verify') or contains(@alt, 'verify')]",
                'audio': "//audio or //*[contains(text(), 'audio')]"
            }
            
            for verification_type, xpath in verification_types.items():
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    self.logger.info(f"تم اكتشاف تحقق من نوع: {verification_type}")
                    return verification_type
            
            self.logger.info("لم يتم اكتشاف أي نوع تحقق")
            return 'unknown'
            
        except Exception as e:
            self.logger.error(f"خطأ في اكتشاف نوع التحقق: {e}")
            return 'unknown'
    
    def solve_image_captcha(self, driver) -> bool:
        """حل CAPTCHA بالصور"""
        try:
            # البحث عن صور CAPTCHA
            captcha_images = driver.find_elements(By.XPATH, 
                "//img[contains(@src, 'captcha') or contains(@alt, 'captcha')]")
            
            if not captcha_images:
                self.logger.info("لم يتم العثور على صور CAPTCHA")
                return False
            
            captcha_image = captcha_images[0]
            
            # التقاط لقطة شاشة للصورة
            screenshot = captcha_image.screenshot_as_png
            image = Image.open(io.BytesIO(screenshot))
            
            # معالجة الصورة
            processed_image = self.preprocess_captcha_image(image)
            
            # حل CAPTCHA
            solution = self.ocr_captcha(processed_image)
            
            if solution:
                # إدخال الحل
                input_field = driver.find_element(By.XPATH, 
                    "//input[@name='captcha' or contains(@placeholder, 'captcha')]")
                input_field.clear()
                input_field.send_keys(solution)
                
                # إرسال الحل
                submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                self.logger.info(f"تم حل CAPTCHA بنجاح: {solution}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في حل CAPTCHA بالصور: {e}")
            return False
    
    def preprocess_captcha_image(self, image: Image.Image) -> np.ndarray:
        """معالجة صورة CAPTCHA"""
        try:
            # تحويل إلى مصفوفة
            img_array = np.array(image)
            
            # تحويل إلى تدرج رمادي
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # تقليل الضوضاء
            denoised = cv2.medianBlur(gray, 3)
            
            # تحسين التباين
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # العتبة
            _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # تنظيف الصورة
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"خطأ في معالجة صورة CAPTCHA: {e}")
            return np.array(image)
    
    def ocr_captcha(self, image: np.ndarray) -> str:
        """استخدام OCR لحل CAPTCHA"""
        try:
            # تحويل إلى صورة PIL
            pil_image = Image.fromarray(image)
            
            # استخدام Tesseract
            import pytesseract
            text = pytesseract.image_to_string(
                pil_image, 
                config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            )
            
            # تنظيف النص
            text = text.strip().replace(' ', '').replace('\n', '').replace('\r', '')
            text = ''.join(c for c in text if c.isalnum())
            
            if len(text) >= 4 and len(text) <= 8:
                self.logger.info(f"OCR حل CAPTCHA: {text}")
                return text
            else:
                self.logger.warning(f"نتيجة OCR غير صالحة: {text}")
                return None
                
        except Exception as e:
            self.logger.error(f"خطأ في OCR CAPTCHA: {e}")
            return None
    
    def solve_audio_captcha(self, driver) -> bool:
        """حل CAPTCHA الصوتي"""
        try:
            # البحث عن عناصر الصوت
            audio_elements = driver.find_elements(By.XPATH, "//audio or //*[contains(text(), 'audio')]")
            
            if not audio_elements:
                self.logger.info("لم يتم العثور على CAPTCHA صوتي")
                return False
            
            # البحث عن زر الصوت
            audio_button = driver.find_element(By.XPATH, 
                "//button[contains(@title, 'audio') or contains(@aria-label, 'audio')]")
            audio_button.click()
            
            # انتظار تحميل الصوت
            time.sleep(2)
            
            # محاولة التعرف على الكلام
            if self.recognition_engine:
                try:
                    with sr.Microphone() as source:
                        self.logger.info("جاري الاستماع للصوت...")
                        audio = self.recognition_engine.listen(source, timeout=10)
                        text = self.recognition_engine.recognize_google(audio)
                        
                        if text:
                            # إدخال النص
                            input_field = driver.find_element(By.XPATH, 
                                "//input[@name='audio' or contains(@placeholder, 'audio')]")
                            input_field.clear()
                            input_field.send_keys(text)
                            
                            # إرسال الحل
                            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                            submit_button.click()
                            
                            self.logger.info(f"تم حل CAPTCHA الصوتي: {text}")
                            return True
                            
                except sr.UnknownValueError:
                    self.logger.warning("لم يتم التعرف على الكلام")
                except sr.RequestError as e:
                    self.logger.error(f"خطأ في خدمة التعرف على الكلام: {e}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في حل CAPTCHA الصوتي: {e}")
            return False
    
    def handle_phone_verification(self, driver) -> bool:
        """التعامل مع التحقق بالهاتف"""
        try:
            # البحث عن حقل الهاتف
            phone_elements = driver.find_elements(By.XPATH, 
                "//input[@name='phone' or contains(@placeholder, 'phone')]")
            
            if not phone_elements:
                self.logger.info("لم يتم العثور على حقل الهاتف")
                return False
            
            phone_input = phone_elements[0]
            
            # توليد رقم هاتف
            phone_number = self.generate_phone_number()
            phone_input.clear()
            phone_input.send_keys(phone_number)
            
            # إرسال رقم الهاتف
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # انتظار رمز التحقق
            time.sleep(3)
            
            # إدخال رمز تحقق مزيف
            sms_input = driver.find_element(By.XPATH, 
                "//input[@name='code' or contains(@placeholder, 'code')]")
            fake_code = ''.join(random.choices(string.digits, k=6))
            sms_input.send_keys(fake_code)
            
            # إرسال رمز التحقق
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            self.logger.info(f"تم إرسال رقم هاتف: {phone_number}")
            return True
            
        except Exception as e:
            self.logger.error(f"خطأ في التحقق بالهاتف: {e}")
            return False
    
    def generate_phone_number(self) -> str:
        """توليد رقم هاتف"""
        # رموز مناطق أمريكية
        area_codes = ['201', '202', '203', '205', '206', '207', '208', '209', '210', 
                     '212', '213', '214', '215', '216', '217', '218', '219', '220']
        
        area_code = random.choice(area_codes)
        prefix = str(random.randint(100, 999))
        line_number = str(random.randint(1000, 9999))
        
        return f"+1{area_code}{prefix}{line_number}"
    
    def handle_email_verification(self, driver) -> bool:
        """التعامل مع التحقق بالبريد الإلكتروني"""
        try:
            # البحث عن عناصر التحقق بالبريد
            email_verify_elements = driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'email') or contains(text(), 'Email')]")
            
            if not email_verify_elements:
                self.logger.info("لم يتم العثور على تحقق بالبريد الإلكتروني")
                return False
            
            # انتظار وصول البريد
            self.logger.info("في انتظار وصول بريد التحقق...")
            time.sleep(10)
            
            # محاولة العثور على رابط التحقق
            verification_links = driver.find_elements(By.XPATH, 
                "//a[contains(@href, 'verify') or contains(@href, 'confirm')]")
            
            if verification_links:
                verification_links[0].click()
                self.logger.info("تم النقر على رابط التحقق")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في التحقق بالبريد الإلكتروني: {e}")
            return False
    
    def solve_image_selection_captcha(self, driver) -> bool:
        """حل CAPTCHA اختيار الصور"""
        try:
            # البحث عن صور الاختيار
            selection_images = driver.find_elements(By.XPATH, 
                "//img[contains(@src, 'select') or contains(@alt, 'select')]")
            
            if not selection_images:
                self.logger.info("لم يتم العثور على CAPTCHA اختيار الصور")
                return False
            
            # اختيار صورة عشوائية
            random_image = random.choice(selection_images)
            random_image.click()
            
            # النقر على زر الإرسال
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            self.logger.info("تم اختيار صورة عشوائية")
            return True
            
        except Exception as e:
            self.logger.error(f"خطأ في حل CAPTCHA اختيار الصور: {e}")
            return False
    
    def handle_all_verifications(self, driver) -> bool:
        """التعامل مع جميع أنواع التحقق"""
        try:
            max_attempts = 5
            attempts = 0
            
            while attempts < max_attempts:
                verification_type = self.detect_verification_type(driver)
                
                if verification_type == 'unknown':
                    self.logger.info("لم يتم اكتشاف تحقق إضافي")
                    return True
                
                self.logger.info(f"معالجة تحقق من نوع: {verification_type}")
                
                success = False
                if verification_type == 'captcha':
                    success = self.solve_image_captcha(driver)
                elif verification_type == 'audio':
                    success = self.solve_audio_captcha(driver)
                elif verification_type == 'phone':
                    success = self.handle_phone_verification(driver)
                elif verification_type == 'email':
                    success = self.handle_email_verification(driver)
                elif verification_type == 'image':
                    success = self.solve_image_selection_captcha(driver)
                elif verification_type == 'sms':
                    success = self.handle_phone_verification(driver)
                
                if success:
                    self.logger.info(f"تم حل التحقق بنجاح: {verification_type}")
                    time.sleep(3)  # انتظار تحميل الصفحة
                else:
                    self.logger.warning(f"فشل في حل التحقق: {verification_type}")
                
                attempts += 1
            
            self.logger.error(f"فشل في حل التحقق بعد {max_attempts} محاولات")
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في معالجة التحقق: {e}")
            return False

# Factory function
def get_human_verification_system():
    """الحصول على نظام التحقق البشري"""
    return HumanVerificationSystem()

if __name__ == "__main__":
    # اختبار نظام التحقق البشري
    logging.basicConfig(level=logging.INFO)
    
    verification_system = get_human_verification_system()
    
    # اختبار توليد رقم هاتف
    phone = verification_system.generate_phone_number()
    print(f"رقم هاتف مولّد: {phone}")
    
    print("✅ تم اختبار نظام التحقق البشري بنجاح")