# 🤖 Moliyaviy Tahlil Telegram Boti

O'zbekiston foydalanuvchilari uchun AI-asoslangan shaxsiy moliyaviy tahlil va maslahat boti.

## ✨ Nima qiladi?

Bu bot sizning 2024-yildagi moliyaviy holatizngizni tahlil qilib, 2025-yil uchun shaxsiy tavsiyalar beradi:

- 💰 Daromad va xarajatlarizngizni tahlil qiladi
- 📊 Moliyaviy ko'rsatkichlarni hisoblaydi  
- 🤖 AI yordamida shaxsiy maslahatlar beradi
- 📈 Daromadni oshirish va xarajatni kamaytirish yo'llarini ko'rsatadi
- 🎯 Konkret harakat rejasi tayyorlaydi

## 🚀 Qanday ishlataman?

### 1-qadam: Telegram bot yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` yuboring
3. Bot nomini kiriting (masalan: "Mening moliyaviy botim")
4. Username kiriting (masalan: @mening_moliya_bot)
5. BotFather sizga **token** beradi - uni nusxalab oling!

### 2-qadam: Claude API key olish

1. [console.anthropic.com](https://console.anthropic.com) ga kiring
2. Ro'yxatdan o'ting (email bilan)
3. **$5 bepul kredit** olasiz! (taxminan 500 ta tahlil qilish uchun yetadi)
4. "API Keys" bo'limiga o'ting
5. "Create Key" bosib, yangi key oling
6. Key'ni nusxalab oling!

### 3-qadam: Serverni tayyorlash

Serverizngizda yoki kompyuterizngizda:

```bash
# Fayllarni yuklab oling
cd telegram-finance-bot

# Virtual muhit yarating (ixtiyoriy)
python3 -m venv venv
source venv/bin/activate

# Kutubxonalarni o'rnating
pip install -r requirements.txt
```

### 4-qadam: .env faylini yaratish

`.env.example` faylini `.env` ga nusxalang:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang va tokenlarizngizni qo'shing:

```env
TELEGRAM_BOT_TOKEN=shu_yerga_bot_tokenizngizni_qoying
ANTHROPIC_API_KEY=shu_yerga_claude_api_keyni_qoying
```

### 5-qadam: Ishga tushirish

```bash
python bot.py
```

Tayyor! Endi Telegram'da botingizga o'ting va `/start` bosing! 🎉

## 📱 Bot qanday ishlaydi?

1. **Start** - Bot salom beradi va boshlanadi
2. **Savollar** - Bot sizga 40 ta savol beradi:
   - Daromad haqida (ish haqi, biznes, investitsiya)
   - Xarajatlar haqida (uy-joy, ovqat, transport)
   - Jamg'arma va qarzlar haqida
   - Maqsad va rejalarizngiz
3. **AI Tahlil** - Barcha javoblarizngizni tahlil qilib, shaxsiy maslahatlar beradi
4. **Natija** - Siz quyidagilarni olasiz:
   - ✅ Moliyaviy holatizngiz tahlili
   - ⚠️ Diqqat qilish kerak bo'lgan masalalar
   - 💡 Konkret tavsiyalar
   - 📈 Daromad oshirish yo'llari
   - 🎁 Bir oylik harakat rejasi

## 💰 Narxlar

### Claude API narxlari:
- Yangi foydalanuvchilar: **$5 bepul kredit** ✨
- Har bir tahlil: **$0.01-0.05** (1-5 sent)
- 1000 ta tahlil: **$10-50**

Ya'ni $5 kredit bilan **100-500 ta** tahlil olasiz! 🎉

### Hosting narxlari:
- **DigitalOcean**: $5/oy
- **AWS EC2**: Bepul (1 yil)
- **Heroku**: Bepul (cheklangan)

## 📊 Ma'lumotlar qaerda saqlanadi?

Barcha ma'lumotlar `data/` papkasida:

```
data/
├── users/              # Har bir foydalanuvchi uchun alohida fayl
│   ├── 123456789.json  # User ID asosida
│   └── 987654321.json
└── analytics/          # Tahlil uchun loglar
    └── sessions_log.jsonl
```

**Xavfsizlik:**
- Faqat sizning serverizngizda
- Parollar va shaxsiy ma'lumotlar yo'q
- GitHub'ga yuklanmaydi (.gitignore)

## 🔧 Sozlamalar

### Savollarni o'zgartirish

`config.py` faylini oching va `QUESTIONS` ni tahrirlang:

```python
QUESTIONS = {
    'yangi_savol': {
        'text': "Sizning yangi savolingiz?",
        'type': 'number',  # number, text, choice, rating
        'section': 'daromad'
    }
}
```

### AI tahlilni sozlash

`ai_analyzer.py` faylida `_create_analysis_prompt` funksiyasini tahrirlang.

## ❓ Tez-tez so'raladigan savollar

**1. Anthropic API key qanday olaman?**
- [console.anthropic.com](https://console.anthropic.com) ga kiring
- Ro'yxatdan o'ting
- $5 bepul kredit olasiz
- "API Keys" dan yangi key yarating

**2. Bot ishlamayapti, nima qilaman?**
- `.env` faylidagi tokenlarni tekshiring
- Internet aloqasini tekshiring
- `python bot.py` da xatoliklarni o'qing

**3. AI tahlil ishlamayapti?**
- ANTHROPIC_API_KEY to'g'ri kiritilganini tekshiring
- API kredit borligini tekshiring (console.anthropic.com)
- Xatolik xabarlarini o'qing

**4. Qancha pul sarflaydi?**
- Har bir tahlil ~$0.01-0.05
- $5 kredit ~100-500 tahlil uchun yetadi

**5. Ma'lumotlarim xavfsizmi?**
- Ha! Faqat sizning serverizngizda
- GitHub'ga yuklanmaydi
- Parol va shaxsiy ma'lumot saqlanmaydi

**6. Serverda qanday ishga tushiraman?**
- README.md'da "Production deployment" bo'limini o'qing
- DigitalOcean yoki AWS ishlatishingiz mumkin

**7. Foydalanuvchilarni qanday ko'raman?**
- `data/users/` papkasida JSON fayllar bor
- `data/analytics/sessions_log.jsonl` da barcha loglar
- `/stats` buyrug'i bilan statistika

## 🛠 Test qilish

Barcha funksiyalarni test qilish uchun:

```bash
python test_bot.py
```

Bu sizga ko'rsatadi:
- ✅ Utils funksiyalari ishlaydi
- ✅ Ma'lumotlar saqlash ishlaydi
- ✅ AI prompt to'g'ri yaratiladi

## 📞 Yordam kerakmi?

- 📧 Email: [sizning emailingiz]
- 💬 Telegram: [sizning telegram]
- 🐛 Muammo topsangiz: GitHub'da Issue oching

## 🎓 Qo'shimcha manbalar

- [Python Telegram Bot dokumentatsiyasi](https://python-telegram-bot.readthedocs.io/)
- [Anthropic Claude dokumentatsiyasi](https://docs.anthropic.com/)
- [Python dasturlash darslari](https://www.python.org/about/gettingstarted/)

## 🎉 Tayyor!

Endi sizning shaxsiy moliyaviy maslahatchi botizngiz tayyor!

Savol-javoblar uchun murojaat qiling. Omad! 🚀

---

**© 2025 - Moliyaviy Tahlil Boti**
