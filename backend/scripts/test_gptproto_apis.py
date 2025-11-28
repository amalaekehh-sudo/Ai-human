"""
Test Script برای GPTProto APIs

این script همه APIهای GPTProto رو تست می‌کنه
"""

import asyncio
import os
import sys
from pathlib import Path

# اضافه کردن path پروژه
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.gptproto.client import GPTProtoClient
from app.services.ai.script_generator import ScriptGenerator


async def test_claude_persian():
    """تست Claude برای تولید متن فارسی"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Claude - Persian Script Generation")
    print("="*60)

    client = GPTProtoClient(api_key=os.getenv("GPTPROTO_API_KEY"))

    try:
        # تست ساده
        result = await client.chat_completion(
            model="claude-sonnet-4-5-20250929",
            messages=[
                {
                    "role": "user",
                    "content": "سلام! یک caption فارسی 50 کلمه‌ای برای پست iPhone 16 Pro Max بنویس. لحن حرفه‌ای و مدرن."
                }
            ],
            temperature=0.7,
            max_tokens=512
        )

        caption = result["choices"][0]["message"]["content"]

        print("\n✅ Caption تولید شد:")
        print("-" * 60)
        print(caption)
        print("-" * 60)

        # بررسی کیفیت
        print("\n📊 بررسی کیفیت:")
        print(f"   - طول: {len(caption)} کاراکتر")
        print(f"   - تعداد کلمات: {len(caption.split())} کلمه")
        print(f"   - فارسی: {'✅' if any(ord(c) > 1000 for c in caption) else '❌'}")
        print(f"   - طبیعی: {'✅ (باید خودت بررسی کنی!)' }")

        # Token usage
        usage = result.get("usage", {})
        if usage:
            print(f"\n💰 استفاده از Token:")
            print(f"   - Input: {usage.get('prompt_tokens', 0)} tokens")
            print(f"   - Output: {usage.get('completion_tokens', 0)} tokens")
            print(f"   - Total: {usage.get('total_tokens', 0)} tokens")

        return True

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        return False

    finally:
        await client.close()


async def test_flux_image():
    """تست Flux برای تولید تصویر"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Flux - Portrait Image Generation")
    print("="*60)

    client = GPTProtoClient(api_key=os.getenv("GPTPROTO_API_KEY"))

    try:
        prompt = """photorealistic portrait of a 28-year-old Persian man,
Tehran tech influencer, modern casual style, wearing dark jacket,
warm cinematic lighting, holding iPhone 16 Pro,
professional studio feel, 4:5 aspect ratio,
high detail, sharp focus, realistic skin texture,
background: soft blur, neutral tones"""

        print(f"\n📝 Prompt:")
        print(f"   {prompt[:100]}...")

        print("\n⏳ در حال تولید تصویر... (ممکنه 10-30 ثانیه طول بکشه)")

        image_data = await client.generate_image(prompt)

        print("\n✅ تصویر تولید شد!")
        print("-" * 60)
        print(f"Output: {image_data[:200]}...")
        print("-" * 60)

        # بررسی فرمت
        if image_data.startswith("http"):
            print("\n📊 فرمت: URL")
            print(f"   🔗 {image_data}")
            print("\n   👉 این URL رو باز کن و تصویر رو ببین!")
        elif image_data.startswith("data:image"):
            print("\n📊 فرمت: Base64 Data URI")
            print(f"   - طول: {len(image_data)} کاراکتر")
            print("   👉 می‌تونی توی HTML یا image viewer باز کنی")
        else:
            print(f"\n⚠️ فرمت نامشخص: {image_data[:100]}")

        return True

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        return False

    finally:
        await client.close()


async def test_minimax_voice():
    """تست MiniMax برای تولید صدای فارسی"""
    print("\n" + "="*60)
    print("🧪 TEST 3: MiniMax - Persian Text-to-Speech")
    print("="*60)

    client = GPTProtoClient(api_key=os.getenv("GPTPROTO_API_KEY"))

    try:
        persian_text = """سلام! من امیرم. امروز می‌خوام iPhone 16 Pro Max رو باهاتون بررسی کنم.
این گوشی یکی از بهترین پرچم‌داران امسال است و قابلیت‌های جالبی داره."""

        print(f"\n📝 متن فارسی:")
        print(f"   {persian_text}")
        print(f"\n   - طول: {len(persian_text)} کاراکتر")
        print(f"   - کلمات: {len(persian_text.split())} کلمه")

        print("\n⏳ در حال ارسال درخواست...")

        # ارسال درخواست (بدون voice clone - فقط TTS)
        task_id = await client.voice_clone(
            text=persian_text,
            accuracy=0.7,
            noise_reduction=True,
            volume_normalization=True
        )

        print(f"\n✅ Task ثبت شد: {task_id}")
        print("⏳ در حال polling برای نتیجه... (ممکنه 30-60 ثانیه طول بکشه)")

        # صبر برای نتیجه
        audio_url = await client.wait_for_voice(task_id, max_wait=120)

        print("\n✅ صدا تولید شد!")
        print("-" * 60)
        print(f"🔗 Audio URL: {audio_url}")
        print("-" * 60)

        print("\n📊 بررسی کیفیت:")
        print("   👉 این فایل صوتی رو دانلود و گوش کن!")
        print("   ⚠️ چک کن:")
        print("      - آیا فارسی رو درست تلفظ می‌کنه؟")
        print("      - لهجه طبیعی است یا robotic?")
        print("      - کیفیت صدا HD است؟")

        return True

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        print("\n💡 نکات:")
        print("   - شاید MiniMax فارسی support نداشته باشه")
        print("   - یا نیاز به voice clone ID باشه")
        print("   - یا API format تغییر کرده باشه")
        return False

    finally:
        await client.close()


async def test_suno_music():
    """تست Suno برای تولید موسیقی"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Suno - Music Generation")
    print("="*60)

    client = GPTProtoClient(api_key=os.getenv("GPTPROTO_API_KEY"))

    try:
        description = "Upbeat modern tech background music, electronic, energetic, 30 seconds, Instagram reel style, no vocals"

        print(f"\n📝 توضیحات:")
        print(f"   {description}")

        print("\n⏳ در حال ارسال درخواست...")

        task_id = await client.generate_music(
            gpt_description_prompt=description,
            instrumental=True,
            model="chirp-v3-5"
        )

        print(f"\n✅ Task ثبت شد: {task_id}")
        print("⏳ در حال polling... (ممکنه 1-2 دقیقه طول بکشه)")

        # صبر برای نتیجه
        audio_url = await client.wait_for_music(task_id, max_wait=180)

        print("\n✅ موسیقی تولید شد!")
        print("-" * 60)
        print(f"🔗 Audio URL: {audio_url}")
        print("-" * 60)

        print("\n📊 بررسی کیفیت:")
        print("   👉 این فایل رو دانلود و گوش کن!")
        print("   ⚠️ چک کن:")
        print("      - آیا مناسب ریلز تکنولوژی است؟")
        print("      - مدت زمان حدود 30 ثانیه است؟")
        print("      - Instrumental است (بدون vocal)?")
        print("      - کیفیت موسیقی خوب است؟")

        return True

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        return False

    finally:
        await client.close()


async def test_script_generator():
    """تست ScriptGenerator service"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Script Generator Service")
    print("="*60)

    client = GPTProtoClient(api_key=os.getenv("GPTPROTO_API_KEY"))
    script_gen = ScriptGenerator(client)

    try:
        print("\n⏳ در حال تولید اسکریپت ریلز...")

        result = await script_gen.generate_reel_script(
            product_name="iPhone 16 Pro Max",
            key_features=[
                "دوربین 48 مگاپیکسل",
                "چیپ A18 Pro",
                "باتری طولانی‌مدت",
                "تیتانیوم design"
            ],
            duration=30,
            tone="premium",
            format_type="review"
        )

        print("\n✅ اسکریپت تولید شد!")
        print("=" * 60)

        print(f"\n📝 HOOK ({len(result['hook'])} کاراکتر):")
        print("-" * 60)
        print(result["hook"])

        print(f"\n📝 BODY ({len(result['body'])} کاراکتر):")
        print("-" * 60)
        print(result["body"])

        print(f"\n📝 CTA ({len(result['cta'])} کاراکتر):")
        print("-" * 60)
        print(result["cta"])

        print(f"\n🏷️ HASHTAGS:")
        print("-" * 60)
        print(result["hashtags"])

        print(f"\n📊 آمار:")
        print(f"   - کلمات: {result['word_count']}")
        print(f"   - مدت تخمینی: {result['estimated_duration']} ثانیه")
        print(f"   - Model: {result['model']}")

        return True

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        return False

    finally:
        await client.close()


async def main():
    """اجرای همه تست‌ها"""
    print("\n" + "🚀" * 30)
    print("  GPTProto API Test Suite")
    print("  پروژه: Amir AI Influencer")
    print("🚀" * 30)

    # چک کردن API key
    api_key = os.getenv("GPTPROTO_API_KEY")
    if not api_key:
        print("\n❌ خطا: GPTPROTO_API_KEY تنظیم نشده!")
        print("\nراه‌حل:")
        print("  export GPTPROTO_API_KEY='sk-your-key-here'")
        return

    print(f"\n✅ API Key: {api_key[:10]}...{api_key[-5:]}")

    # اجرای تست‌ها
    results = {}

    # تست 1: Claude
    results["Claude"] = await test_claude_persian()
    await asyncio.sleep(2)

    # تست 2: Flux
    results["Flux"] = await test_flux_image()
    await asyncio.sleep(2)

    # تست 3: MiniMax (مهم‌ترین!)
    results["MiniMax"] = await test_minimax_voice()
    await asyncio.sleep(2)

    # تست 4: Suno
    results["Suno"] = await test_suno_music()
    await asyncio.sleep(2)

    # تست 5: Script Generator
    results["Script Generator"] = await test_script_generator()

    # خلاصه نتایج
    print("\n" + "="*60)
    print("📊 خلاصه نتایج تست‌ها")
    print("="*60)

    for service, success in results.items():
        status = "✅ موفق" if success else "❌ ناموفق"
        print(f"  {service:<20} {status}")

    total_passed = sum(1 for v in results.values() if v)
    total = len(results)

    print("\n" + "-"*60)
    print(f"  جمع: {total_passed}/{total} تست موفق")
    print("-"*60)

    # نتیجه‌گیری
    if total_passed == total:
        print("\n🎉 عالی! همه تست‌ها موفق بودند!")
        print("\n✅ آماده برای ساخت MVP:")
        print("   1. همه APIها کار می‌کنند")
        print("   2. کیفیت Persian خوب است")
        print("   3. می‌تونیم شروع به ساخت pipeline کنیم")

    elif total_passed >= total * 0.75:
        print("\n🟡 خوب! اکثر تست‌ها موفق بودند")
        print("\n⚠️ بررسی کن:")
        failed = [s for s, r in results.items() if not r]
        for service in failed:
            print(f"   - {service}: چرا fail کرد؟")

    else:
        print("\n🔴 مشکل! تعداد زیادی تست fail شدند")
        print("\n❗ اقدامات لازم:")
        print("   1. API key رو چک کن")
        print("   2. Credit account رو چک کن")
        print("   3. مستندات GPTProto رو دوباره بررسی کن")


if __name__ == "__main__":
    # اجرا
    asyncio.run(main())
