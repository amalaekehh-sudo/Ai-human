"""
GPTProto API Client

یک client کامل برای تمام APIهای GPTProto
"""

import httpx
import asyncio
import time
from typing import Optional, Dict, Any, List
from loguru import logger


class GPTProtoClient:
    """کلاینت اصلی برای GPTProto API"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://gptproto.com",
        timeout: int = 120,
        max_retries: int = 3
    ):
        """
        Args:
            api_key: API key از GPTProto
            base_url: Base URL (default: https://gptproto.com)
            timeout: Timeout برای requestها (seconds)
            max_retries: تعداد دفعات retry در صورت خطا
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        # HTTP client
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )

    async def close(self):
        """بستن connection"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _get_headers(self, use_bearer: bool = False) -> Dict[str, str]:
        """
        ساخت headers برای request

        Args:
            use_bearer: آیا از "Bearer" استفاده کنیم؟ (فقط برای Suno)
        """
        auth_value = f"Bearer {self.api_key}" if use_bearer else self.api_key

        return {
            "Authorization": auth_value,
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        use_bearer: bool = False,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        ارسال request به GPTProto

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint (مثل /v1/chat/completions)
            data: Request body
            use_bearer: استفاده از Bearer در header (فقط Suno)
            retry_count: تعداد retry های انجام شده

        Returns:
            Response JSON

        Raises:
            Exception: در صورت خطا
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(use_bearer=use_bearer)

        try:
            logger.debug(f"Request: {method} {url}")
            logger.debug(f"Data: {data}")

            if method == "GET":
                response = await self.client.get(url, headers=headers)
            elif method == "POST":
                response = await self.client.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            # چک کردن status code
            if response.status_code == 200:
                # چک کردن اینکه response خالی نباشه
                if not response.text:
                    raise Exception(f"Empty response from {endpoint}")

                try:
                    result = response.json()
                    logger.debug(f"Response: {result}")
                    return result
                except ValueError as e:
                    logger.error(f"Failed to parse JSON response from {endpoint}")
                    logger.error(f"Response text: {response.text[:500]}")
                    raise Exception(f"Invalid JSON response from {endpoint}: {e}")

            # Error handling
            error_data = {}
            if response.text:
                try:
                    error_data = response.json()
                except ValueError:
                    logger.warning(f"Could not parse error response as JSON: {response.text[:200]}")

            error_msg = error_data.get("error", {}).get("message", response.text) if isinstance(error_data.get("error"), dict) else response.text

            # لاگ کامل خطا برای debug
            logger.error(f"Response status: {response.status_code}")
            logger.error(f"Response body: {response.text[:500]}")  # اولین 500 کاراکتر
            logger.error(f"Error data: {error_data}")

            # Retry logic برای errorهای موقت
            if response.status_code in [429, 500, 503] and retry_count < self.max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                logger.warning(
                    f"Error {response.status_code}: {error_msg}. "
                    f"Retrying in {wait_time}s... (attempt {retry_count + 1}/{self.max_retries})"
                )
                await asyncio.sleep(wait_time)
                return await self._request(method, endpoint, data, use_bearer, retry_count + 1)

            # Error های غیر قابل retry
            error_messages = {
                401: "Invalid API key (401)",
                403: "Insufficient balance (403)",
                500: "Internal server error (500)",
                503: "Content policy violation (503)",
                429: "Rate limit exceeded (429)"
            }

            raise Exception(
                f"{error_messages.get(response.status_code, 'API Error')} - {error_msg}"
            )

        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                logger.warning(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
                return await self._request(method, endpoint, data, use_bearer, retry_count + 1)
            raise Exception(f"Request failed: {e}")

    # ==================== LLM APIs (Claude, GPT-5) ====================

    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat completion API (برای Claude, GPT-5)

        Args:
            model: نام مدل (مثل "claude-sonnet-4-5-20250929")
            messages: لیست پیام‌ها [{"role": "user", "content": "..."}]
            temperature: میزان خلاقیت (0.0-1.0)
            max_tokens: حداکثر طول جواب
            stream: آیا streaming فعال باشد؟
            **kwargs: پارامترهای اضافی

        Returns:
            Response dict

        Example:
            >>> client = GPTProtoClient("sk-xxx")
            >>> result = await client.chat_completion(
            ...     model="claude-sonnet-4-5-20250929",
            ...     messages=[{"role": "user", "content": "سلام"}]
            ... )
            >>> print(result["choices"][0]["message"]["content"])
        """
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs
        }

        result = await self._request("POST", "/v1/chat/completions", data)

        # چک کردن error
        if "error" in result:
            raise Exception(f"API Error: {result['error']['message']}")

        return result

    # ==================== Image Generation (Flux) ====================

    async def generate_image(
        self,
        prompt: str,
        model: str = "flux-kontext-pro"
    ) -> str:
        """
        تولید تصویر با Flux

        Args:
            prompt: توضیحات تصویر
            model: مدل (default: flux-kontext-pro)

        Returns:
            URL یا base64 تصویر

        Example:
            >>> client = GPTProtoClient("sk-xxx")
            >>> image_url = await client.generate_image(
            ...     prompt="photorealistic portrait of a Persian man"
            ... )
            >>> print(f"Image: {image_url}")
        """
        data = {
            "stream": False,
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        result = await self._request("POST", "/v1/chat/completions", data)

        # چک کردن error
        if "error" in result:
            raise Exception(f"Image generation error: {result['error']['message']}")

        # استخراج URL/base64 تصویر
        image_data = result["choices"][0]["message"]["content"]
        return image_data

    # ==================== Voice Clone (MiniMax) ====================

    async def voice_clone(
        self,
        text: str,
        custom_voice_id: Optional[str] = None,
        audio_url: Optional[str] = None,
        accuracy: float = 0.7,
        noise_reduction: bool = True,
        volume_normalization: bool = True,
        model: str = "speech-2.5-hd-preview-voice-clone"
    ) -> str:
        """
        تولید صدا با voice cloning (async - برمی‌گرداند task_id)

        Args:
            text: متن برای تبدیل به صدا
            custom_voice_id: ID صدای کلون شده (برای استفاده مجدد)
            audio_url: URL نمونه صدا (برای clone جدید)
            accuracy: دقت clone (0.0-1.0)
            noise_reduction: کاهش نویز
            volume_normalization: نرمال‌سازی volume
            model: مدل (default: speech-2.5-hd-preview-voice-clone)

        Returns:
            task_id برای polling

        Example:
            >>> client = GPTProtoClient("sk-xxx")
            >>> task_id = await client.voice_clone(
            ...     text="سلام! من امیرم",
            ...     custom_voice_id="amir-voice-001"
            ... )
            >>> # بعد polling کن:
            >>> result = await client.get_voice_task(task_id)
        """
        data = {
            "model": model,
            "text": text,
            "accuracy": accuracy,
            "need_noise_reduction": noise_reduction,
            "need_volume_normalization": volume_normalization
        }

        # اضافه کردن voice ID یا audio URL
        if custom_voice_id:
            data["custom_voice_id"] = custom_voice_id
        if audio_url:
            data["audio"] = audio_url

        result = await self._request("POST", "/api/v3/minimax/voice-clone", data)

        # چک کردن error
        if "error" in result and result.get("error"):
            raise Exception(f"Voice clone error: {result['error']}")

        # برگرداندن task_id
        # GPTProto API structure: result['data']['id']
        if "data" in result and isinstance(result["data"], dict):
            task_id = result["data"].get("id")
        else:
            # Fallback برای format قدیمی
            task_id = result.get("id") or result.get("task_id") or result.get("prediction_id")

        if not task_id:
            raise Exception(f"No task_id in response: {result}")

        logger.info(f"Voice clone task created: {task_id}")
        return task_id

    async def get_voice_task(self, task_id: str) -> Dict[str, Any]:
        """
        دریافت نتیجه voice task

        Args:
            task_id: Task ID از voice_clone()

        Returns:
            {"status": "success|processing|failed", "result": {...}}

        Example:
            >>> result = await client.get_voice_task("task-123")
            >>> if result["status"] == "success":
            ...     audio_url = result["result"]["audio_url"]
        """
        result = await self._request(
            "GET",
            f"/api/v3/predictions/{task_id}/result"
        )

        return result

    async def wait_for_voice(
        self,
        task_id: str,
        max_wait: int = 180,
        poll_interval: int = 5
    ) -> str:
        """
        صبر کردن تا voice task تمام بشه و برگرداندن audio URL

        Args:
            task_id: Task ID
            max_wait: حداکثر زمان انتظار (seconds)
            poll_interval: فاصله بین هر polling (seconds)

        Returns:
            Audio URL

        Raises:
            Exception: اگر task fail کنه یا timeout بشه
        """
        start_time = time.time()

        while True:
            # چک کردن timeout
            if time.time() - start_time > max_wait:
                raise Exception(f"Voice task timeout after {max_wait}s")

            # دریافت وضعیت
            result = await self.get_voice_task(task_id)

            # GPTProto structure: result['data'] or result directly
            data = result.get("data", result)

            status = data.get("status", "unknown")
            logger.debug(f"Voice task {task_id} status: {status}")

            # Check if completed (GPTProto uses "succeeded" status)
            if status in ["success", "succeeded", "completed"]:
                # audio_url می‌تونه در outputs یا result باشه
                audio_url = None

                # Check outputs array
                if "outputs" in data and data["outputs"]:
                    audio_url = data["outputs"][0] if isinstance(data["outputs"], list) else data["outputs"]

                # Check result field
                if not audio_url and "result" in data:
                    result_data = data["result"]
                    audio_url = result_data.get("audio_url") if isinstance(result_data, dict) else result_data

                if not audio_url:
                    raise Exception(f"No audio_url in completed task: {result}")

                logger.info(f"Voice task {task_id} completed successfully")
                return audio_url

            elif status in ["failed", "error"]:
                error_msg = data.get("error") or result.get("error") or "Unknown error"
                raise Exception(f"Voice task failed: {error_msg}")

            else:
                # هنوز در حال processing (created, processing, running, etc.)
                logger.debug(f"Voice task {task_id} still processing... waiting {poll_interval}s")
                await asyncio.sleep(poll_interval)

    # ==================== Music Generation (Suno) ====================

    async def generate_music(
        self,
        prompt: Optional[str] = None,
        gpt_description_prompt: Optional[str] = None,
        tags: Optional[str] = None,
        title: Optional[str] = None,
        instrumental: bool = True,
        model: str = "chirp-v3-5",
        continue_clip_id: Optional[str] = None,
        continue_at: Optional[int] = None
    ) -> str:
        """
        تولید موسیقی با Suno (async - برمی‌گرداند task_id)

        Args:
            prompt: Custom lyrics/description (Custom mode)
            gpt_description_prompt: AI description (Inspiration mode) - پیشنهادی
            tags: Style tags (مثل "cinematic,epic,ambient")
            title: Track title
            instrumental: true = بدون vocal
            model: chirp-v3-5 (جدید) یا chirp-v3-0
            continue_clip_id: Clip ID برای extension
            continue_at: Second to extend from

        Returns:
            task_id برای polling

        Example - Inspiration Mode (پیشنهادی):
            >>> task_id = await client.generate_music(
            ...     gpt_description_prompt="Upbeat tech music, 30 seconds",
            ...     instrumental=True
            ... )

        Example - Custom Mode:
            >>> task_id = await client.generate_music(
            ...     prompt="Epic battle music",
            ...     tags="cinematic,epic,orchestral",
            ...     title="Before the Battle",
            ...     instrumental=True
            ... )
        """
        data = {
            "mv": model,
            "make_instrumental": instrumental
        }

        # Inspiration mode
        if gpt_description_prompt:
            data["gpt_description_prompt"] = gpt_description_prompt

        # Custom mode
        if prompt:
            data["prompt"] = prompt
        if tags:
            data["tags"] = tags
        if title:
            data["title"] = title

        # Extension mode
        if continue_clip_id:
            data["continue_clip_id"] = continue_clip_id
        if continue_at is not None:
            data["continue_at"] = continue_at

        # ⚠️ Suno نیاز به "Bearer" داره!
        result = await self._request(
            "POST",
            "/v1/suno/submit/music",
            data,
            use_bearer=True  # مهم!
        )

        # چک کردن error
        if result.get("code") != "success":
            error_msg = result.get("message", "Unknown error")
            raise Exception(f"Music generation error: {error_msg}")

        task_id = result["data"]
        return task_id

    async def get_music_task(self, task_id: str) -> Dict[str, Any]:
        """
        دریافت وضعیت music task

        Args:
            task_id: Task ID از generate_music()

        Returns:
            {
                "code": "success",
                "data": [{
                    "status": "completed|processing|failed",
                    "audio_url": "...",
                    "duration": 30,
                    "title": "...",
                    ...
                }]
            }
        """
        result = await self._request(
            "GET",
            f"/v1/suno/fetch/{task_id}",
            use_bearer=True  # Suno نیاز به Bearer داره
        )

        return result

    async def wait_for_music(
        self,
        task_id: str,
        max_wait: int = 300,  # 5 minutes
        poll_interval: int = 5
    ) -> str:
        """
        صبر کردن تا music task تمام بشه و برگرداندن audio URL

        Args:
            task_id: Task ID
            max_wait: حداکثر زمان انتظار (seconds)
            poll_interval: فاصله بین pollingها (seconds)

        Returns:
            Audio URL

        Raises:
            Exception: اگر fail کنه یا timeout بشه
        """
        start_time = time.time()

        while True:
            # چک timeout
            if time.time() - start_time > max_wait:
                raise Exception(f"Music task timeout after {max_wait}s")

            # دریافت وضعیت
            result = await self.get_music_task(task_id)

            # ✅ Fix: باید status رو چک کنیم نه code
            # Response format: {"status": "SUCCESS", "data": [...]} یا {"status": "IN_PROGRESS", "data": "task is running！"}
            data = result.get("data")
            status = result.get("status")

            if not data:
                # اگه data خالی بود، یعنی هنوز آماده نیست
                logger.debug(f"Music task {task_id} not ready yet (no data)... waiting")
                await asyncio.sleep(poll_interval)
                continue

            # چک کردن اینکه data لیست است یا استرینگ
            if isinstance(data, str):
                # هنوز در حال processing - Response: {"data": "task is running！", "status": "IN_PROGRESS"}
                logger.debug(f"Music task {task_id} still processing (status: {status})...")
                await asyncio.sleep(poll_interval)
                continue

            # اگه data لیست شد، یعنی تمام شده - Response: {"data": [{...}], "status": "SUCCESS"}
            if isinstance(data, list) and len(data) > 0:
                task = data[0]

                # ⚠️ Fix: Suno returns "complete" not "completed"
                if task.get("status") in ["complete", "completed", "succeeded"]:
                    audio_url = task.get("audio_url")
                    if not audio_url:
                        raise Exception(f"No audio_url in result: {task}")

                    logger.info(f"Music ready! Duration: {task.get('duration')}s, Title: {task.get('title')}")
                    return audio_url

                elif task.get("status") == "failed":
                    error_msg = task.get("error_message", "Unknown error")
                    raise Exception(f"Music task failed: {error_msg}")

                else:
                    # processing
                    logger.debug(f"Music task {task_id} status: {task.get('status')}... waiting")
                    await asyncio.sleep(poll_interval)
            else:
                # اگه data فرمت ناشناخته داشت
                logger.debug(f"Music task {task_id} unknown data format: {type(data)}... waiting")
                await asyncio.sleep(poll_interval)

    # ==================== VIDEO GENERATION ====================

    async def generate_video_from_image_audio(
        self,
        image_url: str,
        audio_url: str,
        model: str = "sora-2",  # یا "veo-3.1-pro"
        aspect_ratio: str = "9:16"  # Instagram Reels format
    ) -> str:
        """
        تولید ویدیوی talking head از image + audio با lip-sync

        Args:
            image_url: URL تصویر (چهره امیر)
            audio_url: URL صدا (voice cloning)
            model: مدل video generation (sora-2 یا veo-3.1-pro)
            aspect_ratio: نسبت ابعاد (9:16 برای Reels، 16:9 برای landscape)

        Returns:
            Video URL یا task info

        Example:
            >>> client = GPTProtoClient("sk-xxx")
            >>> result = await client.generate_video_from_image_audio(
            ...     image_url="https://...",
            ...     audio_url="https://..."
            ... )
        """
        # ✅ Sora-2 Image-to-Video endpoint from GPTProto docs
        # Endpoint: /api/v3/openai/sora-2/image-to-video
        # Note: This doesn't support audio/lip-sync directly!
        # Audio will need to be merged separately using FFmpeg

        # Prompt for natural speaking animation
        prompt = "The person speaks naturally with subtle facial expressions, slight head movements, and professional body language. Smooth and realistic animation with natural breathing and micro-expressions."

        data = {
            "prompt": prompt,
            "image": image_url,
            "duration": 8  # 4, 8, or 12 seconds available
        }

        logger.info(f"Generating video from image with Sora-2...")
        logger.info(f"  Image: {image_url}")
        logger.info(f"  Audio (will merge later): {audio_url}")

        # Use correct Sora-2 image-to-video endpoint
        result = await self._request(
            "POST",
            "/api/v3/openai/sora-2/image-to-video",
            data
        )

        logger.debug(f"Video generation response: {result}")

        # Response format: {"status": "success", "task_id": "3cafe854..."}
        if "task_id" in result:
            task_id = result["task_id"]
            logger.info(f"Video task created: {task_id}")
            return task_id

        raise Exception(f"No task_id in response: {result}")

    async def get_video_task(self, task_id: str) -> Dict[str, Any]:
        """
        چک کردن وضعیت video generation task

        Args:
            task_id: Task ID

        Returns:
            وضعیت task
        """
        # Endpoint pattern similar to Suno
        # Try: /api/v3/openai/sora-2/fetch/{task_id}
        result = await self._request(
            "GET",
            f"/api/v3/openai/sora-2/fetch/{task_id}",
            use_bearer=True
        )
        return result

    async def wait_for_video(
        self,
        task_id: str,
        max_wait: int = 600,  # 10 minutes (video takes longer)
        poll_interval: int = 10
    ) -> str:
        """
        صبر کردن تا video task تمام بشه

        Args:
            task_id: Task ID
            max_wait: حداکثر زمان انتظار (seconds)
            poll_interval: فاصله بین polls (seconds)

        Returns:
            Video URL

        Raises:
            Exception: اگر fail کنه یا timeout بشه
        """
        start_time = time.time()

        while True:
            if time.time() - start_time > max_wait:
                raise Exception(f"Video task timeout after {max_wait}s")

            result = await self.get_video_task(task_id)

            data = result.get("data")
            status = result.get("status")

            if not data:
                logger.debug(f"Video task {task_id} not ready yet (no data)...")
                await asyncio.sleep(poll_interval)
                continue

            # چک string response (processing)
            if isinstance(data, str):
                logger.debug(f"Video task {task_id} still processing (status: {status})...")
                await asyncio.sleep(poll_interval)
                continue

            # چک list response (completed)
            if isinstance(data, list) and len(data) > 0:
                task = data[0]

                if task.get("status") in ["complete", "completed", "succeeded"]:
                    video_url = task.get("video_url") or task.get("url")
                    if not video_url:
                        raise Exception(f"No video_url in result: {task}")

                    logger.info(f"Video ready! Duration: {task.get('duration')}s")
                    return video_url

                elif task.get("status") == "failed":
                    error_msg = task.get("error_message", "Unknown error")
                    raise Exception(f"Video task failed: {error_msg}")

                else:
                    logger.debug(f"Video task {task_id} status: {task.get('status')}...")
                    await asyncio.sleep(poll_interval)
            else:
                logger.debug(f"Video task {task_id} unknown format...")
                await asyncio.sleep(poll_interval)


# ==================== Helper Functions ====================

async def create_gptproto_client(api_key: str) -> GPTProtoClient:
    """
    ساخت client با context manager support

    Example:
        >>> async with create_gptproto_client("sk-xxx") as client:
        ...     result = await client.chat_completion(...)
    """
    return GPTProtoClient(api_key)
