"""
تست MiniMax Voice Clone با صدای واقعی

این script صدای شما رو clone می‌کنه و یک نمونه تولید می‌کنه
"""

import asyncio
import os
from app.services.gptproto.client import GPTProtoClient


async def test_voice_clone():
    """تست voice cloning با صدای واقعی"""

    print("\n" + "="*60)
    print("🎤 MiniMax Voice Clone Test")
    print("="*60)

    # API key
    api_key = os.getenv("GPTPROTO_API_KEY")
    if not api_key:
        print("❌ GPTPROTO_API_KEY not set!")
        return

    client = GPTProtoClient(api_key=api_key)

    try:
        # بررسی فایل محلی
        import sys
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent
        local_voice_file = project_root / "assets" / "voice" / "amir_voice.m4a"

        # گرفتن URL از environment variable یا ساخت از branch
        VOICE_SAMPLE_URL = os.getenv("VOICE_SAMPLE_URL")

        if not VOICE_SAMPLE_URL:
            # تلاش برای ساخت GitHub URL از branch فعلی
            if local_voice_file.exists():
                print(f"\n✅ فایل صوتی محلی پیدا شد: {local_voice_file}")
                print("\n⚠️ برای استفاده از MiniMax، باید فایل رو به GitHub پوش کنی:")
                print("   git add assets/voice/amir_voice.m4a")
                print("   git commit -m 'Add Amir voice sample'")
                print("   git push")
                print("\nسپس یکی از این URLها رو استفاده کن:")
                print("   export VOICE_SAMPLE_URL='https://tmpfiles.org/dl/12674832/amir_voice_sample.m4a'")
                print("   یا:")
                print("   export VOICE_SAMPLE_URL='https://tmpfiles.org/dl/12674832/amir_voice_sample.m4a'")
                return None
            else:
                print(f"\n❌ فایل صوتی پیدا نشد: {local_voice_file}")
                print("\n📝 مراحل ضبط صدا:")
                print("   1. فایل assets/voice/README.md رو بخون")
                print("   2. صدات رو ضبط کن (30-60 ثانیه)")
                print("   3. ذخیره کن در: assets/voice/amir_voice.m4a")
                print("   4. به GitHub پوش کن")
                print("   5. دوباره این script رو اجرا کن")
                return None

        # متن تست
        test_text = """سلام! من امیرم.
امروز می‌خوام iPhone 16 Pro Max رو باهاتون بررسی کنم.
این گوشی یکی از بهترین پرچم‌داران امسال است."""

        print(f"\n✅ Voice Sample URL:")
        print(f"   {VOICE_SAMPLE_URL}")

        print(f"\n📝 Test Text:")
        print(f"   {test_text}")

        print("\n⏳ Step 1: Submitting voice clone request...")

        # درخواست voice clone
        task_id = await client.voice_clone(
            text=test_text,
            audio_url=VOICE_SAMPLE_URL,
            custom_voice_id="amir-voice-001",  # یک ID اختصاصی
            accuracy=0.8,  # دقت بالا
            noise_reduction=True,
            volume_normalization=True
        )

        print(f"✅ Task submitted: {task_id}")

        print("\n⏳ Step 2: Waiting for voice generation...")
        print("   (این ممکنه 30-60 ثانیه طول بکشه)")

        # صبر برای نتیجه
        audio_url = await client.wait_for_voice(task_id, max_wait=120)

        print("\n✅ Voice generated successfully!")
        print("="*60)
        print(f"\n🔗 Audio URL:")
        print(f"   {audio_url}")
        print("\n👉 این فایل رو دانلود و گوش کن!")
        print("   آیا صدا شبیه صدای تو است؟")
        print("="*60)

        return audio_url

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 احتمالات:")
        print("   1. URL صدا اشتباه است یا در دسترس نیست")
        print("   2. فرمت فایل پشتیبانی نمی‌شود (باید MP3/M4A/WAV باشد)")
        print("   3. فایل خیلی کوچک یا بزرگ است")
        print("   4. کیفیت صدا پایین است")
        return None

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_voice_clone())
