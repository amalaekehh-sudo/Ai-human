"""
تولید اولین ریلز کامل!

این script همه assets یک ریلز رو تولید می‌کنه:
- Script (فارسی)
- Image (Flux)
- Voice (MiniMax با صدای شما)
- Music (Suno)
"""

import asyncio
import os
import json
import sys
from pathlib import Path

# اضافه کردن backend به Python path
project_root = Path(__file__).parent.parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

from app.services.ai.content_pipeline import ContentPipeline


async def main():
    """تولید اولین ریلز"""

    print("\n" + "🎬"*30)
    print("  تولید اولین ریلز کامل - پروژه امیر")
    print("🎬"*30)

    # ═══════════════════════════════════════════════════════
    # تنظیمات
    # ═══════════════════════════════════════════════════════

    # API Key
    gptproto_key = os.getenv("GPTPROTO_API_KEY")
    if not gptproto_key:
        print("\n❌ خطا: GPTPROTO_API_KEY تنظیم نشده!")
        print("   export GPTPROTO_API_KEY='sk-xxx'")
        return

    # URL صدای شما
    # ⚠️ این رو عوض کن به URL واقعی فایل صوتی که آپلود کردی!
    voice_sample_url = os.getenv(
        "VOICE_SAMPLE_URL",
        "https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/main/assets/voice/amir_voice.m4a"
    )

    print(f"\n✅ API Key: {gptproto_key[:10]}...{gptproto_key[-5:]}")
    print(f"✅ Voice Sample: {voice_sample_url}")

    # ═══════════════════════════════════════════════════════
    # مشخصات محصول
    # ═══════════════════════════════════════════════════════

    product = {
        "name": "iPhone 16 Pro Max",
        "features": [
            "دوربین 48 مگاپیکسل با زوم تتراپریسم",
            "چیپ A18 Pro با هوش مصنوعی",
            "باتری طولانی‌مدت تا 29 ساعت",
            "بدنه تیتانیوم سبک و مقاوم",
            "نمایشگر ProMotion 120Hz"
        ],
        "duration": 30  # ثانیه
    }

    print(f"\n📱 محصول: {product['name']}")
    print(f"   ویژگی‌ها: {len(product['features'])} مورد")
    print(f"   مدت: {product['duration']} ثانیه")

    # ═══════════════════════════════════════════════════════
    # ایجاد Pipeline
    # ═══════════════════════════════════════════════════════

    pipeline = ContentPipeline(
        gptproto_key=gptproto_key,
        voice_sample_url=voice_sample_url,
        voice_id="amir-voice-001"
    )

    # ═══════════════════════════════════════════════════════
    # تولید محتوا
    # ═══════════════════════════════════════════════════════

    output_dir = "reels_output"
    print(f"\n📁 Output: {output_dir}/")

    try:
        result = await pipeline.generate_reel_assets(
            product_name=product["name"],
            key_features=product["features"],
            duration=product["duration"],
            output_dir=output_dir,
            include_music=True  # شامل موسیقی
        )

        # ═══════════════════════════════════════════════════════
        # ذخیره نتایج
        # ═══════════════════════════════════════════════════════

        # ذخیره JSON
        json_path = Path(output_dir) / f"{product['name'].replace(' ', '_')}_assets.json"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Assets saved to: {json_path}")

        # ذخیره script به فایل متنی
        script_path = Path(output_dir) / f"{product['name'].replace(' ', '_')}_script.txt"

        with open(script_path, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write(f"Script: {product['name']}\n")
            f.write("="*60 + "\n\n")

            f.write("HOOK:\n")
            f.write(result["script"]["hook"] + "\n\n")

            f.write("BODY:\n")
            f.write(result["script"]["body"] + "\n\n")

            f.write("CTA:\n")
            f.write(result["script"]["cta"] + "\n\n")

            f.write("HASHTAGS:\n")
            f.write(result["script"]["hashtags"] + "\n")

        print(f"💾 Script saved to: {script_path}")

        # ═══════════════════════════════════════════════════════
        # خلاصه نهایی
        # ═══════════════════════════════════════════════════════

        print("\n" + "="*60)
        print("🎊 اولین ریلز شما آماده شد!")
        print("="*60)

        print(f"\n📝 Script ({result['script']['word_count']} کلمه):")
        print("-"*60)
        print(result["script"]["full_script"])
        print("-"*60)

        print(f"\n🖼️  Image:")
        print(f"   {result['image']['url']}")
        print("   👉 این لینک رو باز کن و تصویر رو ببین")

        print(f"\n🎤 Voice:")
        print(f"   {result['voice']['audio_url']}")
        if "local_path" in result["voice"]:
            print(f"   Local: {result['voice']['local_path']}")
        print("   👉 دانلود کن و گوش بده")

        if "music" in result:
            print(f"\n🎵 Music:")
            print(f"   Title: {result['music']['title']}")
            print(f"   Duration: {result['music']['duration']}s")
            print(f"   {result['music']['url']}")
            print("   👉 دانلود کن و گوش بده")

        print("\n" + "="*60)
        print("📦 Assets:")
        print(f"   - Script: {script_path}")
        print(f"   - JSON: {json_path}")
        if "local_path" in result["voice"]:
            print(f"   - Voice: {result['voice']['local_path']}")
        print("="*60)

        print("\n✅ مرحله بعدی:")
        print("   1. تصویر رو ببین")
        print("   2. صدا رو گوش کن (آیا صدات رو clone کرده؟)")
        print("   3. موسیقی رو گوش کن")
        print("   4. اگه همه چیز خوب بود → ادامه به Video Pipeline")

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await pipeline.close()


if __name__ == "__main__":
    asyncio.run(main())
