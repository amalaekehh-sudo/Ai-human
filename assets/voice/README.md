# 🎤 راهنمای ضبط صدای امیر

## مرحله 1: ضبط صدا

### متن برای خواندن:
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

### تنظیمات ضبط:
- **مدت زمان**: 30-60 ثانیه
- **کیفیت**: حداقل 44.1kHz, 16-bit
- **فرمت**: M4A, MP3, یا WAV
- **محیط**: ساکت، بدون نویز پس‌زمینه
- **فاصله**: 15-20 سانتی از میکروفون
- **لحن**: طبیعی، نه خیلی رسمی، نه خیلی غیررسمی

### نکات مهم:
✅ صدای واضح و طبیعی
✅ سرعت متوسط (نه خیلی سریع، نه خیلی آهسته)
✅ تلفظ دقیق کلمات
✅ بدون echo یا reverb
✅ حجم صدا ثابت (نه خیلی آرام، نه خیلی بلند)

❌ نویز پس‌زمینه (ترافیک، فن، باد)
❌ تکان دادن گوشی حین ضبط
❌ تنفس بلند جلوی میکروفون

---

## مرحله 2: ذخیره فایل

بعد از ضبط، فایل رو اینجا ذخیره کن:
```
/home/user/Ai-human/assets/voice/amir_voice.m4a
```

یا اگه با گوشی ضبط کردی:
1. فایل رو به کامپیوتر منتقل کن (AirDrop, USB, Email)
2. کپی کن به این پوشه
3. اسم فایل رو عوض کن به `amir_voice.m4a`

---

## مرحله 3: آپلود به GitHub

```bash
# از دایرکتوری اصلی پروژه:
git add assets/voice/amir_voice.m4a
git commit -m "Add Amir voice sample for MiniMax cloning"
git push origin claude/review-amir-project-016rACWzFaraUxfkHFNLgViX
```

بعد از push، URL فایل:
```
https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/claude/review-amir-project-016rACWzFaraUxfkHFNLgViX/assets/voice/amir_voice.m4a
```

یا اگه به main branch پوش کنی:
```
https://raw.githubusercontent.com/amalaekehh-sudo/Ai-human/main/assets/voice/amir_voice.m4a
```

---

## مرحله 4: تست Voice Clone

```bash
# تنظیم API Key
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"

# تست voice cloning
cd /home/user/Ai-human
python backend/scripts/test_voice_clone.py
```

Script خودش URL رو از فایل محلی می‌خونه!

---

## مرحله 5: تولید اولین ریلز

بعد از موفقیت تست:

```bash
export GPTPROTO_API_KEY="sk-918fb169e8de414fb8ecc09901690ecd"
python backend/scripts/generate_first_reel.py
```

این script تولید می‌کنه:
- ✅ Script فارسی (Claude)
- ✅ تصویر امیر (Flux)
- ✅ صدای clone شده (MiniMax)
- ✅ موسیقی (Suno)

---

## وضعیت فعلی:

- [ ] ضبط صدا
- [ ] ذخیره فایل در assets/voice/
- [ ] آپلود به GitHub
- [ ] تست voice clone
- [ ] تولید اولین ریلز

---

**بعد از ضبط صدا، فقط بگو "آماده" تا همه چیز رو تست کنیم!** 🎬
