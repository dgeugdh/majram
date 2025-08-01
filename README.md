# بوت إنشاء حسابات انستقرام

## نظرة عامة

بوت متقدم لإنشاء حسابات انستقرام تلقائياً مع تكامل البريد المؤقت والتحقق البشري. يتضمن واجهة ويب حديثة ووظائف متقدمة للتعامل مع التحديات المختلفة.

## المميزات

### 🔧 الوظائف الأساسية
- إنشاء حسابات انستقرام تلقائياً
- توليد بيانات عشوائية واقعية
- تكامل مع خدمات البريد المؤقت
- حل CAPTCHA تلقائياً
- التعامل مع التحقق بالهاتف
- واجهة ويب حديثة وسهلة الاستخدام

### 🛡️ ميزات الأمان
- استخدام متصفح غير قابل للكشف
- محاكاة السلوك البشري
- تأخير عشوائي بين العمليات
- تدوير User-Agent
- إخفاء بصمات المتصفح

### 📊 المراقبة والإحصائيات
- تتبع التقدم في الوقت الفعلي
- سجل مفصل للعمليات
- إحصائيات النجاح والفشل
- واجهة إدارية متقدمة

## المتطلبات

### متطلبات النظام
- Python 3.8+
- Chrome/Chromium browser
- نظام تشغيل Linux/Windows/macOS

### المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

## التثبيت والإعداد

### 1. استنساخ المشروع
```bash
git clone <repository-url>
cd instagram-bot
```

### 2. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 3. إعداد المتغيرات البيئية
```bash
cp .env.example .env
# تعديل ملف .env حسب الحاجة
```

### 4. تشغيل التطبيق
```bash
python web_interface.py
```

## الاستخدام

### الواجهة الرسومية
1. افتح المتصفح وانتقل إلى `http://localhost:5000`
2. أدخل عدد الحسابات المطلوبة
3. اضبط التأخير بين الحسابات
4. اضغط "بدء البوت"
5. راقب التقدم والإحصائيات

### الاستخدام من سطر الأوامر
```bash
python instagram_bot.py
```

## هيكل المشروع

```
instagram-bot/
├── instagram_bot.py          # البوت الرئيسي
├── web_interface.py          # واجهة الويب
├── temp_email_service.py     # خدمة البريد المؤقت
├── captcha_solver.py         # حل CAPTCHA
├── requirements.txt          # المتطلبات
├── README.md                # هذا الملف
├── templates/
│   └── index.html           # قالب الواجهة
├── static/
│   ├── css/
│   │   └── style.css        # التنسيقات
│   └── js/
│       └── app.js           # JavaScript
└── logs/
    └── instagram_bot.log    # سجل العمليات
```

## المكونات الرئيسية

### 1. InstagramBot Class
```python
from instagram_bot import InstagramBot

bot = InstagramBot()
result = bot.run_account_creation()
```

**الوظائف الرئيسية:**
- `setup_driver()`: إعداد متصفح Chrome
- `generate_random_user_data()`: توليد بيانات عشوائية
- `create_instagram_account()`: إنشاء الحساب
- `solve_captcha()`: حل CAPTCHA
- `handle_phone_verification()`: التحقق بالهاتف

### 2. TemporaryEmailService
```python
from temp_email_service import get_email_service

email_service = get_email_service()
email = email_service.generate_email()
```

**الوظائف:**
- توليد عناوين بريد مؤقتة
- فحص البريد الوارد
- استخراج روابط التحقق

### 3. CaptchaSolver
```python
from captcha_solver import get_captcha_solver

solver = get_captcha_solver()
solution = solver.solve_captcha(image)
```

**الطرق المدعومة:**
- OCR (Tesseract)
- API services (2captcha)
- Manual solving

## الإعدادات المتقدمة

### تكوين CAPTCHA Solver
```python
# في ملف .env
CAPTCHA_API_KEY=your_2captcha_api_key
CAPTCHA_METHOD=api  # or 'ocr', 'manual'
```

### إعدادات المتصفح
```python
# في instagram_bot.py
options.add_argument('--proxy-server=your_proxy')
options.add_argument('--user-agent=custom_user_agent')
```

### تكوين البريد المؤقت
```python
# في temp_email_service.py
EMAIL_SERVICE_URL=your_temp_email_api
EMAIL_CHECK_INTERVAL=5
```

## استكشاف الأخطاء

### مشاكل شائعة

#### 1. فشل في إعداد المتصفح
```bash
# تأكد من تثبيت Chrome
sudo apt-get install chromium-browser  # Ubuntu/Debian
```

#### 2. مشاكل CAPTCHA
```bash
# تثبيت Tesseract
sudo apt-get install tesseract-ocr
```

#### 3. مشاكل الشبكة
```bash
# فحص الاتصال
ping instagram.com
```

### سجلات الأخطاء
```bash
# عرض السجلات
tail -f logs/instagram_bot.log
```

## الأمان والخصوصية

### أفضل الممارسات
- استخدام VPN أو Proxy
- تدوير عناوين IP
- تغيير User-Agent بانتظام
- إضافة تأخير عشوائي
- عدم تجاوز حدود Instagram

### التحذيرات
⚠️ **تحذير مهم:** هذا البوت مخصص للاستخدام التعليمي فقط. يرجى احترام شروط خدمة Instagram.

## المساهمة

### كيفية المساهمة
1. Fork المشروع
2. إنشاء branch جديد
3. إجراء التعديلات
4. إرسال Pull Request

### معايير الكود
- اتباع PEP 8
- إضافة تعليقات باللغة العربية
- كتابة اختبارات للوظائف الجديدة

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف `LICENSE` للتفاصيل.

## الدعم

### الحصول على المساعدة
- إنشاء Issue في GitHub
- مراجعة الوثائق
- فحص سجلات الأخطاء

### الموارد المفيدة
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Instagram API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [CAPTCHA Solving Services](https://2captcha.com/)

## التحديثات المستقبلية

### المخططات القادمة
- [ ] دعم Instagram API الرسمي
- [ ] تحسين حل CAPTCHA
- [ ] إضافة دعم للصور الشخصية
- [ ] واجهة إدارية متقدمة
- [ ] دعم متعدد اللغات
- [ ] نظام قواعد البيانات

### طلبات الميزات
إذا كان لديك اقتراح لميزة جديدة، يرجى إنشاء Issue مع وصف مفصل.

---

**ملاحظة:** هذا المشروع مخصص للاستخدام التعليمي والبحثي فقط. يرجى احترام شروط خدمة Instagram وقوانين الخصوصية المحلية.