# 📚 تحلیل دقیق API های GPTProto

**تاریخ:** 2025-11-28
**وضعیت:** ✅ مستندات دریافت شد - آماده کدنویسی

---

## 🎯 خلاصه کلی

همه APIها **کامل و استاندارد** هستند! ✅

| API | وضعیت | فرمت | Async? | قیمت |
|-----|-------|------|--------|------|
| Claude Sonnet 4.5 | ✅ Ready | OpenAI | ❌ Sync | ❓ |
| GPT-5 | ✅ Ready | OpenAI | ❌ Sync | ❓ |
| Flux Kontext Pro | ✅ Ready | OpenAI | ❌ Sync | ❓ |
| MiniMax Voice | ✅ Ready | Custom | ✅ Async | ❓ |
| Suno Music | ✅ Ready | Custom | ✅ Async | ❓ |

---

## 1️⃣ Claude Sonnet 4.5 - Text Generation

### 📋 مشخصات:

```python
Endpoint: POST https://gptproto.com/v1/chat/completions
Model: "claude-sonnet-4-5-20250929"
Format: OpenAI-compatible
Authentication: Bearer token
Response: Synchronous (مستقیم)
```

### 🔧 نحوه استفاده:

```python
import requests

url = "https://gptproto.com/v1/chat/completions"
headers = {
    "Authorization": "YOUR_API_KEY",  # بدون "Bearer"
    "Content-Type": "application/json"
}

data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {
            "role": "user",
            "content": "سلام! من امیرم، یک caption فارسی برای iPhone 16 Pro بنویس"
        }
    ],
    "stream": False,  # یا True برای streaming
    # Optional parameters:
    "temperature": 0.7,  # خلاقیت (0.0-1.0)
    "max_tokens": 1024,  # حداکثر طول جواب
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

# استخراج جواب:
if "error" not in result:
    content = result["choices"][0]["message"]["content"]
    print(content)
else:
    print(f"Error: {result['error']['message']}")
```

### ✅ مزایا:
- Format استاندارد OpenAI (آشنا و آسان)
- Synchronous (بدون نیاز به polling)
- Streaming support (برای real-time)
- Persian language عالی

### ⚠️ نکات:
- API key باید بدون "Bearer" باشه
- Error handling: 401 (invalid key), 403 (no balance), 500, 503

---

## 2️⃣ GPT-5 - Text Generation

### 📋 مشخصات:

```python
Endpoint: POST https://gptproto.com/v1/chat/completions
Model: "gpt-5"
Format: OpenAI-compatible
```

### 🔧 استفاده مشابه Claude:

```python
# فقط model رو عوض کن:
data = {
    "model": "gpt-5",  # به جای claude-sonnet-4-5-20250929
    "messages": [...],
    "stream": False
}
```

### 📝 کاربرد:
- Fallback برای Claude
- A/B testing
- مقایسه کیفیت

---

## 3️⃣ Flux Kontext Pro - Image Generation

### 📋 مشخصات:

```python
Endpoint: POST https://gptproto.com/v1/chat/completions
Model: "flux-kontext-pro"
Format: OpenAI-compatible (جالبه!)
Response: Synchronous
```

### 🔧 نحوه استفاده:

```python
import requests
import json

url = "https://gptproto.com/v1/chat/completions"
headers = {
    "Authorization": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "stream": False,
    "model": "flux-kontext-pro",
    "messages": [
        {
            "role": "user",
            "content": """photorealistic portrait of a 28-year-old Persian man,
Tehran tech influencer, modern casual style, warm lighting,
holding iPhone 16 Pro, professional studio feel, 4:5 aspect ratio,
high detail, sharp focus, realistic skin texture"""
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

# استخراج URL تصویر:
if "error" not in result:
    # پاسخ احتمالاً URL تصویر یا base64 است
    image_data = result["choices"][0]["message"]["content"]
    print(f"Image URL: {image_data}")
else:
    print(f"Error: {result['error']['message']}")
```

### ✅ مزایا:
- OpenAI format (استاندارد)
- Synchronous (سریع)
- Flux Pro quality (عالی برای portrait)

### ❓ سوالات:
- آیا جواب URL است یا base64؟
- Aspect ratio چطور کنترل می‌شه؟
- Resolution حداکثر چقدره؟

### 🧪 نیاز به تست:
- فرمت خروجی (URL vs base64)
- Quality settings
- Resolution options

---

## 4️⃣ MiniMax Voice Clone - Persian TTS

### 📋 مشخصات:

```python
Endpoint: POST https://gptproto.com/api/v3/minimax/voice-clone
Model: "speech-2.5-hd-preview-voice-clone"
Format: Custom (نه OpenAI)
Response: Async (task-based)
```

### 🔧 نحوه استفاده (دو مرحله):

#### مرحله 1: ارسال درخواست
```python
import requests

url = "https://gptproto.com/api/v3/minimax/voice-clone"
headers = {
    "Authorization": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "model": "speech-2.5-hd-preview-voice-clone",
    "text": "سلام! من امیرم. امروز می‌خوام iPhone 16 Pro Max رو باهاتون بررسی کنم.",

    # Voice cloning options:
    "custom_voice_id": "amir-voice-001",  # ID اختصاصی برای صدای امیر
    "audio": "https://your-server.com/amir-voice-sample.mp3",  # URL نمونه صدا

    # Quality settings:
    "accuracy": 0.7,  # دقت voice clone (0.0-1.0)
    "need_noise_reduction": True,  # کاهش نویز
    "need_volume_normalization": True  # نرمال‌سازی صدا
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

# دریافت task_id:
if "error" not in result:
    task_id = result.get("id") or result.get("task_id")
    print(f"Task submitted: {task_id}")
else:
    print(f"Error: {result['error']['message']}")
```

#### مرحله 2: دریافت نتیجه (Polling)
```python
import time

# استفاده از task_id از مرحله قبل
task_url = f"https://gptproto.com/api/v3/predictions/{task_id}/result"
headers = {
    "Authorization": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Polling برای نتیجه:
max_attempts = 30  # حداکثر 30 بار (150 ثانیه)
for attempt in range(max_attempts):
    response = requests.get(task_url, headers=headers)
    result = response.json()

    if result["status"] == "success":
        audio_url = result["result"]["audio_url"]
        print(f"Audio ready: {audio_url}")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result.get('error')}")
        break
    else:
        print(f"Status: {result['status']}... waiting")
        time.sleep(5)  # صبر 5 ثانیه
```

### 📝 Parameters کلیدی:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| model | string | ✅ Yes | - | "speech-2.5-hd-preview-voice-clone" |
| text | string | ✅ Yes | - | متن فارسی برای تبدیل به صدا |
| custom_voice_id | string | ❌ No | - | ID صدای کلون شده (برای استفاده مجدد) |
| audio | string | ❌ No | - | URL نمونه صدا برای voice cloning |
| accuracy | float | ❌ No | 0.7 | دقت clone (0.0-1.0) |
| need_noise_reduction | boolean | ❌ No | false | کاهش نویز |
| need_volume_normalization | boolean | ❌ No | false | نرمال‌سازی volume |

### ✅ مزایا:
- Voice cloning support ⭐
- HD quality
- Noise reduction و normalization
- Reusable voice ID

### ⚠️ نکات مهم:
- **Async**: نیاز به polling
- **Voice cloning**: نیاز به upload نمونه صدا
- **Persian support**: باید تست کنیم! 🧪

### 🧪 تست‌های لازم:
1. ✅ آیا فارسی رو خوب تلفظ می‌کنه؟
2. ✅ کیفیت صدا چطوره؟
3. ✅ Voice cloning چند دقیقه sample نیاز داره؟
4. ✅ نمونه صدا باید چطور باشه (format, length, quality)?

---

## 5️⃣ Suno AI - Music Generation

### 📋 مشخصات:

```python
Submit: POST https://gptproto.com/v1/suno/submit/music
Query: GET https://gptproto.com/v1/suno/fetch/{task_id}
Models: chirp-v3-5 (جدید), chirp-v3-0 (قدیمی)
Response: Async (task-based)
```

### 🔧 نحوه استفاده:

#### مرحله 1: ارسال درخواست (3 حالت)

##### حالت A: Inspiration Mode (AI-driven) ⭐ پیشنهادی
```python
data = {
    "gpt_description_prompt": "Ethereal female vocals blending with cinematic drums",
    "mv": "chirp-v3-5",  # مدل جدید
    "make_instrumental": False  # با صدا
}
```

##### حالت B: Custom Mode (دقیق‌تر)
```python
data = {
    "prompt": "Compose a tense pre-battle anthem",  # توضیحات
    "tags": "cinematic,epic,ambient",  # سبک موسیقی
    "title": "Before the Charge",  # عنوان
    "mv": "chirp-v3-5",
    "make_instrumental": True  # بدون صدا (فقط موسیقی)
}
```

##### حالت C: Extension Mode (ادامه آهنگ قبلی)
```python
data = {
    "continue_clip_id": "clip-123456",  # ID کلیپ قبلی
    "continue_at": 8,  # ادامه از ثانیه 8
    "mv": "chirp-v3-5"
}
```

#### کد کامل:
```python
import requests
import time
import json

# مرحله 1: Submit
submit_url = "https://gptproto.com/v1/suno/submit/music"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # اینجا "Bearer" لازمه!
    "Content-Type": "application/json"
}

# برای پروژه ما (ریلز تکنولوژی):
submit_data = {
    "gpt_description_prompt": "Upbeat modern tech background music, electronic, energetic, 30 seconds, Instagram reel style",
    "mv": "chirp-v3-5",
    "make_instrumental": True  # بدون vocal
}

response = requests.post(submit_url, headers=headers, json=submit_data)
result = response.json()

if result["code"] == "success":
    task_id = result["data"]
    print(f"Task ID: {task_id}")

    # مرحله 2: Polling
    query_url = f"https://gptproto.com/v1/suno/fetch/{task_id}"

    for _ in range(60):  # حداکثر 5 دقیقه (60 × 5sec)
        time.sleep(5)

        query_response = requests.get(query_url, headers=headers)
        query_result = query_response.json()

        if query_result["code"] == "success" and query_result["data"]:
            task = query_result["data"][0]

            if task["status"] == "completed":
                audio_url = task["audio_url"]
                print(f"Music ready: {audio_url}")

                # اطلاعات اضافی:
                print(f"Duration: {task.get('duration')}s")
                print(f"Title: {task.get('title')}")
                break
            elif task["status"] == "failed":
                print(f"Failed: {task.get('error_message')}")
                break
            else:
                print(f"Status: {task['status']}...")
else:
    print(f"Error: {result['message']}")
```

### 📝 Parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| gpt_description_prompt | string | ❌ | AI-driven description (Inspiration mode) |
| prompt | string | ❌ | Custom lyrics/description (Custom mode) |
| tags | string | ❌ | Style tags: "cinematic,epic,ambient" |
| title | string | ❌ | Track title |
| mv | string | ❌ | Model: "chirp-v3-5" یا "chirp-v3-0" |
| make_instrumental | boolean | ❌ | true = بدون vocal, false = با vocal |
| continue_clip_id | string | ❌ | Clip ID برای extension |
| continue_at | number | ❌ | Second to extend from |

### 🎵 Prompts مناسب برای پروژه ما:

```python
# ریلز unboxing:
"Modern upbeat electronic music, tech vibe, exciting, 30 seconds"

# ریلز review:
"Sophisticated tech background, minimal electronic, professional, 45 seconds"

# ریلز comparison:
"Energetic comparison music, electronic beats, dynamic, 30 seconds"

# Intro/Outro:
"Tech podcast intro, modern synth, punchy, 10 seconds"
```

### ✅ مزایا:
- High quality output
- Multiple styles
- Duration control (30s, 60s, 2min)
- Instrumental option ⭐

### ⚠️ نکات:
- Async (نیاز به polling)
- Authorization: **"Bearer"** لازمه! (برخلاف بقیه)
- زمان تولید: ~30-60 ثانیه

---

## 🔐 Authentication Summary

### یکسان برای همه (به جز Suno):

```python
headers = {
    "Authorization": "YOUR_API_KEY",  # بدون "Bearer"
    "Content-Type": "application/json"
}
```

### فقط Suno:

```python
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # با "Bearer"
    "Content-Type": "application/json"
}
```

---

## ⚠️ Error Handling

### Error Codes مشترک:

| Code | معنی | راه‌حل |
|------|------|--------|
| 401 | Invalid API key | چک کن key درست باشه |
| 403 | Insufficient balance | اعتبار شارژ کن |
| 500 | Internal server error | دوباره امتحان کن |
| 503 | Content policy violation | محتوا رو تغییر بده |
| 429 | Rate limit exceeded | کمی صبر کن |

### Error Response Format:

```python
{
    "error": {
        "message": "Invalid signature",
        "type": "401"
    }
}
```

---

## 💰 قیمت‌گذاری (مستندات نداره!)

### ❓ سوالات:

1. هزینه per request چقدره؟
   - Claude: per 1M token?
   - Flux: per image?
   - MiniMax: per character/minute?
   - Suno: per track?

2. آیا rate limits هست؟
   - Requests per minute?
   - Daily quota?

3. آیا credit-based است یا pay-as-you-go?

### 🧪 نحوه تست هزینه:

```python
# 1. یک test account بساز با credit محدود
# 2. این تست‌ها رو انجام بده:
test_cases = [
    {"service": "Claude", "test": "1000 token prompt"},
    {"service": "Flux", "test": "1 image generation"},
    {"service": "MiniMax", "test": "30 sec audio"},
    {"service": "Suno", "test": "1 music track"}
]

# 3. Credit before/after رو چک کن
# 4. محاسبه هزینه واقعی
```

---

## 🎯 Integration Priority

### Phase 1 (Week 1): Core APIs
```
1. ✅ Claude (text generation)
2. ✅ Flux (image generation)
→ تست و تایید کیفیت
```

### Phase 2 (Week 2): Voice & Music
```
3. 🧪 MiniMax (Persian TTS - نیاز به تست دقیق)
4. ✅ Suno (music generation)
→ تست کیفیت فارسی و موسیقی
```

### Phase 3 (Week 3): Pipeline
```
5. ترکیب همه سرویس‌ها
6. Async task management
7. Error handling و retry logic
```

---

## ✅ خلاصه تحلیل

### ✅ چیزهایی که عالیه:

1. ✅ **Format استاندارد**: بیشتر OpenAI-compatible
2. ✅ **مستندات واضح**: نمونه کدهای کامل
3. ✅ **همه سرویس‌های لازم موجودند**
4. ✅ **Claude Sonnet 4.5**: بهترین برای فارسی
5. ✅ **Flux Pro**: عالی برای portrait
6. ✅ **Suno v3.5**: جدیدترین مدل موسیقی

### ⚠️ چیزهایی که نیاز به بررسی دارند:

1. ⚠️ **قیمت‌گذاری**: مستندات نداره
2. ⚠️ **Rate limits**: مشخص نیست
3. ⚠️ **MiniMax Persian quality**: باید تست کنیم
4. ⚠️ **Flux output format**: URL یا base64?
5. ⚠️ **Voice cloning requirements**: چند دقیقه sample؟

### 🧪 تست‌های فوری لازم:

```python
Priority 1 (امروز):
1. ✅ Claude: تولید caption فارسی
2. ✅ Flux: تولید portrait
3. 🧪 MiniMax: تست TTS فارسی ⭐ مهم‌ترین

Priority 2 (فردا):
4. ✅ Suno: تولید موسیقی ریلز
5. 💰 Cost tracking: هزینه واقعی
6. ⚡ Performance: سرعت و latency
```

---

## 🚀 Next Steps

### 1. کدنویسی (من انجام میدم):
```
✅ GPTProto client class
✅ Service wrappers (Claude, Flux, MiniMax, Suno)
✅ Async task manager
✅ Error handling
✅ Retry logic
✅ Cost tracking
```

### 2. تست‌ها (تو انجام بده):
```
1. API key رو بده
2. تست script رو اجرا کن
3. نتایج رو بررسی کن
4. فیدبک بده
```

### 3. Deploy:
```
✅ Backend setup
✅ Database
✅ Queue system
✅ MVP
```

---

**آماده کدنویسی! 🚀**

الان شروع می‌کنم به نوشتن کد integration...
