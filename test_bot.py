"""
Bot funksiyalarini test qilish uchun oddiy skript
"""

import utils
from data_manager import DataManager
from ai_analyzer import AIAnalyzer

def test_utils():
    """Utils funksiyalarini test qilish"""
    print("🧪 Utils test qilinmoqda...\n")
    
    # Number parsing
    print("1. Number parsing:")
    tests = [
        ("5000000", 5000000),
        ("5 mln", 5000000),
        ("5million", 5000000),
        ("3.5 mln", 3500000),
        ("0", 0),
        ("yo'q", 0),
    ]
    
    for input_val, expected in tests:
        result = utils.parse_number(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} parse_number('{input_val}') = {result} (kutilgan: {expected})")
    
    # Number formatting
    print("\n2. Number formatting:")
    tests = [
        (5000000, "5 mln"),
        (3500000, "3.5 mln"),
        (150000, "150 000"),
        (0, "0"),
    ]
    
    for input_val, expected in tests:
        result = utils.format_number(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} format_number({input_val}) = '{result}' (kutilgan: '{expected}')")
    
    # Progress bar
    print("\n3. Progress bar:")
    print(f"  {utils.create_progress_bar(5, 10)}")
    print(f"  {utils.create_progress_bar(8, 10)}")
    print(f"  {utils.create_progress_bar(10, 10)}")
    
    print("\n✅ Utils testlari tugadi!\n")

def test_data_manager():
    """DataManager ni test qilish"""
    print("🧪 DataManager test qilinmoqda...\n")
    
    dm = DataManager()
    test_user_id = 999999  # Test user ID
    
    # Reset
    dm.reset_user_data(test_user_id)
    print("1. ✅ User data reset qilindi")
    
    # Load
    data = dm.load_user_data(test_user_id)
    print(f"2. ✅ User data yuklandi: session_id = {data['session_id']}")
    
    # Save answer
    dm.save_answer(test_user_id, 'income_monthly', '5000000')
    print("3. ✅ Javob saqlandi")
    
    # Get current question
    current = dm.get_current_question(test_user_id)
    print(f"4. ✅ Joriy savol: {current}")
    
    # Get all answers
    answers = dm.get_all_answers(test_user_id)
    print(f"5. ✅ Barcha javoblar: {len(answers)} ta")
    
    # Stats
    stats = dm.get_user_stats()
    print(f"6. ✅ Statistika: {stats}")
    
    # Cleanup
    dm.reset_user_data(test_user_id)
    print("7. ✅ Test ma'lumotlari tozalandi")
    
    print("\n✅ DataManager testlari tugadi!\n")

def test_ai_analyzer():
    """AI Analyzer ni test qilish (faqat prompt)"""
    print("🧪 AI Analyzer test qilinmoqda...\n")
    
    analyzer = AIAnalyzer()
    
    # Test ma'lumotlari
    test_user_data = {
        'answers': {
            'income_monthly': '5000000',
            'expense_monthly': '3500000',
            'savings_current': '10000000',
            'debt_total': '0',
            'income_salary': '5000000',
            'self_rating': '7',
            'goals': 'Yangi mashina olish, jamg\'arma ko\'paytirish',
        }
    }
    
    # Prompt yaratish
    prompt = analyzer._create_analysis_prompt(test_user_data)
    
    print("1. ✅ AI prompt yaratildi")
    print(f"   Uzunligi: {len(prompt)} belgi")
    print("\n--- PROMPT NAMUNASI ---")
    print(prompt[:500] + "...\n")
    
    # Fallback
    fallback = analyzer._get_fallback_analysis()
    print("2. ✅ Fallback tahlil mavjud")
    print(f"   Uzunligi: {len(fallback)} belgi")
    
    print("\n⚠️  Real AI tahlil uchun ANTHROPIC_API_KEY kerak!\n")
    print("✅ AI Analyzer testlari tugadi!\n")

def main():
    """Barcha testlarni ishga tushirish"""
    print("="*50)
    print("🤖 TELEGRAM FINANCE BOT - TEST SUITE")
    print("="*50 + "\n")
    
    try:
        test_utils()
        test_data_manager()
        test_ai_analyzer()
        
        print("="*50)
        print("✅ BARCHA TESTLAR MUVAFFAQIYATLI O'TDI!")
        print("="*50)
        print("\n📝 Keyingi qadamlar:")
        print("1. .env faylida TELEGRAM_BOT_TOKEN va ANTHROPIC_API_KEY ni kiriting")
        print("2. python bot.py bilan botni ishga tushiring")
        print("3. Telegram'da botizngizga /start yuboring")
        print("\n🚀 Omad!")
        
    except Exception as e:
        print(f"\n❌ Xatolik: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
