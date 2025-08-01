#!/bin/bash

# Instagram Bot Starter Script
# سكريبت تشغيل بوت انستقرام

echo "🚀 بدء تشغيل بوت انستقرام..."

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت. يرجى تثبيت Python 3.8+"
    exit 1
fi

# التحقق من وجود المتطلبات
if [ ! -f "requirements.txt" ]; then
    echo "❌ ملف requirements.txt غير موجود"
    exit 1
fi

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip3 install -r requirements.txt

# إنشاء مجلد السجلات
mkdir -p logs

# عرض خيارات التشغيل
echo ""
echo "🔧 خيارات التشغيل:"
echo "1. تشغيل واجهة الويب"
echo "2. إنشاء حساب واحد"
echo "3. إنشاء عدة حسابات"
echo "4. اختبار المكونات"
echo "5. تشغيل البوت المتقدم"
echo ""

read -p "اختر رقم الخيار (1-5): " choice

case $choice in
    1)
        echo "🌐 تشغيل واجهة الويب..."
        python3 web_interface.py
        ;;
    2)
        echo "👤 إنشاء حساب واحد..."
        python3 run.py --single
        ;;
    3)
        read -p "أدخل عدد الحسابات (1-10): " num_accounts
        if [ "$num_accounts" -ge 1 ] && [ "$num_accounts" -le 10 ]; then
            echo "👥 إنشاء $num_accounts حسابات..."
            python3 run.py --multiple $num_accounts
        else
            echo "❌ عدد الحسابات يجب أن يكون بين 1 و 10"
            exit 1
        fi
        ;;
    4)
        echo "🧪 اختبار المكونات..."
        python3 run.py --test
        ;;
    5)
        echo "🚀 تشغيل البوت المتقدم..."
        echo "خيارات البوت المتقدم:"
        echo "1. اختبار المكونات"
        echo "2. إنشاء حساب واحد"
        echo "3. إنشاء عدة حسابات"
        echo ""
        read -p "اختر رقم الخيار (1-3): " advanced_choice
        
        case $advanced_choice in
            1)
                python3 run_advanced.py --test
                ;;
            2)
                python3 run_advanced.py --single
                ;;
            3)
                read -p "أدخل عدد الحسابات (1-50): " num_accounts
                if [ "$num_accounts" -ge 1 ] && [ "$num_accounts" -le 50 ]; then
                    read -p "أدخل التأخير بين الحسابات (ثواني): " delay
                    python3 run_advanced.py --batch $num_accounts --delay $delay
                else
                    echo "❌ عدد الحسابات يجب أن يكون بين 1 و 50"
                    exit 1
                fi
                ;;
            *)
                echo "❌ خيار غير صحيح"
                exit 1
                ;;
        esac
        ;;
    *)
        echo "❌ خيار غير صحيح"
        exit 1
        ;;
esac

echo ""
echo "✅ تم الانتهاء من تشغيل البوت"