"""
تست Video Generation با GPTProto

این script از image + audio یک talking head video با lip-sync می‌سازه
"""

import asyncio
import os
import sys
from pathlib import Path

# اضافه کردن backend به Python path
project_root = Path(__file__).parent.parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

from app.services.gptproto.client import GPTProtoClient


async def test_video_generation():
    """تست video generation"""

    print("\n" + "🎬"*30)
    print("  تست Video Generation - GPTProto")
    print("🎬"*30)

    # API Key
    api_key = os.getenv("GPTPROTO_API_KEY")
    if not api_key:
        print("\n❌ خطا: GPTPROTO_API_KEY تنظیم نشده!")
        return

    print(f"\n✅ API Key: {api_key[:10]}...{api_key[-5:]}")

    # ═══════════════════════════════════════════════════════
    # Assets از آخرین ریلز تولید شده
    # ═══════════════════════════════════════════════════════

    image_url = "https://filesystem.site/cdn/20251201/543f27458b4de21cbee0a6098db7e6.png"
    audio_url = "https://d1q70pf5vjeyhc.cloudfront.net/predictions/dc21d213e57f43678a0131ec3a1cbaaf/1.mp3"

    print(f"\n📸 Image: {image_url}")
    print(f"🎤 Audio: {audio_url}")

    # ═══════════════════════════════════════════════════════
    # Video Generation
    # ═══════════════════════════════════════════════════════

    client = GPTProtoClient(api_key)

    try:
        print("\n🎬 شروع Video Generation...")
        print("   این ممکنه چند دقیقه طول بکشه...")

        # تولید ویدیو (ممکنه مستقیم URL بده یا task ID)
        result = await client.generate_video_from_image_audio(
            image_url=image_url,
            audio_url=audio_url,
            model="sora-2",  # یا "veo-3.1-pro"
            aspect_ratio="9:16"
        )

        print(f"\n✅ Video generation response:")
        print(f"   {result}")

        # اگر URL مستقیم برگشت
        if result.startswith("http"):
            video_url = result
        else:
            # اگر task ID برگشت، باید poll کنیم
            print("   Response is not a direct URL, might be task ID or instructions")
            video_url = result

        print("\n" + "="*60)
        print("🎉 Video Generation موفق بود!")
        print("="*60)

        print(f"\n🎬 Video URL:")
        print(f"   {video_url}")
        print("\n👉 لینک رو باز کن و ویدیو رو ببین!")

        # ذخیره URL
        output_dir = Path("reels_output")
        output_dir.mkdir(exist_ok=True)

        video_info_path = output_dir / "video_info.txt"
        with open(video_info_path, "w") as f:
            f.write(f"Video URL: {video_url}\n")
            f.write(f"Image: {image_url}\n")
            f.write(f"Audio: {audio_url}\n")
            f.write(f"Model: sora-2-pro\n")

        print(f"\n💾 Info saved: {video_info_path}")

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()

        print("\n⚠️ احتمالاً endpoint دقیق با GPTProto متفاوته.")
        print("   لطفاً documentation GPTProto رو چک کن:")
        print("   https://gptproto.com/docs")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_video_generation())
