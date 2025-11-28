# 🤖 Amir - AI Influencer Platform

یک سیستم کامل تولید محتوای خودکار برای اینفلوئنسر AI به نام "امیر" - ریویوئر 28 ساله تکنولوژی و گجت در تهران.

## 📋 وضعیت پروژه

**Phase: Initial Development**
**Status: ✅ API Integration Ready**

### پیشرفت:
- [x] تحلیل پروژه و نیازسنجی
- [x] بررسی GPTProto و سرویس‌های موجود
- [x] طراحی معماری
- [x] نوشتن GPTProto client
- [x] نوشتن service wrappers
- [x] آماده‌سازی test scripts
- [ ] تست APIs با API key واقعی
- [ ] ساخت MVP
- [ ] تولید اولین محتوای نمونه

---

## 🎯 هدف پروژه

تولید **خودکار** محتوای حرفه‌ای برای اینستاگرام:
- ✅ ریلزهای 30-45 ثانیه‌ای
- ✅ پست‌های فید (4:5)
- ✅ استوری‌های تعاملی
- ✅ پاسخ به کامنت‌ها

### ویژگی‌های کلیدی:
- 🎬 **Pipeline کامل**: Script → Voice → Image → Video → Music
- 🇮🇷 **فارسی First-Class**: تولید محتوای طبیعی فارسی
- 🏷️ **Transparency**: واترمارک #AIgenerated
- 📊 **Analytics**: ردیابی عملکرد و بهینه‌سازی
- 🔐 **Provenance**: ذخیره کامل metadata تولید

---

## 🏗️ معماری

```
Frontend (React)     →  Admin UI برای مدیریت کمپین‌ها
     ↓
Backend (FastAPI)    →  API endpoints
     ↓
Workers (Celery)     →  تولید async محتوا
     ↓
GPTProto Services    →  AI APIs
  ├─ Claude          →  Script generation (فارسی)
  ├─ Flux            →  Image generation (portrait)
  ├─ MiniMax         →  Voice/TTS (فارسی)
  └─ Suno            →  Music generation
     ↓
Storage (S3 + CDN)   →  ذخیره و توزیع assets
```

---

## 🛠️ Tech Stack

### Backend:
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Queue**: Celery + Redis
- **HTTP Client**: httpx (async)

### AI Services (via GPTProto):
- **LLM**: Claude Sonnet 4.5 (script & caption)
- **Image**: Flux Kontext Pro (portrait)
- **Voice**: MiniMax Speech-2.5-HD (Persian TTS)
- **Music**: Suno AI chirp-v3-5

### Infrastructure:
- **Storage**: S3-compatible + CDN
- **Deployment**: Docker + Kubernetes
- **Monitoring**: Prometheus + Grafana + Sentry

---

## 🚀 Quick Start

### 1. نصب Dependencies

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. تنظیم Environment

```bash
# کپی کردن .env.example
cp .env.example .env

# ویرایش .env و اضافه کردن API key
nano .env
```

در فایل `.env`:
```bash
GPTPROTO_API_KEY=sk-your-api-key-here
```

### 3. تست APIها

```bash
# تست همه سرویس‌های GPTProto
export GPTPROTO_API_KEY='sk-your-key-here'
python backend/scripts/test_gptproto_apis.py
```

این script تست می‌کنه:
- ✅ Claude: تولید caption فارسی
- ✅ Flux: تولید تصویر portrait
- ✅ MiniMax: تولید صدای فارسی (⭐ مهم!)
- ✅ Suno: تولید موسیقی ریلز

---

## 📖 مستندات

### فایل‌های تحلیل و طراحی:

1. **PROJECT_ANALYSIS.md** - تحلیل اولیه کامل پروژه
2. **GPTPROTO_FINDINGS.md** - بررسی GPTProto (Claude API proxy)
3. **REQUIRED_AI_SERVICES.md** - لیست سرویس‌های مورد نیاز
4. **GPTPROTO_SERVICES_ANALYSIS.md** - تطبیق سرویس‌ها با نیازها
5. **GPTPROTO_API_ANALYSIS.md** - تحلیل دقیق API documentation

### کد اصلی:

```
backend/
├── app/
│   ├── services/
│   │   ├── gptproto/
│   │   │   └── client.py              # GPTProto client
│   │   └── ai/
│   │       └── script_generator.py    # Script & caption generator
│   └── ...
└── scripts/
    └── test_gptproto_apis.py          # Test suite
```

---

## 💰 هزینه‌ها (برآورد)

### تولید یک ریلز 30 ثانیه‌ای:

| مرحله | سرویس | هزینه |
|-------|-------|-------|
| Script | Claude | $0.02 |
| Image (3x) | Flux | $0.15 |
| Voice | MiniMax | $0.40 |
| Video | Wav2Lip (GPU) | $0.50 |
| Music | Suno | $0.02 |
| **Total** | | **~$1.10** |

### ماهانه (50 ریلز):
- AI Services: ~$55
- Infrastructure: ~$200-300
- **Total: ~$250-350/month**

---

## 🧪 تست API ها

### نمونه استفاده از Client:

```python
import asyncio
from app.services.gptproto.client import GPTProtoClient

async def main():
    client = GPTProtoClient(api_key="sk-xxx")

    # تولید caption فارسی
    result = await client.chat_completion(
        model="claude-sonnet-4-5-20250929",
        messages=[
            {"role": "user", "content": "یک caption برای iPhone 16 Pro بنویس"}
        ]
    )

    print(result["choices"][0]["message"]["content"])

    await client.close()

asyncio.run(main())
```

### نمونه Script Generator:

```python
from app.services.ai.script_generator import ScriptGenerator

async def main():
    client = GPTProtoClient(api_key="sk-xxx")
    script_gen = ScriptGenerator(client)

    result = await script_gen.generate_reel_script(
        product_name="iPhone 16 Pro Max",
        key_features=["دوربین 48MP", "چیپ A18 Pro"],
        duration=30,
        format_type="review"
    )

    print(result["script"])

asyncio.run(main())
```

---

## 📊 Pipeline تولید محتوا

```
1. Campaign Request
   ↓
2. Script Generation (Claude)
   ↓
3. Image Generation (Flux) - تصویر امیر
   ↓
4. Voice Generation (MiniMax) - صدای فارسی
   ↓
5. Lip-sync (Wav2Lip) - لب‌خوانی
   ↓
6. Music (Suno) - موسیقی پس‌زمینه
   ↓
7. Composition (FFmpeg) - ترکیب + زیرنویس + واترمارک
   ↓
8. Moderation (Claude) - بررسی محتوا
   ↓
9. Human Review - تایید نهایی
   ↓
10. Publish - انتشار در اینستاگرام
```

---

## 🔐 Security & Privacy

- ✅ API keys در environment variables (نه در کد)
- ✅ Secrets در vault/secret manager
- ✅ واترمارک #AIgenerated روی تمام محتوا
- ✅ Provenance metadata برای هر asset
- ✅ Content moderation قبل از انتشار
- ✅ Human-in-the-loop برای محتوای sponsored

---

## 🎯 Roadmap

### Phase 1: MVP (هفته 1-4)
- [x] GPTProto integration
- [x] Script generator
- [ ] تست کامل APIها
- [ ] Image + Voice pipeline
- [ ] اولین ریلز نمونه

### Phase 2: Full Pipeline (هفته 5-8)
- [ ] Video lip-sync (Wav2Lip)
- [ ] Music integration
- [ ] FFmpeg composition
- [ ] Watermarking
- [ ] Admin UI (React)

### Phase 3: Production (هفته 9-12)
- [ ] Campaign management
- [ ] Scheduling
- [ ] Analytics
- [ ] Content moderation
- [ ] Deploy to production

---

## 🐛 Troubleshooting

### API Key Error (401):
```bash
# چک کن API key درست باشه:
echo $GPTPROTO_API_KEY

# یا در .env:
cat .env | grep GPTPROTO_API_KEY
```

### Insufficient Balance (403):
```bash
# اعتبار account رو چک کن در GPTProto dashboard
```

### Persian TTS Quality Issues:
```bash
# اگر MiniMax فارسی ضعیف بود:
# → استفاده از ElevenLabs (خارج از GPTProto)
```

---

## 🤝 Contributing

این پروژه در حال توسعه است. برای مشارکت:

1. مستندات رو بخون
2. تست‌ها رو اجرا کن
3. تغییرات رو commit کن با پیام واضح
4. PR بزن

---

## 📄 License

این پروژه private است و تحت قرارداد محرمانگی.

---

## 📞 Contact

**Project Owner**: امیر - AI Influencer Platform
**Developer**: Claude Code + Your Team
**Repository**: github.com/amalaekehh-sudo/Ai-human

---

**🚀 آماده ساختن یک AI Influencer حرفه‌ای!**

برای شروع، ابتدا API key رو تنظیم کن و test script رو اجرا کن:
```bash
export GPTPROTO_API_KEY='sk-your-key'
python backend/scripts/test_gptproto_apis.py
```
