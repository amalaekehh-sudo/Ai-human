"""
🎬 Workflow Helper - راهنمای گام به گام

این script بهت کمک می‌کنه تا مرحله به مرحله پیش بری
"""

import os
import sys
from pathlib import Path


def check_api_key():
    """چک کردن API key"""
    api_key = os.getenv("GPTPROTO_API_KEY")
    if not api_key:
        print("❌ GPTPROTO_API_KEY تنظیم نشده!")
        print("\nدستور:")
        print('  export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"')
        return False

    print(f"✅ API Key: {api_key[:10]}...{api_key[-5:]}")
    return True


def check_voice_file():
    """چک کردن فایل صوتی"""
    project_root = Path(__file__).parent.parent.parent
    voice_file = project_root / "assets" / "voice" / "amir_voice.m4a"

    if voice_file.exists():
        size_mb = voice_file.stat().st_size / (1024 * 1024)
        print(f"✅ فایل صوتی موجود است: {voice_file}")
        print(f"   حجم: {size_mb:.2f} MB")

        # چک کردن اینکه push شده یا نه
        voice_url = os.getenv("VOICE_SAMPLE_URL")
        if voice_url:
            print(f"✅ URL تنظیم شده: {voice_url}")
            return "ready"
        else:
            print("⚠️ فایل محلی موجوده، ولی URL تنظیم نشده")
            print("\nباید فایل رو به GitHub پوش کنی:")
            print("  git add assets/voice/amir_voice.m4a")
            print("  git commit -m 'Add voice sample'")
            print("  git push")
            print("\nبعد URL رو تنظیم کن:")
            print("  export VOICE_SAMPLE_URL='https://raw.githubusercontent.com/...'")
            return "need_push"
    else:
        print(f"❌ فایل صوتی موجود نیست: {voice_file}")
        print("\n📝 راهنما: assets/voice/README.md")
        print("\nمراحل:")
        print("  1. صدات رو ضبط کن (30-60 ثانیه)")
        print("  2. ذخیره کن در: assets/voice/amir_voice.m4a")
        print("  3. دوباره این script رو اجرا کن")
        return "need_record"


def print_status():
    """نمایش وضعیت کلی"""
    print("\n" + "="*60)
    print("📊 وضعیت پروژه Amir AI Influencer")
    print("="*60)

    # Step 1: API Key
    print("\n1️⃣ API Key:")
    api_ok = check_api_key()

    # Step 2: Voice File
    print("\n2️⃣ Voice Sample:")
    voice_status = check_voice_file()

    # نتیجه‌گیری
    print("\n" + "="*60)

    if api_ok and voice_status == "ready":
        print("✅ همه چیز آماده است!")
        print("\n🎬 مرحله بعدی:")
        print("   python backend/scripts/test_voice_clone.py")
        print("\nیا:")
        print("   python backend/scripts/generate_first_reel.py")

    elif api_ok and voice_status == "need_push":
        print("⚠️ فایل صوتی رو باید push کنی")
        print("\n🔧 دستورات:")
        print("   git add assets/voice/amir_voice.m4a")
        print("   git commit -m 'Add Amir voice sample'")
        print("   git push")
        print('   export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/..."')

    elif api_ok and voice_status == "need_record":
        print("⚠️ ابتدا صدات رو ضبط کن")
        print("\n📖 راهنما کامل:")
        print("   cat assets/voice/README.md")

    else:
        print("❌ API Key رو تنظیم کن")

    print("="*60 + "\n")


def main():
    """اجرای workflow helper"""
    print_status()


if __name__ == "__main__":
    main()
