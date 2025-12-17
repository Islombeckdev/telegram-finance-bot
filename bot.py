import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
import config
from data_manager import DataManager
from ai_analyzer import AIAnalyzer
import utils

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States
ANSWERING = 1

# Global objects
data_manager = DataManager()
ai_analyzer = AIAnalyzer()

# User language storage (default: uz)
user_languages = {}

def get_user_lang(user_id):
    """Get user's language (default: uz)"""
    return user_languages.get(user_id, 'uz')

def get_text(user_id, key):
    """Get text in user's language"""
    lang = get_user_lang(user_id)
    return config.TEXTS.get(lang, config.TEXTS['uz']).get(key, '')

def get_question(user_id, question_key):
    """Get question in user's language"""
    lang = get_user_lang(user_id)
    return config.QUESTIONS.get(lang, config.QUESTIONS['uz']).get(question_key, {})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot start /start"""
    user = update.effective_user
    
    # Check if user already completed
    if data_manager.is_completed(user.id):
        keyboard = [['📊 Yangi tahlil qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Siz allaqachon so'rovnomani to'ldirgan ekansiz!\n\n"
            "Yangi tahlil qilish uchun tugmani bosing.",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    
    # Welcome message
    await update.message.reply_text(
        get_text(user.id, 'welcome'),
        parse_mode='Markdown'
    )
    
    # Start button
    keyboard = [['🚀 Boshlaymiz']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        get_text(user.id, 'start_survey'),
        reply_markup=reply_markup
    )
    
    return ANSWERING

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start survey"""
    user = update.effective_user
    
    # Reset user data
    data_manager.reset_user_data(user.id)
    
    # Ask first question
    question_key = config.QUESTION_ORDER[0]
    await ask_question(update, user.id, question_key, context)
    
    return ANSWERING

async def ask_question(update: Update, user_id: int, question_key: str, context: ContextTypes.DEFAULT_TYPE = None):
    """Ask a question based on type"""
    question_data = get_question(user_id, question_key)
    question_text = question_data['text']
    question_type = question_data['type']
    
    # Progress indicator
    current_index = config.QUESTION_ORDER.index(question_key)
    total = len(config.QUESTION_ORDER)
    progress = f"[{current_index + 1}/{total}]"
    
    message_text = f"{progress}\n\n{question_text}"
    
    # Initialize multi_selected if needed
    if context and question_type == 'inline_multi_choice':
        if 'multi_selected' not in context.user_data:
            context.user_data['multi_selected'] = []
    
    # Create appropriate keyboard based on type
    if question_type == 'inline_choice':
        # Single choice inline keyboard
        keyboard = []
        for option in question_data['options']:
            keyboard.append([InlineKeyboardButton(option, callback_data=f"choice_{question_key}_{option}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'inline_multi_choice':
        # Multiple choice inline keyboard
        keyboard = []
        selected = context.user_data.get('multi_selected', []) if context else []
        for option in question_data['options']:
            check = "✅ " if option in selected else ""
            keyboard.append([InlineKeyboardButton(f"{check}{option}", callback_data=f"multi_{question_key}_{option}")])
        keyboard.append([InlineKeyboardButton("➡️ Keyingisi", callback_data=f"multi_done_{question_key}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'inline_rating':
        # Rating 1-10
        keyboard = [
            [InlineKeyboardButton(str(i), callback_data=f"rating_{question_key}_{i}") for i in range(1, 6)],
            [InlineKeyboardButton(str(i), callback_data=f"rating_{question_key}_{i}") for i in range(6, 11)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'currency' or question_type == 'number':
        # Text input required
        await update.message.reply_text(
            message_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown'
        )
    
    else:
        # Default: text input
        await update.message.reply_text(
            message_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown'
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    data = query.data
    
    # Parse callback data
    if data.startswith('choice_'):
        # Single choice
        parts = data.split('_', 2)
        question_key = parts[1]
        answer = parts[2]
        
        # Save answer
        await save_and_continue(query, user.id, question_key, answer)
    
    elif data.startswith('multi_'):
        # Multiple choice
        if data.startswith('multi_done_'):
            # User finished selecting
            question_key = data.replace('multi_done_', '')
            selected = context.user_data.get('multi_selected', [])
            answer = ', '.join(selected) if selected else 'Hech narsa'
            
            # Clear selection
            context.user_data['multi_selected'] = []
            
            # Save and continue
            await save_and_continue(query, user.id, question_key, answer)
        else:
            # Toggle selection
            parts = data.split('_', 2)
            question_key = parts[1]
            option = parts[2]
            
            if 'multi_selected' not in context.user_data:
                context.user_data['multi_selected'] = []
            
            if option in context.user_data['multi_selected']:
                context.user_data['multi_selected'].remove(option)
            else:
                context.user_data['multi_selected'].append(option)
            
            # Update keyboard
            question_data = get_question(user.id, question_key)
            keyboard = []
            for opt in question_data['options']:
                check = "✅ " if opt in context.user_data['multi_selected'] else ""
                keyboard.append([InlineKeyboardButton(f"{check}{opt}", callback_data=f"multi_{question_key}_{opt}")])
            keyboard.append([InlineKeyboardButton("➡️ Keyingisi", callback_data=f"multi_done_{question_key}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
    
    elif data.startswith('rating_'):
        # Rating selection
        parts = data.split('_')
        question_key = parts[1]
        rating = parts[2]
        
        await save_and_continue(query, user.id, question_key, rating)

async def save_and_continue(query_or_update, user_id: int, question_key: str, answer: str):
    """Save answer and move to next question"""
    # Save answer
    user_info = {
        'username': query_or_update.from_user.username if hasattr(query_or_update, 'from_user') else None,
        'first_name': query_or_update.from_user.first_name if hasattr(query_or_update, 'from_user') else None,
    }
    
    data_manager.save_answer(user_id, question_key, answer, user_info)
    
    # Check if completed
    if data_manager.is_completed(user_id):
        await show_completion(query_or_update, user_id)
        return ConversationHandler.END
    else:
        # Get next question
        next_question = data_manager.get_current_question(user_id)
        
        # Skip conditional questions
        next_question = skip_conditional_questions(user_id, next_question)
        
        if next_question:
            # Send next question as new message (not edit)
            if hasattr(query_or_update, 'message'):
                # It's a callback query
                await ask_question_callback(query_or_update, user_id, next_question)
            else:
                # It's a regular update
                await ask_question(query_or_update, user_id, next_question)
        else:
            # All done
            await show_completion(query_or_update, user_id)
            return ConversationHandler.END

async def ask_question_callback(query, user_id: int, question_key: str):
    """Ask question after callback (as new message)"""
    question_data = get_question(user_id, question_key)
    question_text = question_data['text']
    question_type = question_data['type']
    
    # Progress
    current_index = config.QUESTION_ORDER.index(question_key)
    total = len(config.QUESTION_ORDER)
    progress = f"[{current_index + 1}/{total}]"
    
    message_text = f"{progress}\n\n{question_text}"
    
    # Send as new message
    if question_type == 'inline_choice':
        keyboard = []
        for option in question_data['options']:
            keyboard.append([InlineKeyboardButton(option, callback_data=f"choice_{question_key}_{option}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'inline_multi_choice':
        keyboard = []
        for option in question_data['options']:
            keyboard.append([InlineKeyboardButton(option, callback_data=f"multi_{question_key}_{option}")])
        keyboard.append([InlineKeyboardButton("➡️ Keyingisi", callback_data=f"multi_done_{question_key}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif question_type == 'inline_rating':
        keyboard = [
            [InlineKeyboardButton(str(i), callback_data=f"rating_{question_key}_{i}") for i in range(1, 6)],
            [InlineKeyboardButton(str(i), callback_data=f"rating_{question_key}_{i}") for i in range(6, 11)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    else:
        await query.message.reply_text(message_text, parse_mode='Markdown')

def skip_conditional_questions(user_id: int, question_key: str) -> str:
    """Skip conditional questions based on previous answers"""
    answers = data_manager.get_all_answers(user_id)
    
    # Skip savings_amount if no savings
    if question_key == 'savings_amount':
        has_savings = answers.get('has_savings', '')
        if '❌' in has_savings or 'Yo\'q' in has_savings:
            # Skip this question
            current_idx = config.QUESTION_ORDER.index(question_key)
            if current_idx + 1 < len(config.QUESTION_ORDER):
                return skip_conditional_questions(user_id, config.QUESTION_ORDER[current_idx + 1])
            return None
    
    # Skip debt questions if no debt
    if question_key in ['debt_monthly', 'debt_months']:
        debt_status = answers.get('debt_status', '')
        if '❌' in debt_status or 'Yo\'q' in debt_status:
            current_idx = config.QUESTION_ORDER.index(question_key)
            if current_idx + 1 < len(config.QUESTION_ORDER):
                return skip_conditional_questions(user_id, config.QUESTION_ORDER[current_idx + 1])
            return None
    
    return question_key

async def handle_text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text input answers"""
    user = update.effective_user
    answer_text = update.message.text
    
    # Special buttons
    if answer_text == '📊 Yangi tahlil qilish':
        data_manager.reset_user_data(user.id)
        return await start_survey(update, context)
    
    if answer_text == '🚀 Boshlaymiz':
        return await start_survey(update, context)
    
    if answer_text == '🔄 Qayta hisoblash':
        data_manager.reset_user_data(user.id)
        return await start_survey(update, context)
    
    if answer_text == '📅 2026 uchun reja':
        await update.message.reply_text(
            "🎯 2026 yil uchun reja funksiyasi tez orada qo'shiladi!\n\n"
            "Hozircha /start bilan yangi tahlil qilishingiz mumkin."
        )
        return ANSWERING
    
    # Get current question
    question_key = data_manager.get_current_question(user.id)
    
    if not question_key:
        await update.message.reply_text(get_text(user.id, 'error'))
        return ConversationHandler.END
    
    # Skip conditional questions
    question_key = skip_conditional_questions(user.id, question_key)
    
    if not question_key:
        await show_completion(update, user.id)
        return ConversationHandler.END
    
    question_data = get_question(user.id, question_key)
    question_type = question_data['type']
    
    # Validate based on type
    validated_answer = None
    
    if question_type == 'currency':
        validated_answer = utils.parse_currency(answer_text)
        if validated_answer is None:
            await update.message.reply_text(get_text(user.id, 'number_required'))
            return ANSWERING
    
    elif question_type == 'number':
        try:
            validated_answer = int(answer_text.strip())
        except:
            await update.message.reply_text("⚠️ Iltimos, raqam kiriting (masalan: 12)")
            return ANSWERING
    
    else:
        validated_answer = answer_text.strip()
    
    # Save answer
    user_info = {
        'username': user.username,
        'first_name': user.first_name,
    }
    
    data_manager.save_answer(user.id, question_key, str(validated_answer), user_info)
    
    # Check if completed
    if data_manager.is_completed(user.id):
        await show_completion(update, user.id)
        return ConversationHandler.END
    else:
        next_question = data_manager.get_current_question(user.id)
        next_question = skip_conditional_questions(user.id, next_question)
        
        if next_question:
            await ask_question(update, user.id, next_question, context)
            return ANSWERING
        else:
            await show_completion(update, user.id)
            return ConversationHandler.END

async def show_completion(update_or_query, user_id: int):
    """Show AI analysis after completion"""
    # Send waiting message
    message = update_or_query.message if hasattr(update_or_query, 'message') else update_or_query
    
    await message.reply_text(get_text(user_id, 'all_complete'))
    
    # Get user data
    user_data = data_manager.load_user_data(user_id)
    
    try:
        # Generate AI analysis
        analysis = ai_analyzer.analyze_financial_data(user_data)
        
        # Save analysis
        data_manager.save_ai_analysis(user_id, analysis)
        
        # Send analysis in chunks
        chunks = utils.split_text_into_chunks(analysis)
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                await message.reply_text(
                    "🤖 **SIZNING MOLIYAVIY TAHLILIZNGIZ:**\n\n" + chunk,
                    parse_mode='Markdown'
                )
            else:
                await message.reply_text(chunk, parse_mode='Markdown')
        
        # Final buttons
        keyboard = [config.FINAL_BUTTONS['uz']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await message.reply_text(
            get_text(user_id, 'final_buttons'),
            reply_markup=reply_markup
        )
        
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        await message.reply_text(get_text(user_id, 'error'))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text(
        "So'rovnoma bekor qilindi. Qayta boshlash uchun /start bosing.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
🤖 **Moliyaviy Tahlil Boti**

✅ 14 ta oddiy savol
✅ AI tahlil va tavsiyalar
✅ Dollar qo'llab-quvvatlash
✅ Inline tugmalar

**Buyruqlar:**
/start - Boshlash
/help - Yordam
/cancel - Bekor qilish

Tayyor bo'lsangiz /start bosing! 🚀
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot"""
    
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    if not config.ANTHROPIC_API_KEY:
        print("⚠️ ANTHROPIC_API_KEY topilmadi!")
        return
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ANSWERING: [
                CallbackQueryHandler(handle_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_answer),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Start bot
    print("🤖 Bot ishga tushdi!")
    print("📊 Foydalanuvchilar bilan suhbatlashishni boshlang...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()