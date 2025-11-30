"""
Voice Generator Service با MiniMax (GPTProto)

تولید صدای فارسی با voice cloning
"""

import time
from typing import Optional
from loguru import logger
from pathlib import Path

from ..gptproto.client import GPTProtoClient


class VoiceGenerator:
    """سرویس تولید صدای فارسی با MiniMax voice cloning"""

    def __init__(
        self,
        client: GPTProtoClient,
        voice_sample_url: str,
        custom_voice_id: Optional[str] = None
    ):
        """
        Args:
            client: GPTProto client
            voice_sample_url: URL فایل صوتی برای clone کردن
            custom_voice_id: شناسه اختصاصی صدا (اختیاری - اگر None باشه، unique ID تولید می‌شه)
        """
        self.client = client
        self.voice_sample_url = voice_sample_url
        self.custom_voice_id_prefix = custom_voice_id or "amir-voice"

    async def generate_voice(
        self,
        text: str,
        accuracy: float = 0.8,
        noise_reduction: bool = True,
        volume_normalization: bool = True,
        save_path: Optional[str] = None
    ) -> str:
        """
        تولید صدا از متن فارسی

        Args:
            text: متن فارسی
            accuracy: دقت voice clone (0.0-1.0)
            noise_reduction: کاهش نویز
            volume_normalization: نرمال‌سازی صدا
            save_path: مسیر ذخیره (اختیاری)

        Returns:
            URL فایل صوتی تولید شده
        """
        logger.info(f"Generating voice for text: {text[:50]}...")

        # تولید unique voice ID برای جلوگیری از duplicate error
        unique_voice_id = f"{self.custom_voice_id_prefix}-{int(time.time())}"

        # ارسال درخواست voice clone
        task_id = await self.client.voice_clone(
            text=text,
            audio_url=self.voice_sample_url,
            custom_voice_id=unique_voice_id,
            accuracy=accuracy,
            noise_reduction=noise_reduction,
            volume_normalization=volume_normalization
        )

        logger.debug(f"Using voice ID: {unique_voice_id}")

        logger.info(f"Voice task submitted: {task_id}")

        # صبر برای نتیجه
        audio_url = await self.client.wait_for_voice(task_id, max_wait=180)

        logger.info(f"Voice generated: {audio_url}")

        # اختیاری: دانلود و ذخیره local
        if save_path:
            import httpx
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(audio_url)

                Path(save_path).parent.mkdir(parents=True, exist_ok=True)

                with open(save_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Voice saved to: {save_path}")

        return audio_url

    async def generate_reel_voiceover(
        self,
        script: str,
        save_dir: Optional[str] = None
    ) -> dict:
        """
        تولید voiceover برای ریلز

        Args:
            script: اسکریپت کامل ریلز
            save_dir: مسیر ذخیره

        Returns:
            {
                "audio_url": "...",
                "local_path": "..." (اگر save_dir داده شده باشد)
            }
        """
        logger.info("Generating reel voiceover...")

        # تنظیمات بهینه برای ریلز
        save_path = None
        if save_dir:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"{save_dir}/voice_{timestamp}.mp3"

        audio_url = await self.generate_voice(
            text=script,
            accuracy=0.8,  # دقت بالا
            noise_reduction=True,
            volume_normalization=True,
            save_path=save_path
        )

        result = {
            "audio_url": audio_url
        }

        if save_path:
            result["local_path"] = save_path

        return result
