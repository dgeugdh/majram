#!/usr/bin/env python3
"""
Advanced Instagram Bot Runner
تشغيل بوت انستقرام متقدم مع جميع الميزات
"""

import os
import sys
import argparse
import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from instagram_bot import InstagramBot
from advanced_features import (
    get_human_verification,
    get_proxy_manager,
    get_image_verification,
    get_phone_verification,
    get_account_manager,
    get_security_manager
)
from human_verification import get_human_verification_system
from temp_email_advanced import get_advanced_temp_email_service
from captcha_solver import get_captcha_solver

class AdvancedInstagramBot:
    """بوت انستقرام متقدم مع جميع الميزات"""
    
    def __init__(self, config: Dict = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self.setup_logging()
        self.setup_components()
        
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        # إنشاء مجلد السجلات
        Path("logs").mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/advanced_bot.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def setup_components(self):
        """إعداد جميع المكونات"""
        try:
            # إعداد مكونات الميزات المتقدمة
            self.human_verification = get_human_verification()
            self.proxy_manager = get_proxy_manager()
            self.image_verification = get_image_verification()
            self.phone_verification = get_phone_verification()
            self.account_manager = get_account_manager()
            self.security_manager = get_security_manager()
            
            # إعداد نظام التحقق البشري
            self.human_verification_system = get_human_verification_system()
            
            # إعداد خدمة البريد المؤقت المتقدمة
            use_mock_email = self.config.get('use_mock_email', True)
            self.email_service = get_advanced_temp_email_service(use_mock=use_mock_email)
            
            # إعداد محلل CAPTCHA
            use_mock_captcha = self.config.get('use_mock_captcha', True)
            self.captcha_solver = get_captcha_solver(use_mock=use_mock_captcha)
            
            self.logger.info("✅ تم إعداد جميع المكونات بنجاح")
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في إعداد المكونات: {e}")
            raise
    
    def setup_proxies(self, proxy_list: List[str]):
        """إعداد قائمة البروكسيات"""
        try:
            for proxy in proxy_list:
                self.proxy_manager.add_proxy(proxy)
            
            self.logger.info(f"تم إضافة {len(proxy_list)} بروكسي")
            
        except Exception as e:
            self.logger.error(f"خطأ في إعداد البروكسيات: {e}")
    
    def create_advanced_account(self, user_data: Dict) -> Optional[Dict]:
        """إنشاء حساب متقدم مع جميع الميزات"""
        try:
            self.logger.info("🚀 بدء إنشاء حساب متقدم...")
            
            # إعداد البوت الأساسي
            bot = InstagramBot()
            
            # تطبيق ميزات الأمان
            self.security_manager.add_random_delays()
            user_agent = self.security_manager.rotate_user_agent()
            
            # إعداد البروكسي إذا كان متاحاً
            proxy = self.proxy_manager.get_random_proxy()
            if proxy:
                self.logger.info(f"استخدام البروكسي: {proxy['proxy']}")
            
            # إنشاء الحساب
            result = bot.run_account_creation()
            
            if result:
                # تطبيق التحقق البشري
                if self.config.get('enable_human_verification', True):
                    self.logger.info("تطبيق التحقق البشري...")
                    # هنا يمكن إضافة منطق التحقق البشري
                
                # حفظ الحساب
                self.account_manager.save_account(result)
                
                self.logger.info(f"✅ تم إنشاء الحساب بنجاح: {result['username']}")
                return result
            else:
                self.logger.error("❌ فشل في إنشاء الحساب")
                return None
                
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الحساب المتقدم: {e}")
            return None
    
    def run_batch_creation(self, num_accounts: int, delay_between: int = 5) -> Dict:
        """تشغيل إنشاء مجموعة من الحسابات"""
        try:
            self.logger.info(f"🔄 بدء إنشاء {num_accounts} حساب...")
            
            successful_accounts = []
            failed_accounts = 0
            start_time = time.time()
            
            for i in range(num_accounts):
                self.logger.info(f"📝 إنشاء الحساب {i+1}/{num_accounts}")
                
                # توليد بيانات المستخدم
                user_data = self.generate_advanced_user_data()
                
                # إنشاء الحساب
                result = self.create_advanced_account(user_data)
                
                if result:
                    successful_accounts.append(result)
                    self.logger.info(f"✅ تم إنشاء الحساب {i+1}: {result['username']}")
                else:
                    failed_accounts += 1
                    self.logger.error(f"❌ فشل في إنشاء الحساب {i+1}")
                
                # تأخير بين الحسابات
                if i < num_accounts - 1:
                    self.logger.info(f"⏳ انتظار {delay_between} ثواني...")
                    time.sleep(delay_between)
            
            # حساب الإحصائيات
            end_time = time.time()
            duration = end_time - start_time
            success_rate = (len(successful_accounts) / num_accounts) * 100
            
            stats = {
                'total_accounts': num_accounts,
                'successful_accounts': len(successful_accounts),
                'failed_accounts': failed_accounts,
                'success_rate': success_rate,
                'duration_seconds': duration,
                'accounts_per_minute': (len(successful_accounts) / duration) * 60,
                'accounts': successful_accounts
            }
            
            self.logger.info(f"📊 النتائج النهائية:")
            self.logger.info(f"   الحسابات الناجحة: {len(successful_accounts)}")
            self.logger.info(f"   الحسابات الفاشلة: {failed_accounts}")
            self.logger.info(f"   معدل النجاح: {success_rate:.1f}%")
            self.logger.info(f"   المدة: {duration:.1f} ثانية")
            self.logger.info(f"   الحسابات/الدقيقة: {stats['accounts_per_minute']:.1f}")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء المجموعة: {e}")
            return {
                'total_accounts': num_accounts,
                'successful_accounts': 0,
                'failed_accounts': num_accounts,
                'success_rate': 0,
                'duration_seconds': 0,
                'accounts_per_minute': 0,
                'accounts': []
            }
    
    def generate_advanced_user_data(self) -> Dict:
        """توليد بيانات مستخدم متقدمة"""
        try:
            from faker import Faker
            fake = Faker()
            
            # توليد بيانات شخصية
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))
            
            # توليد بريد مؤقت
            email = self.email_service.generate_email()
            
            # توليد رقم هاتف
            phone_number = self.phone_verification.generate_phone_number()
            
            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'password': password,
                'email': email,
                'phone': phone_number,
                'created_at': time.time()
            }
            
            self.logger.info(f"تم توليد بيانات المستخدم: {username}")
            return user_data
            
        except Exception as e:
            self.logger.error(f"خطأ في توليد بيانات المستخدم: {e}")
            return {}
    
    def test_all_components(self) -> bool:
        """اختبار جميع المكونات"""
        try:
            self.logger.info("🧪 اختبار جميع المكونات...")
            
            # اختبار خدمة البريد المؤقت
            email = self.email_service.generate_email()
            self.logger.info(f"✅ خدمة البريد المؤقت: {email}")
            
            # اختبار محلل CAPTCHA
            from PIL import Image
            test_image = Image.new('RGB', (200, 50), color='white')
            captcha_result = self.captcha_solver.solve_captcha(test_image)
            self.logger.info(f"✅ محلل CAPTCHA: {captcha_result}")
            
            # اختبار توليد رقم الهاتف
            phone = self.phone_verification.generate_phone_number()
            self.logger.info(f"✅ توليد رقم الهاتف: {phone}")
            
            # اختبار مدير الحسابات
            test_account = {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'test123'
            }
            self.account_manager.save_account(test_account)
            self.logger.info("✅ مدير الحسابات")
            
            # اختبار مدير الأمان
            user_agent = self.security_manager.rotate_user_agent()
            self.logger.info(f"✅ مدير الأمان: {user_agent[:50]}...")
            
            self.logger.info("✅ جميع المكونات تعمل بشكل صحيح")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ فشل في اختبار المكونات: {e}")
            return False
    
    def save_results(self, results: Dict, filename: str = None):
        """حفظ النتائج في ملف"""
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"results_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 تم حفظ النتائج في {filename}")
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ النتائج: {e}")

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="بوت انستقرام متقدم",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python run_advanced.py --test                    # اختبار المكونات
  python run_advanced.py --single                 # إنشاء حساب واحد
  python run_advanced.py --batch 5                # إنشاء 5 حسابات
  python run_advanced.py --batch 10 --delay 10    # إنشاء 10 حسابات مع تأخير 10 ثواني
        """
    )
    
    parser.add_argument('--test', action='store_true',
                       help='اختبار جميع المكونات')
    parser.add_argument('--single', action='store_true',
                       help='إنشاء حساب واحد')
    parser.add_argument('--batch', type=int, metavar='N',
                       help='إنشاء N حسابات')
    parser.add_argument('--delay', type=int, default=5,
                       help='التأخير بين الحسابات (ثواني)')
    parser.add_argument('--config', type=str,
                       help='ملف التكوين JSON')
    parser.add_argument('--proxies', type=str,
                       help='قائمة البروكسيات مفصولة بفواصل')
    parser.add_argument('--output', type=str,
                       help='ملف حفظ النتائج')
    
    args = parser.parse_args()
    
    # تحميل التكوين
    config = {}
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل ملف التكوين: {e}")
            return 1
    
    # إنشاء البوت المتقدم
    bot = AdvancedInstagramBot(config)
    
    # إعداد البروكسيات
    if args.proxies:
        proxy_list = args.proxies.split(',')
        bot.setup_proxies(proxy_list)
    
    # اختبار المكونات
    if args.test:
        if bot.test_all_components():
            print("✅ جميع الاختبارات نجحت")
            return 0
        else:
            print("❌ فشل في الاختبارات")
            return 1
    
    # إنشاء حساب واحد
    if args.single:
        user_data = bot.generate_advanced_user_data()
        result = bot.create_advanced_account(user_data)
        if result:
            print(f"✅ تم إنشاء الحساب: {result['username']}")
            return 0
        else:
            print("❌ فشل في إنشاء الحساب")
            return 1
    
    # إنشاء مجموعة حسابات
    if args.batch:
        if args.batch < 1 or args.batch > 50:
            print("عدد الحسابات يجب أن يكون بين 1 و 50")
            return 1
        
        results = bot.run_batch_creation(args.batch, args.delay)
        
        # حفظ النتائج
        if args.output:
            bot.save_results(results, args.output)
        else:
            bot.save_results(results)
        
        if results['successful_accounts'] > 0:
            print(f"✅ تم إنشاء {results['successful_accounts']} حساب بنجاح")
            return 0
        else:
            print("❌ فشل في إنشاء أي حساب")
            return 1
    
    # إذا لم يتم تحديد أي خيار، عرض المساعدة
    parser.print_help()
    return 1

if __name__ == "__main__":
    import random
    import string
    
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)