import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
import config
from data_manager import DataManager
from ai_analyzer import AIAnalyzer
import utils

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Holatlar
ANSWERING = 1

# Global obyektlar
data_manager = DataManager()
ai_analyzer = AIAnalyzer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlash /start"""
    user = update.effective_user
    
    # Agar avvalgi sessiya bo'lsa
    if data_manager.is_completed(user.id):
        keyboard = [
            ['🔄 Qaytadan boshlash', '📊 Oxirgi tahlilni ko\'rish']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Siz allaqachon so'rovnomani to'ldirgan ekansiz!\n\n"
            "Nima qilishni xohlaysiz?",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    
    # Yangi foydalanuvchi
    await update.message.reply_text(
        config.TEXTS['welcome'],
        parse_mode='Markdown'
    )
    
    keyboard = [['🚀 Boshlaymiz']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        config.TEXTS['start_survey'],
        reply_markup=reply_markup
    )
    
    return ANSWERING

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """So'rovnomani boshlash"""
    user = update.effective_user
    
    # Foydalanuvchi ma'lumotlarini tozalash (yangi sessiya)
    data_manager.reset_user_data(user.id)
    
    # Birinchi savolni berish
    question_key = config.QUESTION_ORDER[0]
    await ask_question(update, question_key)
    
    return ANSWERING

async def ask_question(update: Update, question_key: str):
    """Savolni berish"""
    question_data = config.QUESTIONS[question_key]
    question_text = question_data['text']
    question_type = question_data['type']
    
    # Progress bar qo'shish
    current_index = config.QUESTION_ORDER.index(question_key)
    progress = utils.create_progress_bar(current_index + 1, len(config.QUESTION_ORDER))
    
    message_text = f"{progress}\n\n{question_text}"
    
    # Savol turiga qarab klaviatura
    if question_type == 'choice':
        keyboard = [[option] for option in question_data['options']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'multi_choice':
        # Inline keyboard (bir nechta tanlov)
        keyboard = []
        for option in question_data['options']:
            keyboard.append([InlineKeyboardButton(f"☐ {option}", callback_data=f"toggle_{option}")])
        keyboard.append([InlineKeyboardButton("✅ Tayyor", callback_data="multi_done")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Context'ga saqlash
        if 'multi_choices' not in update._effective_message._bot_data:
            update._effective_message._bot_data['multi_choices'] = []
        
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'rating':
        keyboard = [
            ['1', '2', '3', '4', '5'],
            ['6', '7', '8', '9', '10']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    else:
        # Oddiy matn yoki raqam
        await update.message.reply_text(
            message_text, 
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown'
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Javobni qayta ishlash"""
    user = update.effective_user
    answer_text = update.message.text
    
    # Agar "Qaytadan boshlash" bosilsa
    if answer_text == '🔄 Qaytadan boshlash':
        data_manager.reset_user_data(user.id)
        return await start_survey(update, context)
    
    # Agar "Oxirgi tahlilni ko'rish" bosilsa
    if answer_text == '📊 Oxirgi tahlilni ko\'rish':
        user_data = data_manager.load_user_data(user.id)
        analysis = user_data.get('ai_analysis')
        
        if analysis:
            chunks = utils.split_text_into_chunks(analysis)
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text("Tahlil topilmadi.")
        
        keyboard = [['/start']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Yangi so'rovnoma uchun /start bosing.",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    
    # Agar "Boshlaymiz" bosilsa
    if answer_text == '🚀 Boshlaymiz':
        return await start_survey(update, context)
    
    # Joriy savolni olish
    question_key = data_manager.get_current_question(user.id)
    
    if not question_key:
        await update.message.reply_text("Xatolik yuz berdi. /start bosing.")
        return ConversationHandler.END
    
    question_data = config.QUESTIONS[question_key]
    question_type = question_data['type']
    
    # Javobni validatsiya qilish
    validated_answer = validate_answer(answer_text, question_type)
    
    if validated_answer is None and question_type in ['number', 'rating']:
        await update.message.reply_text(
            "❌ Iltimos, to'g'ri formatda kiriting.\n\n" + question_data['text'],
            parse_mode='Markdown'
        )
        return ANSWERING
    
    # Javobni saqlash
    user_info = {
        'username': user.username,
        'first_name': user.first_name,
        'language_code': user.language_code
    }
    
    data_manager.save_answer(user.id, question_key, validated_answer or answer_text, user_info)
    
    # Keyingi savolga o'tish yoki tahlil
    if data_manager.is_completed(user.id):
        await show_completion(update, user.id)
        return ConversationHandler.END
    else:
        next_question = data_manager.get_current_question(user.id)
        await ask_question(update, next_question)
        return ANSWERING

def validate_answer(answer: str, question_type: str):
    """Javobni validatsiya qilish"""
    if question_type == 'number':
        return utils.parse_number(answer)
    elif question_type == 'rating':
        return utils.validate_rating(answer)
    else:
        return utils.clean_text(answer)

async def handle_multi_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ko'p tanlovli savollar uchun"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    data = query.data
    
    if 'multi_choices' not in context.bot_data:
        context.bot_data['multi_choices'] = {}
    
    if user.id not in context.bot_data['multi_choices']:
        context.bot_data['multi_choices'][user.id] = []
    
    if data.startswith('toggle_'):
        option = data.replace('toggle_', '')
        
        # Toggle
        if option in context.bot_data['multi_choices'][user.id]:
            context.bot_data['multi_choices'][user.id].remove(option)
        else:
            context.bot_data['multi_choices'][user.id].append(option)
        
        # Klaviaturani yangilash
        question_key = data_manager.get_current_question(user.id)
        question_data = config.QUESTIONS[question_key]
        
        keyboard = []
        for opt in question_data['options']:
            check = "☑" if opt in context.bot_data['multi_choices'][user.id] else "☐"
            keyboard.append([InlineKeyboardButton(f"{check} {opt}", callback_data=f"toggle_{opt}")])
        keyboard.append([InlineKeyboardButton("✅ Tayyor", callback_data="multi_done")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    
    elif data == 'multi_done':
        selected = context.bot_data['multi_choices'].get(user.id, [])
        
        if not selected:
            await query.message.reply_text("⚠️ Kamida bitta variant tanlang!")
            return ANSWERING
        
        # Javobni saqlash
        question_key = data_manager.get_current_question(user.id)
        answer = ", ".join(selected)
        
        user_info = {
            'username': user.effective_user.username,
            'first_name': user.effective_user.first_name,
            'language_code': user.effective_user.language_code
        }
        
        data_manager.save_answer(user.id, question_key, answer, user_info)
        
        # Tozalash
        context.bot_data['multi_choices'][user.id] = []
        
        # Keyingi savol yoki tahlil
        if data_manager.is_completed(user.id):
            await show_completion_callback(query, user.id)
            return ConversationHandler.END
        else:
            next_question = data_manager.get_current_question(user.id)
            
            # Yangi savol uchun oddiy xabar
            question_data = config.QUESTIONS[next_question]
            question_text = question_data['text']
            
            current_index = config.QUESTION_ORDER.index(next_question)
            progress = utils.create_progress_bar(current_index + 1, len(config.QUESTION_ORDER))
            
            await query.message.reply_text(
                f"{progress}\n\n{question_text}",
                parse_mode='Markdown'
            )
            
            return ANSWERING

async def show_completion(update: Update, user_id: int):
    """So'rovnoma tugagach AI tahlil ko'rsatish"""
    await update.message.reply_text(config.TEXTS['all_complete'])
    
    # AI tahlil
    user_data = data_manager.load_user_data(user_id)
    
    try:
        analysis = ai_analyzer.analyze_financial_data(user_data)
        
        # Tahlilni saqlash
        data_manager.save_ai_analysis(user_id, analysis)
        
        # Tahlilni yuborish (bo'laklarga bo'lib)
        chunks = utils.split_text_into_chunks(analysis)
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                await update.message.reply_text(
                    "🤖 **SIZNING SHAXSIY MOLIYAVIY TAHLILIZNGIZ:**\n\n" + chunk,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        
        # Yakuniy xabar
        await update.message.reply_text(
            "✅ Tahliz tugadi!\n\n"
            "Yana yangi tahlil olish uchun /start bosing.",
            reply_markup=ReplyKeyboardRemove()
        )
        
    except Exception as e:
        logger.error(f"AI tahlil xatosi: {e}")
        await update.message.reply_text(
            "❌ Tahlilni yaratishda xatolik yuz berdi.\n"
            "Iltimos, keyinroq qayta urinib ko'ring yoki /start bosing."
        )

async def show_completion_callback(query, user_id: int):
    """Callback query orqali tugallash"""
    await query.message.reply_text(config.TEXTS['all_complete'])
    
    user_data = data_manager.load_user_data(user_id)
    
    try:
        analysis = ai_analyzer.analyze_financial_data(user_data)
        data_manager.save_ai_analysis(user_id, analysis)
        
        chunks = utils.split_text_into_chunks(analysis)
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                await query.message.reply_text(
                    "🤖 **SIZNING SHAXSIY MOLIYAVIY TAHLILIZNGIZ:**\n\n" + chunk,
                    parse_mode='Markdown'
                )
            else:
                await query.message.reply_text(chunk, parse_mode='Markdown')
        
        await query.message.reply_text(
            "✅ Tahliz tugadi!\n\n"
            "Yana yangi tahlil olish uchun /start bosing.",
            reply_markup=ReplyKeyboardRemove()
        )
        
    except Exception as e:
        logger.error(f"AI tahlil xatosi: {e}")
        await query.message.reply_text(
            "❌ Tahlilni yaratishda xatolik yuz berdi.\n"
            "Iltimos, keyinroq qayta urinib ko'ring yoki /start bosing."
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bekor qilish"""
    await update.message.reply_text(
        "So'rovnoma bekor qilindi. Qayta boshlash uchun /start bosing.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    help_text = """
🤖 **Moliyaviy Tahlil Boti**

Bu bot sizning moliyaviy holatizngizni tahlil qiladi va shaxsiy tavsiyalar beradi.

**Buyruqlar:**
/start - Botni boshlash
/help - Yordam
/cancel - So'rovnomani bekor qilish

**Qanday ishlaydi?**
1. Bot sizga moliyaviy savolar beradi
2. Siz javob berasiz
3. Oxirida AI tahlil va tavsiyalar olasiz

**Savollar:**
- Daromadingiz haqida
- Xarajatlarizngiz haqida
- Jamg'arma va qarzlaringiz
- Maqsad va rejalaringiz

Tayyor bo'lsangiz /start bosing! 🚀
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistika (admin uchun)"""
    stats = data_manager.get_user_stats()
    
    stats_text = f"""
📊 **Bot Statistikasi**

👥 Jami foydalanuvchilar: {stats['total_users']}
✅ To'ldirilgan: {stats['completed_surveys']}
⏳ Jarayonda: {stats['in_progress']}
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

def main():
    """Botni ishga tushirish"""
    
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        print("📝 .env faylida TELEGRAM_BOT_TOKEN ni kiriting")
        return
    
    if not config.ANTHROPIC_API_KEY:
        print("⚠️ ANTHROPIC_API_KEY topilmadi!")
        print("📝 .env faylida ANTHROPIC_API_KEY ni kiriting")
        print("🔗 https://console.anthropic.com dan API key oling")
        return
    
    # Bot yaratish
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ANSWERING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer),
                CallbackQueryHandler(handle_multi_choice),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Handlerlarni qo'shish
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('stats', stats_command))
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi!")
    print("📊 Foydalanuvchilar bilan suhbatlashishni boshlang...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()