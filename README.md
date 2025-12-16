# 🤖 Moliyaviy Tahlil Telegram Boti

O'zbekiston foydalanuvchilari uchun AI-asoslangan shaxsiy moliyaviy tahlil va maslahat boti.

## 📋 Xususiyatlar

- ✅ To'liq moliyaviy so'rovnoma (daromad, xarajat, jamg'arma, qarzlar)
- 🤖 Claude AI tomonidan shaxsiy tahlil va tavsiyalar
- 📊 Progress bar va qulay interfeys
- 💾 Barcha ma'lumotlarni JSON formatida saqlash
- 📈 CustDev uchun analytics log (JSONL format)
- 🇺🇿 To'liq o'zbekcha til

## 🚀 O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone <your-repo-url>
cd telegram-finance-bot
```

### 2. Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Environment o'zgaruvchilarini sozlash

`.env.example` faylini `.env` ga nusxalang:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
ANTHROPIC_API_KEY=your_anthropic_api_key
```

#### Telegram Bot Token olish:

1. [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username'ini kiriting
4. Token'ni oling va `.env` ga qo'shing

#### Anthropic API Key olish:

1. [console.anthropic.com](https://console.anthropic.com) ga ro'yxatdan o'ting
2. Yangi foydalanuvchilar uchun **$5 kredit** beriladi
3. API Keys bo'limidan yangi key yarating
4. Key'ni `.env` ga qo'shing

### 5. Botni ishga tushirish

```bash
python bot.py
```

Botingiz tayyor! Telegram'da botingizga `/start` yuboring.

## 📁 Loyiha strukturasi

```
telegram-finance-bot/
├── bot.py              # Asosiy bot logikasi
├── config.py           # Konfiguratsiya va savollar
├── data_manager.py     # Ma'lumotlarni boshqarish
├── ai_analyzer.py      # Claude AI integratsiyasi
├── utils.py            # Yordamchi funksiyalar
├── requirements.txt    # Python kutubxonalari
├── .env.example        # Environment example
├── README.md           # Dokumentatsiya
└── data/               # Ma'lumotlar papkasi (avtomatik yaratiladi)
    ├── users/          # Har bir foydalanuvchi uchun alohida JSON
    └── analytics/      # Session loglari (JSONL format)
```

## 📊 Ma'lumotlar strukturasi

### User data (data/users/{user_id}.json)

```json
{
  "user_id": 123456789,
  "started_at": "2025-01-15T10:30:00",
  "session_id": "session_20250115_103000",
  "current_question": 5,
  "completed": false,
  "answers": {
    "income_monthly": "5000000",
    "expense_monthly": "3500000",
    ...
  },
  "ai_analysis": "AI tahlil matni...",
  "updated_at": "2025-01-15T10:45:00"
}
```

### Analytics log (data/analytics/sessions_log.jsonl)

Har bir qator - alohida JSON:

```json
{"timestamp": "2025-01-15T10:30:00", "user_id": 123, "session_id": "session_...", "question_key": "income_monthly", "answer": "5000000", "section": "daromad"}
{"timestamp": "2025-01-15T10:35:00", "user_id": 123, "session_id": "session_...", "event_type": "ai_analysis", "analysis": "..."}
```

## 🎯 Bot buyruqlari

- `/start` - Botni boshlash
- `/help` - Yordam
- `/cancel` - So'rovnomani bekor qilish
- `/stats` - Statistika (admin uchun)

## 🔧 Sozlamalarni o'zgartirish

### Savollarni qo'shish/o'zgartirish

`config.py` faylida `QUESTIONS` va `QUESTION_ORDER` ni tahrirlang:

```python
QUESTIONS = {
    'yangi_savol': {
        'text': "Sizning yangi savolingiz?",
        'type': 'number',  # number, text, choice, multi_choice, rating
        'section': 'daromad'
    }
}

QUESTION_ORDER = [
    'yangi_savol',
    ...
]
```

### AI promptni sozlash

`ai_analyzer.py` faylida `_create_analysis_prompt` metodini tahrirlang.

## 📈 Analytics va CustDev

### Barcha session loglarini ko'rish:

```python
from data_manager import DataManager

dm = DataManager()
logs = dm.export_analytics()

# Analizlar
for log in logs:
    print(log)
```

### Statistika olish:

```python
stats = dm.get_user_stats()
print(f"Jami foydalanuvchilar: {stats['total_users']}")
print(f"To'ldirilgan: {stats['completed_surveys']}")
```

## 💰 Narxlar

### Anthropic API:

- **Yangi foydalanuvchilar:** $5 kredit (test uchun kifoya)
- **Claude Sonnet 4:** ~$3 per 1M input tokens, ~$15 per 1M output tokens
- **Bizning bot:** Har bir tahlil ~$0.01-0.05

1000 ta tahlil ≈ $10-50

## 🔐 Xavfsizlik

- API keylarni hech qachon GitHub'ga yuklmang
- `.env` fayili `.gitignore`da
- User data faqat local serverda

## 🐛 Muammolarni hal qilish

### Bot ishlamayapti:

1. `.env` faylida tokenlar to'g'ri kiritilganini tekshiring
2. Internet aloqani tekshiring
3. `python bot.py` da xatoliklarni o'qing

### AI tahlil ishlamayapti:

1. ANTHROPIC_API_KEY to'g'ri kiritilganini tekshiring
2. API kredit borligini tekshiring
3. Loglarni tekshiring

### Ma'lumotlar saqlanmayapti:

1. `data/` papkasi yaratilganini tekshiring
2. Fayl yozish ruxsatini tekshiring

## 🚀 Production deployment

### Hosting variantlari:

1. **DigitalOcean Droplet** ($5/month)
2. **AWS EC2** (free tier)
3. **Heroku** (free tier - limited)
4. **Railway.app**
5. **PythonAnywhere**

### Deployment qadamlari:

```bash
# Servergayuklash
git clone <repo>
cd telegram-finance-bot

# Virtual muhit
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Environment
nano .env  # tokenlarni kiriting

# Screen yoki tmux ishlatish
screen -S finance-bot
python bot.py

# Detach: Ctrl+A, D
```

### Avtomatik restart (systemd):

`/etc/systemd/system/finance-bot.service` yarating:

```ini
[Unit]
Description=Finance Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-finance-bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Ishga tushirish:

```bash
sudo systemctl enable finance-bot
sudo systemctl start finance-bot
sudo systemctl status finance-bot
```

## 📞 Aloqa

Agar savol yoki muammo bo'lsa, issue oching yoki to'g'ridan-to'g'ri murojaat qiling.

## 📝 Litsenziya

MIT License

## 🎉 Minnatdorchilik

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Anthropic Claude](https://www.anthropic.com/claude)

---

**Muvaffaqiyatlar! 🚀**
