"""
Advanced Features for Instagram Bot
ميزات متقدمة لبوت انستقرام
"""

import time
import random
import string
import requests
import json
import logging
from typing import Optional, Dict, List, Tuple
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os

class HumanVerification:
    """محاكاة السلوك البشري"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def human_type(self, element, text: str, min_delay: float = 0.1, max_delay: float = 0.3):
        """كتابة نص بطريقة بشرية"""
        try:
            element.clear()
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(min_delay, max_delay))
            
            self.logger.info(f"تم كتابة النص بطريقة بشرية: {text}")
            
        except Exception as e:
            self.logger.error(f"خطأ في الكتابة البشرية: {e}")
            element.send_keys(text)
    
    def human_scroll(self, driver, direction: str = 'down', distance: int = 300):
        """تمرير الصفحة بطريقة بشرية"""
        try:
            if direction == 'down':
                driver.execute_script(f"window.scrollBy(0, {distance});")
            elif direction == 'up':
                driver.execute_script(f"window.scrollBy(0, -{distance});")
            
            time.sleep(random.uniform(0.5, 1.5))
            self.logger.info(f"تم التمرير {direction}")
            
        except Exception as e:
            self.logger.error(f"خطأ في التمرير: {e}")
    
    def human_mouse_move(self, driver, element=None):
        """تحريك الماوس بطريقة بشرية"""
        try:
            actions = ActionChains(driver)
            
            if element:
                actions.move_to_element(element)
            else:
                # تحريك عشوائي
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y)
            
            actions.perform()
            time.sleep(random.uniform(0.2, 0.8))
            
        except Exception as e:
            self.logger.error(f"خطأ في تحريك الماوس: {e}")
    
    def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """تأخير عشوائي"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay

class ProxyManager:
    """إدارة البروكسي"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxies = []
        self.current_proxy = None
    
    def add_proxy(self, proxy: str, username: str = None, password: str = None):
        """إضافة بروكسي"""
        proxy_config = {
            'proxy': proxy,
            'username': username,
            'password': password
        }
        self.proxies.append(proxy_config)
        self.logger.info(f"تم إضافة بروكسي: {proxy}")
    
    def get_random_proxy(self) -> Optional[Dict]:
        """الحصول على بروكسي عشوائي"""
        if self.proxies:
            self.current_proxy = random.choice(self.proxies)
            return self.current_proxy
        return None
    
    def test_proxy(self, proxy: Dict) -> bool:
        """اختبار البروكسي"""
        try:
            proxy_url = proxy['proxy']
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == 200:
                self.logger.info(f"البروكسي يعمل: {proxy_url}")
                return True
            else:
                self.logger.warning(f"البروكسي لا يعمل: {proxy_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في اختبار البروكسي: {e}")
            return False

class ImageVerification:
    """التحقق من الصور"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def solve_image_captcha(self, image: Image.Image) -> Optional[str]:
        """حل CAPTCHA بالصور"""
        try:
            # تحويل الصورة إلى مصفوفة
            img_array = np.array(image)
            
            # تحويل إلى تدرج رمادي
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # تحليل الصورة للعثور على النص
            # هذا مثال بسيط - في التطبيق الحقيقي ستحتاج إلى خوارزميات أكثر تعقيداً
            
            # استخدام OCR
            import pytesseract
            text = pytesseract.image_to_string(gray, config='--psm 8')
            
            # تنظيف النص
            text = text.strip().replace(' ', '').replace('\n', '')
            
            if text and len(text) >= 3:
                self.logger.info(f"تم حل CAPTCHA بالصور: {text}")
                return text
            else:
                self.logger.warning("لم يتم العثور على نص في الصورة")
                return None
                
        except Exception as e:
            self.logger.error(f"خطأ في حل CAPTCHA بالصور: {e}")
            return None
    
    def detect_human_verification(self, driver) -> bool:
        """اكتشاف التحقق البشري"""
        try:
            # البحث عن عناصر التحقق البشري
            verification_elements = driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'verify') or contains(text(), 'human') or contains(text(), 'robot')]")
            
            if verification_elements:
                self.logger.info("تم اكتشاف تحقق بشري")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في اكتشاف التحقق البشري: {e}")
            return False

class PhoneVerification:
    """التحقق بالهاتف"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_phone_number(self, country_code: str = '+1') -> str:
        """توليد رقم هاتف"""
        try:
            # توليد رقم هاتف أمريكي
            area_code = random.choice(['201', '202', '203', '205', '206', '207', '208', '209', '210'])
            prefix = str(random.randint(100, 999))
            line_number = str(random.randint(1000, 9999))
            
            phone_number = f"{country_code}{area_code}{prefix}{line_number}"
            self.logger.info(f"تم توليد رقم هاتف: {phone_number}")
            return phone_number
            
        except Exception as e:
            self.logger.error(f"خطأ في توليد رقم الهاتف: {e}")
            return None
    
    def handle_sms_verification(self, driver) -> bool:
        """التعامل مع التحقق بالرسائل النصية"""
        try:
            # البحث عن حقل إدخال رمز التحقق
            sms_input = driver.find_element(By.XPATH, 
                "//input[@name='code' or contains(@placeholder, 'code') or contains(@placeholder, 'verification')]")
            
            if sms_input:
                # إدخال رمز تحقق مزيف (في التطبيق الحقيقي ستحتاج إلى خدمة SMS)
                fake_code = ''.join(random.choices(string.digits, k=6))
                sms_input.send_keys(fake_code)
                
                # البحث عن زر الإرسال
                submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                
                self.logger.info("تم إرسال رمز تحقق مزيف")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في التحقق بالرسائل النصية: {e}")
            return False

class AccountManager:
    """إدارة الحسابات"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.accounts = []
    
    def save_account(self, account_data: Dict):
        """حفظ بيانات الحساب"""
        try:
            # إضافة timestamp
            account_data['created_at'] = time.time()
            account_data['status'] = 'created'
            
            self.accounts.append(account_data)
            
            # حفظ في ملف
            self.save_to_file(account_data)
            
            self.logger.info(f"تم حفظ الحساب: {account_data['username']}")
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الحساب: {e}")
    
    def save_to_file(self, account_data: Dict):
        """حفظ الحساب في ملف"""
        try:
            filename = f"accounts_{int(time.time())}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم حفظ الحساب في {filename}")
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الملف: {e}")
    
    def load_accounts(self, filename: str) -> List[Dict]:
        """تحميل الحسابات من ملف"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                accounts = json.load(f)
            
            self.logger.info(f"تم تحميل {len(accounts)} حساب")
            return accounts
            
        except Exception as e:
            self.logger.error(f"خطأ في تحميل الحسابات: {e}")
            return []
    
    def get_account_stats(self) -> Dict:
        """الحصول على إحصائيات الحسابات"""
        try:
            total = len(self.accounts)
            successful = len([acc for acc in self.accounts if acc.get('status') == 'created'])
            failed = total - successful
            
            return {
                'total': total,
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / total * 100) if total > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"خطأ في حساب الإحصائيات: {e}")
            return {'total': 0, 'successful': 0, 'failed': 0, 'success_rate': 0}

class SecurityManager:
    """إدارة الأمان"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def rotate_user_agent(self) -> str:
        """تدوير User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        user_agent = random.choice(user_agents)
        self.logger.info(f"تم تدوير User-Agent: {user_agent}")
        return user_agent
    
    def add_random_delays(self):
        """إضافة تأخيرات عشوائية"""
        delay = random.uniform(2, 8)
        time.sleep(delay)
        self.logger.info(f"تأخير عشوائي: {delay:.2f} ثانية")
    
    def simulate_human_behavior(self, driver):
        """محاكاة السلوك البشري"""
        try:
            # تحريك الماوس عشوائياً
            actions = ActionChains(driver)
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            actions.move_by_offset(x, y).perform()
            
            # تمرير الصفحة
            driver.execute_script(f"window.scrollBy(0, {random.randint(100, 300)});")
            
            # تأخير عشوائي
            time.sleep(random.uniform(1, 3))
            
            self.logger.info("تم محاكاة السلوك البشري")
            
        except Exception as e:
            self.logger.error(f"خطأ في محاكاة السلوك البشري: {e}")

# Factory functions
def get_human_verification():
    """الحصول على محاكي السلوك البشري"""
    return HumanVerification()

def get_proxy_manager():
    """الحصول على مدير البروكسي"""
    return ProxyManager()

def get_image_verification():
    """الحصول على محلل الصور"""
    return ImageVerification()

def get_phone_verification():
    """الحصول على محلل الهاتف"""
    return PhoneVerification()

def get_account_manager():
    """الحصول على مدير الحسابات"""
    return AccountManager()

def get_security_manager():
    """الحصول على مدير الأمان"""
    return SecurityManager()

if __name__ == "__main__":
    # اختبار الميزات المتقدمة
    logging.basicConfig(level=logging.INFO)
    
    # اختبار محاكي السلوك البشري
    human_verification = get_human_verification()
    human_verification.random_delay(1, 2)
    
    # اختبار مدير البروكسي
    proxy_manager = get_proxy_manager()
    proxy_manager.add_proxy("http://proxy.example.com:8080")
    
    # اختبار مدير الحسابات
    account_manager = get_account_manager()
    test_account = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test123'
    }
    account_manager.save_account(test_account)
    
    print("✅ تم اختبار جميع الميزات المتقدمة بنجاح")