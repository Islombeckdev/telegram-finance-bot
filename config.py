import os
from dotenv import load_dotenv

load_dotenv()

# Bot sozlamalari
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Ma'lumotlar saqlash yo'llari
DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")
ANALYTICS_DIR = os.path.join(DATA_DIR, "analytics")
SESSIONS_LOG = os.path.join(ANALYTICS_DIR, "sessions_log.jsonl")

# Bot sozlamalari
MAX_MESSAGE_LENGTH = 4096
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 2000

# O'zbekcha matnlar
TEXTS = {
    'welcome': """
🧾 **Mening moliyaviy yilim — 2025**

Assalomu alaykum! Men sizning moliyaviy yilingizni tahlil qilishga yordam beraman.

Bu yerda siz:
✅ O'tgan yildagi daromad va xarajatlaringizni ko'rib chiqasiz
✅ Moliyaviy holatga baho berasiz
✅ Kelgusi yil uchun maqsadlar qo'yasiz
✅ AI dan shaxsiy tavsiyalar olasiz

Boshlash uchun /start bosing!
    """,
    
    'start_survey': """
Yaxshi! Keling, boshlaylik 🚀

Men sizga savol beraman, siz javob berasiz. Oxirida barcha ma'lumotlaringizga asoslangan to'liq tahlil va tavsiyalar olasiz.

Tayyor bo'lsangiz, "Boshlaymiz" tugmasini bosing!
    """,
    
    'section_complete': "✅ Bo'lim to'ldirildi! Keyingisiga o'tamiz...",
    
    'all_complete': """
🎉 Ajoyib! Barcha ma'lumotlar to'ldirildi!

Endi men sizning moliyaviy holatizni tahlil qilyapman va shaxsiy tavsiyalar tayyorlayapman...

⏳ Bir necha soniya kutib turing...
    """,
    
    'error': "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring yoki /start bosing.",
}

# Savollar strukturasi (PDF asosida)
QUESTIONS = {
    # 1️⃣ DAROMAD
    'income_monthly': {
        'text': "1️⃣ **MEN QANCHA PUL TOPDIM?**\n\n📊 O'rtacha oylik daromadingiz qancha? (so'mda)",
        'type': 'number',
        'section': 'daromad'
    },
    'income_salary': {
        'text': "💼 Oylik ish haqi (so'mda):",
        'type': 'number',
        'section': 'daromad'
    },
    'income_freelance': {
        'text': "💻 Qo'shimcha ish / frilans (oyiga, so'mda):",
        'type': 'number',
        'section': 'daromad'
    },
    'income_business': {
        'text': "🏢 Biznes (oyiga, so'mda):",
        'type': 'number',
        'section': 'daromad'
    },
    'income_investment': {
        'text': "📈 Investitsiya (oyiga, so'mda):",
        'type': 'number',
        'section': 'daromad'
    },
    'income_other': {
        'text': "💰 Boshqa daromadlar (oyiga, so'mda):",
        'type': 'number',
        'section': 'daromad'
    },
    'income_trend': {
        'text': "📊 Daromad dinamikasi (2024ga nisbatan):",
        'type': 'choice',
        'options': ['O\'sdi', 'O\'zgarmadi', 'Kamaydi'],
        'section': 'daromad'
    },
    
    # 2️⃣ XARAJATLAR
    'expense_monthly': {
        'text': "2️⃣ **PUL QAYERGA KETDI?**\n\n💸 O'rtacha oylik xarajatlaringiz qancha? (so'mda)",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_housing': {
        'text': "🏠 Yashash xarajatlari (ijara, kommunal, oyiga so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_food': {
        'text': "🍽 Oziq-ovqat (oyiga, so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_transport': {
        'text': "🚗 Transport (oyiga, so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_entertainment': {
        'text': "🎉 Ko'ngilochar / kafelar (oyiga, so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_subscriptions': {
        'text': "📱 Online servislar / obunalar (oyiga, so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_other': {
        'text': "💳 Boshqa xarajatlar (oyiga, so'mda):",
        'type': 'number',
        'section': 'xarajat'
    },
    'expense_top3': {
        'text': "🎯 Eng ko'p pul ketgan TOP-3 yo'nalishni yozing (masalan: kafe, kiyim, transport):",
        'type': 'text',
        'section': 'xarajat'
    },
    'expense_unnecessary': {
        'text': "⚠️ Keraksiz bo'lgan xarajatlar bormi? (bor bo'lsa yozing, yo'q bo'lsa 'yo'q' deb yozing):",
        'type': 'text',
        'section': 'xarajat'
    },
    
    # 3️⃣ XARIDLAR
    'purchases_count': {
        'text': "3️⃣ **MEN NIMALARNI OLDIM?**\n\n🛍 2024-yilda eng muhim 3 ta xaridingiz nima bo'ldi? (har birini alohida yozing, masalan: telefon, mebel)",
        'type': 'text',
        'section': 'xarid'
    },
    'purchases_value': {
        'text': "💵 Bu xaridlarning umumiy qiymati qancha? (taxminan, so'mda):",
        'type': 'number',
        'section': 'xarid'
    },
    'purchases_satisfaction': {
        'text': "😊 Qaysi xaridlar hayotingizni yaxshiladi? Qaysilarini takrorlamasligingizni xohlaysiz?",
        'type': 'text',
        'section': 'xarid'
    },
    
    # 4️⃣ AKTIVLAR
    'savings_current': {
        'text': "4️⃣ **HOZIR MENDA NIMA BOR?**\n\n💰 Hozirgi jamg'armangiz qancha? (taxminan, so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'savings_cash': {
        'text': "💵 Naqd pul (uy/hamyon, so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'savings_bank': {
        'text': "🏦 Bank jamg'armasi (so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'savings_gold': {
        'text': "🪙 Oltin / valyuta (so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'savings_property': {
        'text': "🏡 Uy / mashina (taxminan qiymati, so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'savings_investment': {
        'text': "📊 Investitsiya (aksiyalar, biznes, so'mda):",
        'type': 'number',
        'section': 'aktiv'
    },
    'emergency_fund': {
        'text': "🆘 Zaxira fondingiz necha oylik xarajatga yetadi? (masalan: 3 oy, 6 oy, yo'q):",
        'type': 'text',
        'section': 'aktiv'
    },
    
    # 5️⃣ QARZLAR
    'debt_total': {
        'text': "5️⃣ **QARZLAR BORMI?**\n\n📉 Umumiy qarzingiz qancha? (so'mda, yo'q bo'lsa 0 yozing):",
        'type': 'number',
        'section': 'qarz'
    },
    'debt_bank': {
        'text': "🏦 Bank / Mikroqarz qarzi (so'mda):",
        'type': 'number',
        'section': 'qarz'
    },
    'debt_personal': {
        'text': "👥 Yaqinlar / do'stlardan qarz (so'mda):",
        'type': 'number',
        'section': 'qarz'
    },
    'debt_feeling': {
        'text': "😰 Qarzlar haqida hissiyotlaringiz:",
        'type': 'choice',
        'options': ['Asosan yengillik berdi', 'Asosan bosim qilyapti'],
        'section': 'qarz'
    },
    
    # 6️⃣ O'Z-O'ZINI BAHOLASH
    'self_rating': {
        'text': "6️⃣ **O'ZIMGA HALOL BAHO**\n\n⭐ Moliyaviy holatizga 1 dan 10 gacha baho bering:",
        'type': 'rating',
        'section': 'baho'
    },
    'biggest_mistake': {
        'text': "❌ 2024-yildagi eng katta moliyaviy xatongiz nima bo'ldi?",
        'type': 'text',
        'section': 'baho'
    },
    'best_decision': {
        'text': "✅ 2024-yildagi eng to'g'ri moliyaviy qaroringiz?",
        'type': 'text',
        'section': 'baho'
    },
    
    # 7️⃣ MAQSADLAR
    'goals': {
        'text': "7️⃣ **KELGUSI YIL UCHUN 3 MAQSAD**\n\n🎯 2025-yil uchun 3 ta moliyaviy maqsad yozing (har birini alohida, masalan: 10 mln jamg'armoq):",
        'type': 'text',
        'section': 'maqsad'
    },
    
    # 8️⃣ HARAKATLAR
    'actions': {
        'text': "8️⃣ **MEN ENDI SHULARNI QILAMAN**\n\n✅ Qaysi 3 ta harakatni amalga oshirishni xohlaysiz?",
        'type': 'multi_choice',
        'options': [
            'Xarajatlarni yozib boraman',
            'Jamg\'armani birinchi qilaman',
            'Keraksiz xaridlarni kamaytiraman',
            'Qarzga ehtiyot bo\'laman',
            'Daromadni ko\'paytiraman'
        ],
        'section': 'harakat'
    },
}

# Savol ketma-ketligi
QUESTION_ORDER = [
    # Daromad
    'income_monthly', 'income_salary', 'income_freelance', 'income_business',
    'income_investment', 'income_other', 'income_trend',
    
    # Xarajat
    'expense_monthly', 'expense_housing', 'expense_food', 'expense_transport',
    'expense_entertainment', 'expense_subscriptions', 'expense_other',
    'expense_top3', 'expense_unnecessary',
    
    # Xaridlar
    'purchases_count', 'purchases_value', 'purchases_satisfaction',
    
    # Aktivlar
    'savings_current', 'savings_cash', 'savings_bank', 'savings_gold',
    'savings_property', 'savings_investment', 'emergency_fund',
    
    # Qarzlar
    'debt_total', 'debt_bank', 'debt_personal', 'debt_feeling',
    
    # Baholash
    'self_rating', 'biggest_mistake', 'best_decision',
    
    # Maqsadlar
    'goals',
    
    # Harakatlar
    'actions',
]
