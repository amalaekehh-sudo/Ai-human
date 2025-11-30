"""
Content Pipeline کامل

Script → Image → Voice → Music
"""

import asyncio
import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from .script_generator import ScriptGenerator
from .voice_generator import VoiceGenerator
from ..gptproto.client import GPTProtoClient


class ContentPipeline:
    """Pipeline کامل تولید محتوا برای ریلز"""

    def __init__(
        self,
        gptproto_key: str,
        voice_sample_url: str,
        voice_id: str = "amir-voice-001"
    ):
        """
        Args:
            gptproto_key: GPTProto API key
            voice_sample_url: URL صدا برای voice cloning
            voice_id: شناسه اختصاصی صدا
        """
        self.gpt_client = GPTProtoClient(api_key=gptproto_key)
        self.script_gen = ScriptGenerator(self.gpt_client)
        self.voice_gen = VoiceGenerator(
            client=self.gpt_client,
            voice_sample_url=voice_sample_url,
            custom_voice_id=voice_id
        )

    async def generate_reel_assets(
        self,
        product_name: str,
        key_features: list,
        duration: int = 30,
        output_dir: str = "output",
        include_music: bool = True
    ) -> Dict[str, Any]:
        """
        تولید همه assets برای یک ریلز

        Args:
            product_name: نام محصول
            key_features: لیست ویژگی‌ها
            duration: مدت ریلز (ثانیه)
            output_dir: مسیر ذخیره
            include_music: آیا موسیقی هم تولید بشه؟

        Returns:
            {
                "product": "iPhone 16 Pro Max",
                "script": {
                    "hook": "...",
                    "body": "...",
                    "cta": "...",
                    "full_script": "...",
                    "word_count": 85,
                    "estimated_duration": 32
                },
                "image": {
                    "url": "https://...",
                    "prompt": "..."
                },
                "voice": {
                    "url": "https://...",
                    "local_path": "output/voice_20231128_123456.mp3"
                },
                "music": {
                    "url": "https://...",
                    "title": "Pulse in Pixels",
                    "duration": 60
                },
                "timestamp": "2023-11-28T12:34:56"
            }
        """
        timestamp = datetime.now()
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        result = {
            "product": product_name,
            "timestamp": timestamp.isoformat()
        }

        logger.info("="*60)
        logger.info(f"🎬 Starting Content Pipeline for: {product_name}")
        logger.info("="*60)

        # ═══════════════════════════════════════════════════════
        # 1️⃣ SCRIPT GENERATION
        # ═══════════════════════════════════════════════════════
        logger.info("\n📝 Step 1/4: Generating script...")

        script_data = await self.script_gen.generate_reel_script(
            product_name=product_name,
            key_features=key_features,
            duration=duration,
            tone="premium",
            format_type="review"
        )

        # ساخت full script
        full_script = f"{script_data['hook']}\n\n{script_data['body']}\n\n{script_data['cta']}"

        result["script"] = {
            "hook": script_data["hook"],
            "body": script_data["body"],
            "cta": script_data["cta"],
            "full_script": full_script,
            "word_count": script_data["word_count"],
            "estimated_duration": script_data["estimated_duration"],
            "hashtags": script_data.get("hashtags", "")
        }

        logger.info(f"✅ Script generated:")
        logger.info(f"   - Words: {script_data['word_count']}")
        logger.info(f"   - Duration: ~{script_data['estimated_duration']}s")

        # ═══════════════════════════════════════════════════════
        # 2️⃣ IMAGE GENERATION
        # ═══════════════════════════════════════════════════════
        logger.info("\n🖼️  Step 2/4: Generating image...")

        image_prompt = f"""photorealistic portrait of a 28-year-old Persian man,
Tehran tech influencer named Amir, modern casual style,
wearing dark jacket, holding {product_name},
warm cinematic lighting, professional studio feel,
4:5 aspect ratio, high detail, sharp focus,
realistic skin texture, background soft blur neutral tones"""

        image_data_raw = await self.gpt_client.generate_image(image_prompt)

        # استخراج URL از markdown
        image_url = self._extract_image_url(image_data_raw)

        result["image"] = {
            "url": image_url,
            "prompt": image_prompt
        }

        logger.info(f"✅ Image generated:")
        logger.info(f"   - URL: {image_url}")

        # ═══════════════════════════════════════════════════════
        # 3️⃣ VOICE GENERATION
        # ═══════════════════════════════════════════════════════
        logger.info("\n🎤 Step 3/4: Generating voice...")

        voice_data = await self.voice_gen.generate_reel_voiceover(
            script=full_script,
            save_dir=str(output_path)
        )

        result["voice"] = voice_data

        logger.info(f"✅ Voice generated:")
        logger.info(f"   - URL: {voice_data['audio_url']}")
        if "local_path" in voice_data:
            logger.info(f"   - Local: {voice_data['local_path']}")

        # ═══════════════════════════════════════════════════════
        # 4️⃣ MUSIC GENERATION (اختیاری)
        # ═══════════════════════════════════════════════════════
        if include_music:
            logger.info("\n🎵 Step 4/4: Generating music...")

            music_prompt = f"Upbeat modern tech background music for {product_name} review, electronic, energetic, Instagram reel style, no vocals"

            music_task_id = await self.gpt_client.generate_music(
                gpt_description_prompt=music_prompt,
                instrumental=True,
                model="chirp-v3-5"
            )

            logger.info(f"   ⏳ Music task: {music_task_id}, waiting...")

            music_url = await self.gpt_client.wait_for_music(
                music_task_id,
                max_wait=180
            )

            # دریافت metadata موسیقی
            music_result = await self.gpt_client.get_music_task(music_task_id)

            if music_result.get("data") and isinstance(music_result["data"], list):
                music_info = music_result["data"][0]

                result["music"] = {
                    "url": music_url,
                    "title": music_info.get("title", "Unknown"),
                    "duration": music_info.get("duration", 0),
                    "tags": music_info.get("tags", "")
                }

                logger.info(f"✅ Music generated:")
                logger.info(f"   - Title: {result['music']['title']}")
                logger.info(f"   - Duration: {result['music']['duration']}s")
                logger.info(f"   - URL: {music_url}")
            else:
                result["music"] = {
                    "url": music_url
                }
        else:
            logger.info("\n⏭️  Step 4/4: Skipping music generation")

        # ═══════════════════════════════════════════════════════
        # SUMMARY
        # ═══════════════════════════════════════════════════════
        logger.info("\n" + "="*60)
        logger.info("🎉 Content Pipeline Complete!")
        logger.info("="*60)
        logger.info(f"\nProduct: {product_name}")
        logger.info(f"\n📝 Script:")
        logger.info(f"   {result['script']['full_script'][:100]}...")
        logger.info(f"\n🖼️  Image: {result['image']['url']}")
        logger.info(f"\n🎤 Voice: {result['voice']['audio_url']}")
        if include_music and "music" in result:
            logger.info(f"\n🎵 Music: {result['music']['url']}")
        logger.info("\n" + "="*60)

        return result

    def _extract_image_url(self, image_data: str) -> str:
        """استخراج URL تصویر از markdown"""
        # جستجو برای URL با پسوند .png یا .jpg
        url_match = re.search(r'https://[^\s\)]+\.(png|jpg|jpeg)', image_data)

        if url_match:
            return url_match.group(0)

        # اگر پیدا نشد، کل data رو برگردون
        return image_data

    async def close(self):
        """بستن connections"""
        await self.gpt_client.close()
