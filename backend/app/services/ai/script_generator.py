"""
Script Generator Service

تولید اسکریپت فارسی برای ریلز های امیر
"""

from typing import List, Dict, Optional
from loguru import logger

from ..gptproto.client import GPTProtoClient


class ScriptGenerator:
    """سرویس تولید اسکریپت فارسی"""

    def __init__(self, client: GPTProtoClient, model: str = "claude-sonnet-4-5-20250929"):
        self.client = client
        self.model = model

    async def generate_reel_script(
        self,
        product_name: str,
        key_features: List[str],
        duration: int = 30,
        tone: str = "premium",
        format_type: str = "review"
    ) -> Dict[str, any]:
        """
        تولید اسکریپت برای ریلز

        Args:
            product_name: نام محصول (مثل "iPhone 16 Pro Max")
            key_features: لیست ویژگی‌های کلیدی
            duration: مدت ریلز (ثانیه)
            tone: لحن (premium, casual, excited, professional)
            format_type: نوع (review, unboxing, comparison, tutorial)

        Returns:
            {
                "script": "اسکریپت کامل...",
                "hook": "جمله اول (3 ثانیه)",
                "body": "بدنه اصلی",
                "cta": "Call to action",
                "estimated_duration": 32,
                "word_count": 85
            }
        """
        features_text = "\n".join([f"- {f}" for f in key_features])

        # Persona + Instructions
        prompt = f"""شما "امیر" هستید - یک اینفلوئنسر تکنولوژی 28 ساله در تهران.

ویژگی‌های شما:
- سبک: حرفه‌ای، مدرن، کمی طنز، هرگز خشن یا سیاسی
- زبان: فارسی طبیعی با اصطلاحات تهران
- تخصص: موبایل، آیفون، لوازم جانبی، گجت‌های مصرفی
- لحن: {tone}

محصول: {product_name}
ویژگی‌های کلیدی:
{features_text}

نوع ریلز: {format_type}
مدت زمان: {duration} ثانیه

لطفاً یک اسکریپت برای ریلز اینستاگرام بنویسید که شامل:

1. **Hook (3 ثانیه اول)**: جمله جذاب برای توقف اسکرول
2. **Body ({duration-6} ثانیه)**: توضیح ویژگی‌ها، نقاط قوت/ضعف
3. **CTA (3 ثانیه آخر)**: دعوت به عمل

قوانین:
- زبان فارسی طبیعی و روان
- جملات کوتاه (مناسب برای ریلز)
- 2-3 ایموجی حداکثر
- بدون محتوای سیاسی یا حساس
- اگر sponsored است، #تبلیغاتی اضافه کن

فرمت خروجی:
```
HOOK:
[جمله اول جذاب]

BODY:
[متن اصلی با نقاط مهم]

CTA:
[دعوت به عمل]

HASHTAGS:
#تکنولوژی #موبایل ...
```
"""

        logger.info(f"Generating {format_type} script for {product_name}")

        # فراخوانی API
        result = await self.client.chat_completion(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "شما یک نویسنده محتوای حرفه‌ای برای اینفلوئنسر تکنولوژی هستید. همیشه فارسی طبیعی و جذاب می‌نویسید."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,  # کمی خلاق‌تر
            max_tokens=1024
        )

        # استخراج متن
        content = result["choices"][0]["message"]["content"]

        # پارس کردن خروجی
        script_parts = self._parse_script(content)

        # برآورد مدت زمان (فارسی: ~2.5 کلمه در ثانیه)
        word_count = len(script_parts["script"].split())
        estimated_duration = int(word_count / 2.5)

        return {
            "script": script_parts["script"],
            "hook": script_parts["hook"],
            "body": script_parts["body"],
            "cta": script_parts["cta"],
            "hashtags": script_parts["hashtags"],
            "estimated_duration": estimated_duration,
            "word_count": word_count,
            "model": self.model,
            "product": product_name
        }

    async def generate_caption(
        self,
        product_name: str,
        key_features: List[str],
        tone: str = "premium",
        max_length: int = 150,
        is_sponsored: bool = False,
        variants: int = 3
    ) -> List[str]:
        """
        تولید caption برای پست اینستاگرام

        Args:
            product_name: نام محصول
            key_features: ویژگی‌های کلیدی
            tone: لحن
            max_length: حداکثر طول (کاراکتر)
            is_sponsored: آیا تبلیغاتی است؟
            variants: تعداد variantها

        Returns:
            لیست captionها
        """
        features_text = ", ".join(key_features)

        prompt = f"""شما "امیر" هستید - اینفلوئنسر تکنولوژی 28 ساله تهران.

محصول: {product_name}
ویژگی‌ها: {features_text}
لحن: {tone}

{variants} عدد caption فارسی برای پست اینستاگرام بنویسید:

قوانین:
- حداکثر {max_length} کاراکتر
- 1 ایموجی حداکثر
- جمله کوتاه و جذاب
- CTA: "لینک در بیو"
{"- برچسب: #تبلیغاتی #AIgenerated" if is_sponsored else ""}

فرمت:
1. [caption اول]

2. [caption دوم]

3. [caption سوم]
"""

        result = await self.client.chat_completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,  # خلاق
            max_tokens=512
        )

        content = result["choices"][0]["message"]["content"]

        # پارس کردن captions
        captions = self._parse_captions(content, variants)

        logger.info(f"Generated {len(captions)} captions for {product_name}")

        return captions

    async def generate_comment_response(
        self,
        comment_text: str,
        context: Optional[str] = None
    ) -> str:
        """
        تولید پاسخ به کامنت

        Args:
            comment_text: متن کامنت
            context: context اضافی (مثلاً محصول مورد نظر)

        Returns:
            پاسخ مناسب
        """
        prompt = f"""شما "امیر" هستید - اینفلوئنسر تکنولوژی.

کامنت کاربر: "{comment_text}"
{"Context: " + context if context else ""}

یک پاسخ کوتاه، دوستانه و حرفه‌ای بنویسید:
- حداکثر 50 کلمه
- لحن friendly و helpful
- فارسی طبیعی
"""

        result = await self.client.chat_completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=256
        )

        response = result["choices"][0]["message"]["content"].strip()

        return response

    def _parse_script(self, content: str) -> Dict[str, str]:
        """پارس کردن script از خروجی LLM"""
        parts = {
            "hook": "",
            "body": "",
            "cta": "",
            "hashtags": "",
            "script": content
        }

        # استخراج بخش‌ها
        if "HOOK:" in content:
            hook_start = content.find("HOOK:") + 5
            hook_end = content.find("BODY:", hook_start)
            parts["hook"] = content[hook_start:hook_end].strip()

        if "BODY:" in content:
            body_start = content.find("BODY:") + 5
            body_end = content.find("CTA:", body_start)
            parts["body"] = content[body_start:body_end].strip()

        if "CTA:" in content:
            cta_start = content.find("CTA:") + 4
            cta_end = content.find("HASHTAGS:", cta_start) if "HASHTAGS:" in content else len(content)
            parts["cta"] = content[cta_start:cta_end].strip()

        if "HASHTAGS:" in content:
            hashtags_start = content.find("HASHTAGS:") + 9
            parts["hashtags"] = content[hashtags_start:].strip()

        return parts

    def _parse_captions(self, content: str, expected: int) -> List[str]:
        """پارس کردن captions از خروجی"""
        captions = []

        # Split by numbers (1. 2. 3.)
        lines = content.split("\n")
        current_caption = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # شروع caption جدید
            if line.startswith(tuple([f"{i}." for i in range(1, expected + 2)])):
                if current_caption:
                    captions.append(current_caption.strip())
                # حذف شماره
                current_caption = line.split(".", 1)[1].strip() if "." in line else line
            else:
                current_caption += " " + line

        # اضافه کردن آخرین caption
        if current_caption:
            captions.append(current_caption.strip())

        return captions[:expected]
