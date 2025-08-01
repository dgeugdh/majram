#!/usr/bin/env python3
"""
Instagram Bot Runner
تشغيل بوت انستقرام مع واجهة ويب
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_interface import app
from instagram_bot import InstagramBot
from temp_email_service import get_email_service
from captcha_solver import get_captcha_solver

def setup_logging():
    """إعداد نظام التسجيل"""
    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    Path("logs").mkdir(exist_ok=True)
    
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/instagram_bot.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def test_components():
    """اختبار المكونات الأساسية"""
    logger = logging.getLogger(__name__)
    
    try:
        # اختبار خدمة البريد المؤقت
        logger.info("اختبار خدمة البريد المؤقت...")
        email_service = get_email_service(use_mock=True)
        email = email_service.generate_email()
        logger.info(f"تم إنشاء بريد مؤقت: {email}")
        
        # اختبار حل CAPTCHA
        logger.info("اختبار حل CAPTCHA...")
        captcha_solver = get_captcha_solver(use_mock=True)
        logger.info("تم تهيئة حل CAPTCHA بنجاح")
        
        # اختبار البوت
        logger.info("اختبار البوت...")
        bot = InstagramBot()
        logger.info("تم تهيئة البوت بنجاح")
        
        logger.info("✅ جميع المكونات تعمل بشكل صحيح")
        return True
        
    except Exception as e:
        logger.error(f"❌ فشل في اختبار المكونات: {e}")
        return False

def run_web_interface(host='0.0.0.0', port=5000, debug=False):
    """تشغيل واجهة الويب"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"تشغيل واجهة الويب على http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.error(f"فشل في تشغيل واجهة الويب: {e}")

def run_single_account():
    """تشغيل إنشاء حساب واحد"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("بدء إنشاء حساب انستقرام واحد...")
        bot = InstagramBot()
        result = bot.run_account_creation()
        
        if result:
            logger.info(f"✅ تم إنشاء الحساب بنجاح: {result}")
            return result
        else:
            logger.error("❌ فشل في إنشاء الحساب")
            return None
            
    except Exception as e:
        logger.error(f"خطأ في إنشاء الحساب: {e}")
        return None

def run_multiple_accounts(num_accounts):
    """تشغيل إنشاء عدة حسابات"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"بدء إنشاء {num_accounts} حسابات...")
        
        successful_accounts = []
        failed_accounts = 0
        
        for i in range(num_accounts):
            logger.info(f"إنشاء الحساب {i+1}/{num_accounts}")
            
            bot = InstagramBot()
            result = bot.run_account_creation()
            
            if result:
                successful_accounts.append(result)
                logger.info(f"✅ تم إنشاء الحساب {i+1}: {result['username']}")
            else:
                failed_accounts += 1
                logger.error(f"❌ فشل في إنشاء الحساب {i+1}")
        
        # طباعة النتائج
        logger.info(f"\n📊 النتائج النهائية:")
        logger.info(f"الحسابات الناجحة: {len(successful_accounts)}")
        logger.info(f"الحسابات الفاشلة: {failed_accounts}")
        logger.info(f"معدل النجاح: {(len(successful_accounts)/num_accounts)*100:.1f}%")
        
        return successful_accounts
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء الحسابات: {e}")
        return []

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="بوت إنشاء حسابات انستقرام",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python run.py --web                    # تشغيل واجهة الويب
  python run.py --single                 # إنشاء حساب واحد
  python run.py --multiple 5             # إنشاء 5 حسابات
  python run.py --test                   # اختبار المكونات
        """
    )
    
    parser.add_argument('--web', action='store_true', 
                       help='تشغيل واجهة الويب')
    parser.add_argument('--single', action='store_true',
                       help='إنشاء حساب واحد')
    parser.add_argument('--multiple', type=int, metavar='N',
                       help='إنشاء N حسابات')
    parser.add_argument('--test', action='store_true',
                       help='اختبار المكونات')
    parser.add_argument('--host', default='0.0.0.0',
                       help='عنوان المضيف لواجهة الويب (افتراضي: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000,
                       help='منفذ واجهة الويب (افتراضي: 5000)')
    parser.add_argument('--debug', action='store_true',
                       help='تفعيل وضع التصحيح')
    
    args = parser.parse_args()
    
    # إعداد التسجيل
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 بدء تشغيل بوت انستقرام...")
    
    # اختبار المكونات إذا طُلب
    if args.test:
        if test_components():
            logger.info("✅ جميع الاختبارات نجحت")
            return 0
        else:
            logger.error("❌ فشل في الاختبارات")
            return 1
    
    # تشغيل واجهة الويب
    if args.web:
        run_web_interface(args.host, args.port, args.debug)
        return 0
    
    # إنشاء حساب واحد
    if args.single:
        result = run_single_account()
        return 0 if result else 1
    
    # إنشاء عدة حسابات
    if args.multiple:
        if args.multiple < 1 or args.multiple > 10:
            logger.error("عدد الحسابات يجب أن يكون بين 1 و 10")
            return 1
        
        results = run_multiple_accounts(args.multiple)
        return 0 if results else 1
    
    # إذا لم يتم تحديد أي خيار، عرض المساعدة
    parser.print_help()
    return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)