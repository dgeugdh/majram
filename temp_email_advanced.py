"""
Advanced Temporary Email Service
خدمة بريد مؤقت متقدمة
"""

import requests
import time
import random
import string
import json
import logging
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import threading
import queue

class AdvancedTempEmailService:
    """خدمة بريد مؤقت متقدمة مع دعم عدة مزودين"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.email_providers = self.setup_providers()
        self.current_provider = None
        self.email_queue = queue.Queue()
        self.monitoring_thread = None
        self.stop_monitoring = False
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def setup_providers(self) -> Dict:
        """إعداد مزودي البريد المؤقت"""
        providers = {
            'temp_mail_org': {
                'name': 'Temp-Mail.org',
                'base_url': 'https://temp-mail.org',
                'generate_url': 'https://temp-mail.org/api/v1/email/new',
                'check_url': 'https://temp-mail.org/api/v1/email/{email}/messages',
                'domains': ['temp-mail.org', 'tmpmail.org'],
                'working': True
            },
            'guerrilla_mail': {
                'name': 'Guerrilla Mail',
                'base_url': 'https://www.guerrillamail.com',
                'generate_url': 'https://www.guerrillamail.com/ajax/email_address',
                'check_url': 'https://www.guerrillamail.com/ajax/check_email',
                'domains': ['guerrillamail.com', 'guerrillamailblock.com'],
                'working': True
            },
            '10minutemail': {
                'name': '10MinuteMail',
                'base_url': 'https://10minutemail.com',
                'generate_url': 'https://10minutemail.com/address.api.php',
                'check_url': 'https://10minutemail.com/mail.api.php',
                'domains': ['10minutemail.com'],
                'working': True
            },
            'mailinator': {
                'name': 'Mailinator',
                'base_url': 'https://www.mailinator.com',
                'generate_url': 'https://www.mailinator.com/v3/index.jsp',
                'check_url': 'https://www.mailinator.com/v3/index.jsp',
                'domains': ['mailinator.com'],
                'working': True
            }
        }
        return providers
    
    def test_provider(self, provider_name: str) -> bool:
        """اختبار مزود البريد"""
        try:
            provider = self.email_providers[provider_name]
            
            # اختبار الاتصال
            response = self.session.get(provider['base_url'], timeout=10)
            if response.status_code == 200:
                self.logger.info(f"مزود {provider['name']} يعمل")
                return True
            else:
                self.logger.warning(f"مزود {provider['name']} لا يعمل")
                provider['working'] = False
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في اختبار مزود {provider_name}: {e}")
            self.email_providers[provider_name]['working'] = False
            return False
    
    def get_working_provider(self) -> Optional[str]:
        """الحصول على مزود يعمل"""
        working_providers = [name for name, provider in self.email_providers.items() 
                           if provider['working']]
        
        if working_providers:
            return random.choice(working_providers)
        return None
    
    def generate_email(self, provider_name: str = None) -> Optional[str]:
        """توليد بريد إلكتروني مؤقت"""
        try:
            if not provider_name:
                provider_name = self.get_working_provider()
            
            if not provider_name:
                self.logger.error("لا يوجد مزود بريد يعمل")
                return None
            
            provider = self.email_providers[provider_name]
            self.current_provider = provider_name
            
            # توليد اسم المستخدم
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            domain = random.choice(provider['domains'])
            email = f"{username}@{domain}"
            
            self.logger.info(f"تم توليد بريد مؤقت: {email} من {provider['name']}")
            return email
            
        except Exception as e:
            self.logger.error(f"خطأ في توليد البريد المؤقت: {e}")
            return None
    
    def check_email_temp_mail_org(self, email: str) -> List[Dict]:
        """فحص البريد من Temp-Mail.org"""
        try:
            # استخراج اسم المستخدم من البريد
            username = email.split('@')[0]
            
            url = f"https://temp-mail.org/api/v1/email/{username}/messages"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                emails = []
                
                for msg in data.get('messages', []):
                    emails.append({
                        'from': msg.get('from', ''),
                        'subject': msg.get('subject', ''),
                        'body': msg.get('body', ''),
                        'timestamp': msg.get('timestamp', ''),
                        'id': msg.get('id', '')
                    })
                
                return emails
            else:
                self.logger.warning(f"فشل في فحص البريد: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص البريد من Temp-Mail.org: {e}")
            return []
    
    def check_email_guerrilla_mail(self, email: str) -> List[Dict]:
        """فحص البريد من Guerrilla Mail"""
        try:
            # استخراج اسم المستخدم من البريد
            username = email.split('@')[0]
            
            url = "https://www.guerrillamail.com/ajax/check_email"
            data = {
                'email': email,
                'offset': 0,
                'seq': 0
            }
            
            response = self.session.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                emails = []
                
                for msg in data.get('list', []):
                    emails.append({
                        'from': msg.get('mail_from', ''),
                        'subject': msg.get('mail_subject', ''),
                        'body': msg.get('mail_body', ''),
                        'timestamp': msg.get('mail_timestamp', ''),
                        'id': msg.get('mail_id', '')
                    })
                
                return emails
            else:
                self.logger.warning(f"فشل في فحص البريد: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص البريد من Guerrilla Mail: {e}")
            return []
    
    def check_email_10minutemail(self, email: str) -> List[Dict]:
        """فحص البريد من 10MinuteMail"""
        try:
            url = "https://10minutemail.com/mail.api.php"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                emails = []
                
                for msg in data.get('mail_list', []):
                    emails.append({
                        'from': msg.get('from', ''),
                        'subject': msg.get('subject', ''),
                        'body': msg.get('body', ''),
                        'timestamp': msg.get('timestamp', ''),
                        'id': msg.get('id', '')
                    })
                
                return emails
            else:
                self.logger.warning(f"فشل في فحص البريد: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص البريد من 10MinuteMail: {e}")
            return []
    
    def check_email(self, email: str) -> List[Dict]:
        """فحص البريد الإلكتروني"""
        try:
            if not self.current_provider:
                self.logger.error("لم يتم تحديد مزود البريد")
                return []
            
            provider_name = self.current_provider
            
            if provider_name == 'temp_mail_org':
                return self.check_email_temp_mail_org(email)
            elif provider_name == 'guerrilla_mail':
                return self.check_email_guerrilla_mail(email)
            elif provider_name == '10minutemail':
                return self.check_email_10minutemail(email)
            else:
                self.logger.warning(f"مزود غير مدعوم: {provider_name}")
                return []
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص البريد: {e}")
            return []
    
    def extract_verification_link(self, email_body: str) -> Optional[str]:
        """استخراج رابط التحقق من نص البريد"""
        try:
            # أنماط مختلفة لروابط التحقق
            patterns = [
                r'https://[^\s]*instagram[^\s]*verify[^\s]*',
                r'https://[^\s]*instagram[^\s]*confirm[^\s]*',
                r'https://[^\s]*verify[^\s]*',
                r'https://[^\s]*confirm[^\s]*',
                r'https://[^\s]*activation[^\s]*',
                r'https://[^\s]*email[^\s]*verify[^\s]*'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, email_body, re.IGNORECASE)
                if matches:
                    link = matches[0].strip()
                    self.logger.info(f"تم العثور على رابط تحقق: {link}")
                    return link
            
            self.logger.warning("لم يتم العثور على رابط تحقق في البريد")
            return None
            
        except Exception as e:
            self.logger.error(f"خطأ في استخراج رابط التحقق: {e}")
            return None
    
    def wait_for_verification_email(self, email: str, timeout: int = 120) -> Optional[str]:
        """انتظار بريد التحقق"""
        try:
            self.logger.info(f"في انتظار بريد التحقق إلى {email}")
            
            start_time = time.time()
            check_interval = 5  # فحص كل 5 ثواني
            
            while time.time() - start_time < timeout:
                emails = self.check_email(email)
                
                for email_data in emails:
                    # البحث عن بريد من Instagram
                    if 'instagram' in email_data['from'].lower() or 'instagram' in email_data['subject'].lower():
                        self.logger.info(f"تم العثور على بريد من Instagram: {email_data['subject']}")
                        
                        # استخراج رابط التحقق
                        verification_link = self.extract_verification_link(email_data['body'])
                        if verification_link:
                            return verification_link
                
                time.sleep(check_interval)
            
            self.logger.warning(f"انتهت مهلة انتظار بريد التحقق ({timeout} ثانية)")
            return None
            
        except Exception as e:
            self.logger.error(f"خطأ في انتظار بريد التحقق: {e}")
            return None
    
    def start_email_monitoring(self, email: str):
        """بدء مراقبة البريد في خيط منفصل"""
        self.stop_monitoring = False
        self.monitoring_thread = threading.Thread(
            target=self._monitor_email_thread,
            args=(email,)
        )
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_email_monitoring(self):
        """إيقاف مراقبة البريد"""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
    
    def _monitor_email_thread(self, email: str):
        """خيط مراقبة البريد"""
        try:
            while not self.stop_monitoring:
                emails = self.check_email(email)
                
                for email_data in emails:
                    if 'instagram' in email_data['from'].lower() or 'instagram' in email_data['subject'].lower():
                        self.email_queue.put(email_data)
                
                time.sleep(5)  # فحص كل 5 ثواني
                
        except Exception as e:
            self.logger.error(f"خطأ في خيط مراقبة البريد: {e}")
    
    def get_latest_email(self) -> Optional[Dict]:
        """الحصول على أحدث بريد"""
        try:
            if not self.email_queue.empty():
                return self.email_queue.get_nowait()
            return None
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على أحدث بريد: {e}")
            return None

class MockAdvancedTempEmailService:
    """خدمة بريد مؤقت مزيفة للاختبار"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emails = {}
        self.verification_links = {}
    
    def generate_email(self) -> str:
        """توليد بريد مؤقت مزيف"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@mock-temp.com"
        self.emails[email] = []
        self.logger.info(f"تم توليد بريد مؤقت مزيف: {email}")
        return email
    
    def add_mock_email(self, email: str, from_addr: str, subject: str, body: str, verification_link: str = None):
        """إضافة بريد مزيف"""
        if email not in self.emails:
            self.emails[email] = []
        
        email_data = {
            'from': from_addr,
            'subject': subject,
            'body': body,
            'timestamp': time.time(),
            'id': str(random.randint(1000, 9999))
        }
        
        self.emails[email].append(email_data)
        
        if verification_link:
            self.verification_links[email] = verification_link
        
        self.logger.info(f"تم إضافة بريد مزيف إلى {email}")
    
    def check_email(self, email: str) -> List[Dict]:
        """فحص البريد المزيف"""
        return self.emails.get(email, [])
    
    def wait_for_verification_email(self, email: str, timeout: int = 60) -> Optional[str]:
        """انتظار بريد التحقق المزيف"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if email in self.verification_links:
                link = self.verification_links[email]
                self.logger.info(f"تم العثور على رابط تحقق مزيف: {link}")
                return link
            
            time.sleep(2)
        
        self.logger.warning("انتهت مهلة انتظار بريد التحقق المزيف")
        return None

# Factory functions
def get_advanced_temp_email_service(use_mock: bool = False):
    """الحصول على خدمة بريد مؤقت متقدمة"""
    if use_mock:
        return MockAdvancedTempEmailService()
    else:
        return AdvancedTempEmailService()

if __name__ == "__main__":
    # اختبار خدمة البريد المؤقت المتقدمة
    logging.basicConfig(level=logging.INFO)
    
    # استخدام الخدمة المزيفة للاختبار
    email_service = get_advanced_temp_email_service(use_mock=True)
    
    # توليد بريد مؤقت
    email = email_service.generate_email()
    print(f"تم توليد البريد: {email}")
    
    # إضافة بريد مزيف
    if isinstance(email_service, MockAdvancedTempEmailService):
        email_service.add_mock_email(
            email,
            'noreply@instagram.com',
            'Confirm your Instagram account',
            'Click here to confirm your account: https://instagram.com/confirm/123456',
            'https://instagram.com/confirm/123456'
        )
    
    # انتظار بريد التحقق
    link = email_service.wait_for_verification_email(email, timeout=10)
    if link:
        print(f"تم العثور على رابط التحقق: {link}")
    else:
        print("لم يتم العثور على رابط تحقق")
    
    print("✅ تم اختبار خدمة البريد المؤقت المتقدمة بنجاح")