# بوت إنشاء حسابات انستجرام 🤖

بوت متقدم لإنشاء حسابات انستجرام تلقائياً مع تكامل بشري وبريد إلكتروني مؤقت.

## المميزات ✨

- **إنشاء حسابات تلقائي**: إنشاء حسابات انستجرام بكميات كبيرة
- **تكامل بشري**: معالجة CAPTCHA والتحقق البشري
- **بريد مؤقت**: استخدام بريد إلكتروني مؤقت للتحقق
- **واجهة ويب حديثة**: واجهة مستخدم جميلة وسهلة الاستخدام
- **إحصائيات في الوقت الفعلي**: مراقبة التقدم والنتائج
- **تصدير النتائج**: حفظ الحسابات المُنشأة بصيغة CSV

## المتطلبات 📋

### متطلبات النظام
- Python 3.8+
- Chrome Browser
- Tesseract OCR (اختياري للـ CAPTCHA)

### متطلبات Python
```
selenium==4.15.2
requests==2.31.0
beautifulsoup4==4.12.2
fake-useragent==1.4.0
undetected-chromedriver==3.5.4
webdriver-manager==4.0.1
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
pyautogui==0.9.54
speechrecognition==3.10.0
pyaudio==0.2.11
pyttsx3==2.90
temp-mail==1.0.0
faker==20.1.0
```

## التثبيت 🚀

### 1. استنساخ المشروع
```bash
git clone <repository-url>
cd instagram-bot
```

### 2. إنشاء البيئة الافتراضية
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. تثبيت Tesseract (اختياري)
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# تحميل من: https://github.com/UB-Mannheim/tesseract/wiki
```

## الاستخدام 💻

### تشغيل الواجهة الرسومية
```bash
python web_interface.py
```

ثم افتح المتصفح على: `http://localhost:5000`

### تشغيل البوت مباشرة
```bash
python instagram_bot.py
```

## كيفية العمل 🔧

### 1. إنشاء البيانات العشوائية
- أسماء عشوائية باستخدام Faker
- أسماء مستخدمين فريدة
- كلمات مرور قوية
- بريد إلكتروني مؤقت

### 2. معالجة التحقق البشري
- **CAPTCHA**: حل تلقائي باستخدام OCR أو خدمات خارجية
- **تحقق الهاتف**: استخدام أرقام وهمية
- **تحقق البريد**: استخدام بريد مؤقت

### 3. إنشاء الحساب
- ملء النموذج تلقائياً
- معالجة الأخطاء والاستثناءات
- تسجيل العملية بالكامل

## الملفات 📁

```
instagram-bot/
├── instagram_bot.py          # البوت الرئيسي
├── web_interface.py          # واجهة الويب
├── temp_email_service.py     # خدمة البريد المؤقت
├── captcha_solver.py         # حل CAPTCHA
├── requirements.txt          # متطلبات Python
├── README.md                # هذا الملف
├── templates/
│   └── index.html           # قالب الواجهة
├── static/
│   ├── css/
│   │   └── style.css        # التصميم
│   └── js/
│       └── app.js           # JavaScript
└── logs/
    └── instagram_bot.log    # سجلات البوت
```

## الإعدادات ⚙️

### متغيرات البيئة
إنشاء ملف `.env`:
```env
# إعدادات البوت
BOT_DELAY=2
MAX_ACCOUNTS=10
CAPTCHA_SOLVER_API_KEY=your_api_key

# إعدادات الويب
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=True
```

### إعدادات متقدمة
```python
# في instagram_bot.py
class InstagramBot:
    def __init__(self):
        self.delay_between_accounts = 2  # ثواني
        self.max_retries = 3
        self.captcha_timeout = 60
        self.email_timeout = 120
```

## الأمان 🔒

### نصائح مهمة
- استخدم VPN لتجنب الحظر
- غير User-Agent بشكل دوري
- استخدم proxies متعددة
- لا تزيد عن 10 حسابات في اليوم
- احترم شروط استخدام انستجرام

### إعدادات الأمان
```python
# إعدادات Chrome المتقدمة
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
```

## استكشاف الأخطاء 🔍

### مشاكل شائعة

#### 1. خطأ في Chrome Driver
```bash
# تحديث Chrome Driver
pip install --upgrade webdriver-manager
```

#### 2. خطأ في CAPTCHA
```python
# استخدام خدمة خارجية
solver = CaptchaSolver()
solution = solver.solve_captcha_api(image)
```

#### 3. خطأ في البريد المؤقت
```python
# استخدام خدمة بريد مختلفة
email_service = TemporaryEmailService()
email = email_service.generate_email()
```

### سجلات الأخطاء
```bash
# مراجعة السجلات
tail -f logs/instagram_bot.log
```

## المساهمة 🤝

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:

1. Fork المشروع
2. إنشاء branch جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى Branch (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## الترخيص 📄

هذا المشروع مرخص تحت رخصة MIT. راجع ملف `LICENSE` للتفاصيل.

## تنبيه قانوني ⚠️

هذا المشروع للأغراض التعليمية فقط. المستخدم مسؤول عن الامتثال لشروط استخدام انستجرام والقوانين المحلية. لا نتحمل أي مسؤولية عن الاستخدام غير القانوني.

## الدعم 💬

إذا واجهت أي مشاكل أو لديك أسئلة:

- افتح Issue جديد
- راجع الوثائق
- تواصل مع المطورين

## التحديثات القادمة 🚀

- [ ] دعم reCAPTCHA
- [ ] معالجة الصور المتقدمة
- [ ] دعم متصفحات متعددة
- [ ] واجهة API
- [ ] نظام إدارة الحسابات
- [ ] إحصائيات متقدمة

---

**ملاحظة**: هذا المشروع للأغراض التعليمية فقط. يرجى استخدامه بمسؤولية واحترام شروط الخدمة.