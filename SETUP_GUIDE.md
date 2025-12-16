# 📖 Qadamma-qadam O'rnatish Yo'riqnomasi

Bu yo'riqnoma sizga botni 0 dan ishga tushirishda yordam beradi.

## ✅ Talab qilinadigan narsalar

- ✅ Kompyuter (Windows/Mac/Linux)
- ✅ Internet aloqa
- ✅ Python 3.8+ o'rnatilgan bo'lishi
- ✅ 10-15 daqiqa vaqt

## 📱 1-QADAM: Telegram Bot Yaratish

### 1.1 BotFather'ga o'ting

1. Telegram'ni oching
2. Qidiruv qismiga `@BotFather` yozing
3. BotFather botini oching
4. `/start` bosing

### 1.2 Yangi bot yaratish

BotFather'ga quyidagi buyruqlarni yuboring:

```
/newbot
```

BotFather sizdan bot nomini so'raydi:

```
Bot nomini kiriting:
Mening Moliyaviy Botim
```

Keyin username so'raydi (tugashi `bot` bilan bo'lishi kerak):

```
Bot username'ini kiriting:
mening_moliya_bot
```

### 1.3 Token olish

BotFather sizga token beradi. Misol:

```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

⚠️ **MUHIM:** Bu tokenni biron kimga bermang! Bu sizning botizngizga kirish kaliti.

📝 Tokenni biror joyga nusxalab qo'ying (notepad, notes)

## 🤖 2-QADAM: Claude API Key Olish

### 2.1 Anthropic'ga ro'yxatdan o'tish

1. Brauzerizngizda [console.anthropic.com](https://console.anthropic.com) oching
2. "Sign Up" bosing
3. Email va parol kiriting
4. Email'ingizni tasdiqlang

### 2.2 API Key yaratish

1. Console'ga kiring
2. Chap tarafda **"API Keys"** ni toping
3. **"Create Key"** tugmasini bosing
4. Key'ga nom bering (masalan: "Finance Bot")
5. **"Create Key"** ni bosing
6. Key ko'rinadi:

```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **MUHIM:** Bu keyni nusxalab oling! Bir marta ko'rinadi!

📝 Keyni biror joyga nusxalab qo'ying (notepad, notes)

### 2.3 Kredit tekshirish

1. Console'da "Settings" → "Billing" ga o'ting
2. Yangi foydalanuvchilar **$5 bepul kredit** oladi
3. Bu ~100-500 tahlil uchun yetadi

## 💻 3-QADAM: Bot Fayllarini Tayyorlash

### 3.1 Fayllarni yuklab olish

Telegram'dan yoki boshqa manbadan bot fayllarini oling.

Fayl strukturasi:

```
telegram-finance-bot/
├── bot.py
├── config.py
├── data_manager.py
├── ai_analyzer.py
├── utils.py
├── requirements.txt
├── .env.example
└── README.md
```

### 3.2 Papkaga o'ting

**Windows (Command Prompt):**
```cmd
cd C:\Users\YourName\telegram-finance-bot
```

**Mac/Linux (Terminal):**
```bash
cd ~/telegram-finance-bot
```

## 🔧 4-QADAM: Python va Kutubxonalarni O'rnatish

### 4.1 Python versiyasini tekshirish

```bash
python --version
```

Yoki:

```bash
python3 --version
```

Python 3.8+ bo'lishi kerak. Agar yo'q bo'lsa:
- Windows: [python.org](https://www.python.org/downloads/) dan yuklab oling
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

### 4.2 Virtual muhit yaratish (ixtiyoriy, lekin tavsiya etiladi)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Virtual muhit faollashganda `(venv)` ko'rinadi.

### 4.3 Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

Bu 1-2 daqiqa davom etadi. Kutib turing...

✅ "Successfully installed..." ko'rinsangiz tayyor!

## 🔐 5-QADAM: .env Faylini Sozlash

### 5.1 .env faylini yaratish

**Windows:**
```cmd
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### 5.2 .env faylini tahrirlash

`.env` faylini matn muharririda oching:
- Windows: Notepad
- Mac: TextEdit
- Linux: nano, vim, gedit

Quyidagi qatorlarni topib, o'z tokenlarizngizni qo'ying:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **E'tibor bering:**
- Qo'shtirnoq (`"`) ishlatmang
- Bo'sh joy qoldirmang
- Tokenlarni to'g'ri nusxalang

### 5.3 Faylni saqlash

- Windows: `Ctrl + S`
- Mac: `Cmd + S`
- Linux: `Ctrl + O` (nano'da)

## ✅ 6-QADAM: Test Qilish

Avval test qiling:

```bash
python test_bot.py
```

Natija:

```
✅ Utils testlari tugadi!
✅ DataManager testlari tugadi!
✅ AI Analyzer testlari tugadi!
✅ BARCHA TESTLAR MUVAFFAQIYATLI O'TDI!
```

Agar barcha testlar o'tsa, botni ishga tushirishga tayyor!

## 🚀 7-QADAM: Botni Ishga Tushirish

```bash
python bot.py
```

Natija:

```
🤖 Bot ishga tushdi!
📊 Foydalanuvchilar bilan suhbatlashishni boshlang...
```

✅ **Bot ishlayapti!**

## 📱 8-QADAM: Botni Test Qilish

1. Telegram'ni oching
2. Qidiruvda o'z botizngizning username'ini yozing (masalan: @mening_moliya_bot)
3. Botni oching
4. `/start` bosing
5. Botdan javob kelishi kerak!

## 🎉 Tayyor!

Sizning botizngiz tayyor! Endi foydalanuvchilar:

1. `/start` bosib so'rovnomani boshlaydi
2. 40 ta savolga javob beradi
3. AI tahlil va tavsiyalar oladi

## 🛑 Botni To'xtatish

Terminal/Command Prompt'da:
- Windows/Mac/Linux: `Ctrl + C`

## 🔄 Botni Qayta Ishga Tushirish

```bash
python bot.py
```

## 📊 Foydalanuvchi Ma'lumotlarini Ko'rish

Ma'lumotlar `data/` papkasida:

```
data/
├── users/
│   ├── 123456789.json  ← Har bir foydalanuvchi
│   └── 987654321.json
└── analytics/
    └── sessions_log.jsonl  ← Barcha loglar
```

JSON fayllarni istalgan matn muharririda ochishingiz mumkin.

## 🐛 Muammolarni Hal Qilish

### Muammo 1: "ModuleNotFoundError"

**Xatolik:**
```
ModuleNotFoundError: No module named 'telegram'
```

**Yechim:**
```bash
pip install -r requirements.txt
```

### Muammo 2: "TELEGRAM_BOT_TOKEN topilmadi"

**Xatolik:**
```
❌ TELEGRAM_BOT_TOKEN topilmadi!
```

**Yechim:**
- `.env` fayli mavjudligini tekshiring
- Tokenni to'g'ri nusxalganingizni tekshiring
- Qo'shtirnoq ishlatmaganingizni tekshiring

### Muammo 3: Bot javob bermayapti

**Tekshiring:**
1. Bot ishlayaptimi? (`python bot.py` bajarilganmi?)
2. Internet bor-mi?
3. Token to'g'ri-mi?
4. BotFather'da botni o'chirib qo'yganmisiz?

### Muammo 4: AI tahlil ishlamayapti

**Xatolik:**
```
❌ Tahlilni yaratishda xatolik
```

**Tekshiring:**
1. ANTHROPIC_API_KEY to'g'ri-mi?
2. API kredit bor-mi? (console.anthropic.com'da tekshiring)
3. Internet tez-mi?

## 💡 Keyingi Qadamlar

### Botni 24/7 Ishlashi Uchun

Serverda ishlatish uchun README.md'dagi "Production Deployment" bo'limini o'qing.

### Savollarni O'zgartirish

`config.py` faylini tahrirlang.

### AI Tahlilni Sozlash

`ai_analyzer.py` faylini tahrirlang.

## 📞 Yordam Kerakmi?

Agar qandaydir muammo bo'lsa:
1. Xatolik xabarini to'liq o'qing
2. Google'da qidiring
3. GitHub'da Issue oching
4. To'g'ridan-to'g'ri murojaat qiling

---

**Omad! Muvaffaqiyatlar! 🚀**
