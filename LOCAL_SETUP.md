# 🖥️ راهنمای اجرا روی Mac/کامپیوتر محلی

## ⚠️ چرا باید روی کامپیوتر خودت اجرا کنی؟

محیط Claude Code دسترسی به `gptproto.com` رو بلاک می‌کنه.
برای استفاده از MiniMax voice clone، باید کد رو روی Mac خودت اجرا کنی.

---

## 📋 پیش‌نیازها

1. ✅ Mac/Linux/Windows با Python 3.11+
2. ✅ Git نصب باشه
3. ✅ فایل صوتی (قبلاً آپلود کردی ✅)
4. ✅ API Key (داری ✅)

---

## 🚀 مراحل نصب (یکبار)

### قدم 1: Clone کردن پروژه

```bash
cd ~/Documents  # یا هر جایی که می‌خوای

# Clone از GitHub
git clone https://github.com/amalaekehh-sudo/Ai-human.git
cd Ai-human

# Checkout به branch فعلی
git checkout claude/review-amir-project-016rACWzFaraUxfkHFNLgViX
```

### قدم 2: نصب Python Dependencies

```bash
# ساخت virtual environment
python3 -m venv venv

# فعال کردن (Mac/Linux)
source venv/bin/activate

# یا اگه Windows:
# venv\Scripts\activate

# نصب packages
pip install -r backend/requirements.txt
```

**خروجی موردانتظار:**
```
Successfully installed fastapi httpx loguru pydantic ...
```

### قدم 3: تنظیم Environment Variables

```bash
# تنظیم API Key
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"

# تنظیم Voice URL
export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"

# برای راحتی، می‌تونی اینا رو به .bashrc یا .zshrc اضافه کنی:
echo 'export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"' >> ~/.zshrc
echo 'export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"' >> ~/.zshrc

# Reload
source ~/.zshrc
```

---

## ✅ تست سیستم

### تست 1: چک کردن وضعیت

```bash
python backend/scripts/workflow_helper.py
```

**خروجی مورد انتظار:**
```
============================================================
📊 وضعیت پروژه Amir AI Influencer
============================================================

1️⃣ API Key:
✅ API Key: sk-918fb16...90ecd

2️⃣ Voice Sample:
✅ URL تنظیم شده: https://raw.githubusercontent.com/...

============================================================
✅ همه چیز آماده است!

🎬 مرحله بعدی:
   python backend/scripts/test_voice_clone.py
============================================================
```

### تست 2: Voice Clone

```bash
python backend/scripts/test_voice_clone.py
```

**خروجی مورد انتظار:**
```
🎤 MiniMax Voice Clone Test
============================================================

✅ Voice Sample URL:
   https://raw.githubusercontent.com/.../amir_voice.m4a

📝 Test Text:
   سلام! من امیرم...

⏳ Step 1: Submitting voice clone request...
✅ Task submitted: 17ac9b6e-xxxx

⏳ Step 2: Waiting for voice generation...
   (این ممکنه 30-60 ثانیه طول بکشه)

✅ Voice generated successfully!
============================================================

🔗 Audio URL:
   https://cdn.minimax.ai/minimax-...

👉 این فایل رو دانلود و گوش کن!
   آیا صدا شبیه صدای تو است؟
============================================================
```

### تست 3: تولید اولین ریلز

اگر voice clone موفق بود:

```bash
python backend/scripts/generate_first_reel.py
```

**خروجی مورد انتظار:**
```
🎬 تولید اولین ریلز - iPhone 16 Pro Max
============================================================

⏳ Step 1/4: Generating script with Claude...
✅ Script generated (256 chars)

⏳ Step 2/4: Generating image with Flux...
✅ Image generated: https://cdn.flux.ai/...

⏳ Step 3/4: Generating voice with MiniMax...
✅ Voice cloned: https://cdn.minimax.ai/...
   Saved to: reels_output/voice_xxxxx.mp3

⏳ Step 4/4: Generating music with Suno...
✅ Music generated: https://cdn.suno.ai/...

============================================================
✅ همه assets تولید شدند!
============================================================

📂 Assets Location:
   reels_output/iPhone_16_Pro_Max_assets.json

📝 Script:
   [Hook]
   تا حالا دوربین 48 مگاپیکسلی استفاده کردی؟...
```

---

## 📁 ساختار فایل‌های خروجی

بعد از اجرا:

```
Ai-human/
├── reels_output/
│   ├── iPhone_16_Pro_Max_assets.json    # همه URLها و metadata
│   ├── iPhone_16_Pro_Max_script.txt     # اسکریپت کامل
│   ├── image_xxxxx.png                  # تصویر از Flux
│   ├── voice_xxxxx.mp3                  # صدای clone شده
│   └── music_xxxxx.mp3                  # موسیقی از Suno (اختیاری)
```

**محتوای JSON:**
```json
{
  "product_name": "iPhone 16 Pro Max",
  "generated_at": "2025-11-30T08:30:00",
  "assets": {
    "script": {
      "full_script": "...",
      "hook": "...",
      "body": "...",
      "cta": "..."
    },
    "image": {
      "url": "https://cdn.flux.ai/...",
      "prompt": "..."
    },
    "voice": {
      "url": "https://cdn.minimax.ai/...",
      "local_path": "reels_output/voice_xxxxx.mp3"
    },
    "music": {
      "url": "https://cdn.suno.ai/..."
    }
  }
}
```

---

## 🔧 Troubleshooting

### مشکل 1: ModuleNotFoundError

```bash
# مطمئن شو virtual environment فعال است:
source venv/bin/activate

# دوباره نصب کن:
pip install -r backend/requirements.txt
```

### مشکل 2: API Key Invalid

```bash
# چک کن که تنظیم شده:
echo $GPTPROTO_API_KEY

# دوباره تنظیم کن:
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
```

### مشکل 3: Voice Clone Failed (403)

```bash
# چک کن که روی Mac اجرا می‌کنی (نه Claude Code):
curl -I https://gptproto.com

# باید 200 OK برگردونه، نه 403
```

### مشکل 4: Voice URL 404

```bash
# چک کن فایل در GitHub موجود است:
curl -I "$VOICE_SAMPLE_URL"

# یا مستقیماً:
curl -I "https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"

# باید 200 OK برگردونه
```

---

## 🎯 دستورات یکجا (Run Everything)

بعد از نصب، هر بار که می‌خوای تست کنی:

```bash
# فعال کردن environment
cd ~/Documents/Ai-human
source venv/bin/activate

# تنظیم keys
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"

# تولید ریلز
python backend/scripts/generate_first_reel.py
```

یا یک script shell بساز:

```bash
#!/bin/bash
# run_amir.sh

cd ~/Documents/Ai-human
source venv/bin/activate

export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"

python backend/scripts/generate_first_reel.py
```

بعد:
```bash
chmod +x run_amir.sh
./run_amir.sh
```

---

## 📊 هزینه‌ها (تقریبی)

هر ریلز کامل:
- Script (Claude): ~$0.02
- Image (Flux): ~$0.15
- Voice (MiniMax): ~$0.40
- Music (Suno): ~$0.20

**جمع: ~$0.77 per reel**

---

## 🔄 Pull کردن آخرین تغییرات

هر بار قبل از اجرا، آخرین تغییرات رو بکش:

```bash
cd ~/Documents/Ai-human
git pull origin claude/review-amir-project-016rACWzFaraUxfkHFNLgViX
```

---

## ✨ بعد از موفقیت

وقتی voice clone موفق شد، می‌تونی:

1. **تولید دسته‌ای:** چندین محصول رو پشت سر هم بدی
2. **ایجاد API:** FastAPI server رو اجرا کنی برای dashboard
3. **Automation:** Celery برای تولید روزانه خودکار
4. **Video Pipeline:** Wav2Lip برای lip-sync اضافه کنی

---

**🎬 آماده‌ای؟ همه چیز push شده، فقط clone کن و اجرا کن!**
