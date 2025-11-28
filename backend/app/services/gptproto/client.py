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
                result = response.json()
                logger.debug(f"Response: {result}")
                return result

            # Error handling
            error_data = response.json() if response.text else {}
            error_msg = error_data.get("error", {}).get("message", response.text)

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
        if "error" in result:
            raise Exception(f"Voice clone error: {result['error']['message']}")

        # برگرداندن task_id
        task_id = result.get("id") or result.get("task_id") or result.get("prediction_id")
        if not task_id:
            raise Exception(f"No task_id in response: {result}")

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

            if result["status"] == "success":
                audio_url = result["result"].get("audio_url")
                if not audio_url:
                    raise Exception(f"No audio_url in result: {result}")
                return audio_url

            elif result["status"] == "failed":
                error_msg = result.get("error") or "Unknown error"
                raise Exception(f"Voice task failed: {error_msg}")

            else:
                # هنوز در حال processing
                logger.debug(f"Voice task {task_id} status: {result['status']}... waiting")
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

            if result.get("code") == "success" and result.get("data"):
                task = result["data"][0]

                if task["status"] == "completed":
                    audio_url = task.get("audio_url")
                    if not audio_url:
                        raise Exception(f"No audio_url in result: {task}")

                    logger.info(f"Music ready! Duration: {task.get('duration')}s, Title: {task.get('title')}")
                    return audio_url

                elif task["status"] == "failed":
                    error_msg = task.get("error_message", "Unknown error")
                    raise Exception(f"Music task failed: {error_msg}")

                else:
                    # processing
                    logger.debug(f"Music task {task_id} status: {task['status']}... waiting")
                    await asyncio.sleep(poll_interval)
            else:
                # اگه data خالی بود، یعنی هنوز آماده نیست
                logger.debug(f"Music task {task_id} not ready yet... waiting")
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
