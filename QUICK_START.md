# 🚀 راهنمای سریع - تولید اولین ریلز

## وضعیت فعلی ✅

- ✅ **API Key**: تنظیم شده
- ✅ **Claude (Script)**: تست شده - عالی!
- ✅ **Flux (Image)**: تست شده - عالی!
- ✅ **Suno (Music)**: تست شده - عالی!
- ⏳ **MiniMax (Voice)**: منتظر voice sample

---

## یک قدم تا اولین ریلز! 🎬

فقط کافیه صدات رو ضبط کنی و همه چیز آماده است!

---

## مرحله 1: ضبط صدا (5 دقیقه)

### گزینه A: با گوشی (آسان‌ترین)

```
1. باز کن: Voice Memos (iOS) یا Voice Recorder (Android)
2. دکمه ضبط رو بزن
3. این متن رو بخون (طبیعی و با سرعت معمولی):
```

**متن برای خواندن:**
```
سلام! من امیرم، اینفلوئنسر تکنولوژی تهران.
امروز می‌خوام یکی از جدیدترین محصولات رو باهاتون بررسی کنم.
این گوشی یکی از بهترین پرچم‌داران امسال است.
دوربین 48 مگاپیکسلی، چیپ قدرتمند، و باتری عالی داره.
طراحی تیتانیوم سبک و مقاوم، نمایشگر 120 هرتز.
کیفیت ساخت فوق‌العاده است و تجربه کاربری روان.
اگه دنبال یک گوشی پرمیوم هستی، این انتخاب عالیه.
لینک خرید در بیو. ممنون که همراه ما بودی!
```

```
4. ذخیره کن
5. Share → Save to Files → Export
6. اسم فایل: amir_voice.m4a
```

### گزینه B: با کامپیوتر

```bash
# اگه ffmpeg داری:
ffmpeg -f avfoundation -i ":0" -t 60 amir_voice.m4a

# یا با QuickTime (Mac):
# File → New Audio Recording → Record → Save
```

---

## مرحله 2: انتقال فایل (2 دقیقه)

### اگه با گوشی ضبط کردی:

**روش 1: AirDrop (Mac + iPhone)**
```
1. گوشی: Share → AirDrop → انتخاب Mac
2. Mac: فایل رو Save کن در: Downloads/
3. کپی به پروژه:
   cp ~/Downloads/amir_voice.m4a ~/Ai-human/assets/voice/
```

**روش 2: Google Drive / iCloud**
```
1. آپلود به Drive/iCloud
2. دانلود روی کامپیوتر
3. کپی به: /home/user/Ai-human/assets/voice/amir_voice.m4a
```

**روش 3: Email**
```
1. Email به خودت
2. دانلود فایل
3. کپی به پوشه پروژه
```

### بعد از کپی، چک کن:

```bash
ls -lh assets/voice/amir_voice.m4a
# باید فایلی حدود 500KB - 5MB باشه
```

---

## مرحله 3: Push به GitHub (1 دقیقه)

```bash
cd /home/user/Ai-human

# اضافه کردن فایل
git add assets/voice/amir_voice.m4a

# کامیت
git commit -m "Add Amir voice sample for MiniMax cloning"

# پوش کردن
git push origin claude/review-amir-project-016rACWzFaraUxfkHFNLgViX
```

بعد از push، URL فایل:
```
https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a
```

---

## مرحله 4: تنظیم Environment (30 ثانیه)

```bash
# API Key (قبلاً تنظیم شده)
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"

# Voice URL (بعد از push)
export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"
```

---

## مرحله 5: تست Voice Clone (2 دقیقه)

```bash
cd /home/user/Ai-human

# تست voice cloning
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
✅ Task submitted: xxxxx

⏳ Step 2: Waiting for voice generation...
   (این ممکنه 30-60 ثانیه طول بکشه)

✅ Voice generated successfully!
============================================================

🔗 Audio URL:
   https://cdn.minimax.ai/...

👉 این فایل رو دانلود و گوش کن!
   آیا صدا شبیه صدای تو است؟
============================================================
```

### بررسی کیفیت:

1. URL رو باز کن
2. فایل صوتی رو دانلود کن
3. گوش کن:
   - ✅ آیا شبیه صدای توست؟
   - ✅ آیا تلفظ فارسی درست است؟
   - ✅ آیا کیفیت صدا خوب است؟

---

## مرحله 6: تولید اولین ریلز کامل! (3-5 دقیقه)

اگر voice clone موفق بود:

```bash
cd /home/user/Ai-human

# تولید ریلز کامل
python backend/scripts/generate_first_reel.py
```

**این script تولید می‌کنه:**

1. ✅ **Script فارسی** - با Claude
   - Hook جذاب (3 ثانیه)
   - Body توضیحات (24 ثانیه)
   - CTA قوی (3 ثانیه)
   - Hashtags مناسب

2. ✅ **تصویر امیر** - با Flux
   - پرتره photorealistic
   - 28 ساله، اینفلوئنسر تهران
   - نگه داشتن محصول

3. ✅ **صدای clone شده** - با MiniMax
   - صدای طبیعی فارسی
   - Clone از صدای تو
   - کیفیت HD

4. ✅ **موسیقی پس‌زمینه** - با Suno
   - تِک، مدرن، energetic
   - مناسب Instagram Reels
   - Instrumental (بدون vocal)

**خروجی:**
```
reels_output/
├── iPhone_16_Pro_Max_assets.json      # تمام metadata
├── iPhone_16_Pro_Max_script.txt       # اسکریپت کامل
├── image_xxxxx.png                    # تصویر
├── voice_xxxxx.mp3                    # صدا
└── music_xxxxx.mp3                    # موسیقی
```

---

## مرحله 7: بررسی نتایج

```bash
# چک کردن فایل‌های تولید شده
ls -lh reels_output/

# خواندن script
cat reels_output/iPhone_16_Pro_Max_script.txt

# بررسی JSON
cat reels_output/iPhone_16_Pro_Max_assets.json | jq .
```

### Assets که داری:

1. **Script**: فایل .txt
2. **Image**: URL در JSON
3. **Voice**: URL + فایل محلی MP3
4. **Music**: URL در JSON

---

## Troubleshooting

### مشکل 1: Voice clone fail شد

```bash
# چک کن URL در دسترس باشه:
curl -I "$VOICE_SAMPLE_URL"
# باید 200 OK برگردونه

# اگر 404: فایل push نشده
git push origin claude/review-amir-project-016rACWzFaraUxfkHFNLgViX

# اگر فایل خیلی بزرگ (>10MB):
# کیفیت رو کم کن:
ffmpeg -i amir_voice.m4a -b:a 128k amir_voice_compressed.m4a
```

### مشکل 2: API Error (403/401)

```bash
# چک کردن API key:
echo $GPTPROTO_API_KEY

# دوباره تنظیم کن:
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
```

### مشکل 3: Python Import Error

```bash
# مطمئن شو که در virtual environment هستی:
source backend/venv/bin/activate

# نصب dependencies:
pip install -r backend/requirements.txt
```

---

## چک‌لیست کامل ✅

قبل از تولید ریلز، این‌ها رو چک کن:

- [ ] API Key تنظیم شده (`echo $GPTPROTO_API_KEY`)
- [ ] فایل صوتی ضبط شده (`ls assets/voice/amir_voice.m4a`)
- [ ] فایل به GitHub پوش شده (`git status`)
- [ ] VOICE_SAMPLE_URL تنظیم شده (`echo $VOICE_SAMPLE_URL`)
- [ ] Voice clone تست شده (`python test_voice_clone.py`)
- [ ] کیفیت صدا تایید شده (گوش دادن به output)

---

## دستورات یکجا 🎯

```bash
# تنظیم environment
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
export VOICE_SAMPLE_URL="https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a"

# چک کردن وضعیت
python backend/scripts/workflow_helper.py

# تست voice clone
python backend/scripts/test_voice_clone.py

# تولید اولین ریلز
python backend/scripts/generate_first_reel.py
```

---

## مرحله بعدی (بعد از موفقیت)

1. **Video Pipeline**: Wav2Lip برای lip-sync
2. **FFmpeg Composition**: ترکیب همه assets
3. **Watermarking**: اضافه کردن #AIgenerated
4. **Admin UI**: داشبورد مدیریت
5. **Automation**: تولید خودکار روزانه

---

## سوالات متداول

**Q: چقدر طول می‌کشه تا یک ریلز تولید بشه؟**
A: 3-5 دقیقه (Script: 5s, Image: 20s, Voice: 60s, Music: 90s)

**Q: هزینه هر ریلز چقدر است؟**
A: حدود $0.77 (Script: $0.02, Image: $0.15, Voice: $0.40, Music: $0.20)

**Q: آیا می‌تونم صدای دیگه‌ای استفاده کنم؟**
A: بله! فقط فایل جدید رو ضبط کن و URL رو عوض کن.

**Q: کیفیت تصاویر و صدا رو می‌شه بهتر کرد؟**
A: بله، با تنظیم parameters در script‌ها (مثل accuracy=0.9)

---

**🎬 آماده؟ فقط صدات رو ضبط کن و بقیه رو به سیستم بسپار!**
