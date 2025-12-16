import anthropic
from typing import Dict, Any
import config
import utils

class AIAnalyzer:
    """Claude AI yordamida moliyaviy tahlil"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    def analyze_financial_data(self, user_data: Dict[str, Any]) -> str:
        """
        Foydalanuvchi ma'lumotlarini tahlil qilish va tavsiyalar berish
        """
        # Ma'lumotlarni strukturalash
        analysis_prompt = self._create_analysis_prompt(user_data)
        
        try:
            # Claude API ga so'rov
            message = self.client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )
            
            # Javobni olish
            analysis = message.content[0].text
            return analysis
            
        except Exception as e:
            print(f"AI tahlil xatosi: {e}")
            return self._get_fallback_analysis()
    
    def _create_analysis_prompt(self, user_data: Dict[str, Any]) -> str:
        """
        Claude uchun prompt tayyorlash
        """
        answers = user_data.get('answers', {})
        
        # Asosiy ko'rsatkichlarni hisoblash
        income_monthly = utils.parse_number(str(answers.get('income_monthly', 0))) or 0
        expense_monthly = utils.parse_number(str(answers.get('expense_monthly', 0))) or 0
        savings = utils.parse_number(str(answers.get('savings_current', 0))) or 0
        debt_total = utils.parse_number(str(answers.get('debt_total', 0))) or 0
        
        # Daromad tarkibi
        income_salary = utils.parse_number(str(answers.get('income_salary', 0))) or 0
        income_freelance = utils.parse_number(str(answers.get('income_freelance', 0))) or 0
        income_business = utils.parse_number(str(answers.get('income_business', 0))) or 0
        income_investment = utils.parse_number(str(answers.get('income_investment', 0))) or 0
        
        # Xarajat tarkibi
        expense_housing = utils.parse_number(str(answers.get('expense_housing', 0))) or 0
        expense_food = utils.parse_number(str(answers.get('expense_food', 0))) or 0
        expense_entertainment = utils.parse_number(str(answers.get('expense_entertainment', 0))) or 0
        
        # Ko'rsatkichlar
        savings_rate = utils.safe_divide((income_monthly - expense_monthly), income_monthly) * 100
        debt_to_income = utils.safe_divide(debt_total, income_monthly * 12) * 100
        
        prompt = f"""
Sen moliyaviy maslahatchi sifatida ishlamoqdasizsan. O'zbekistonda yashovchi odamning moliyaviy holatini tahlil qiling va shaxsiy tavsiyalar bering.

📊 MOLIYAVIY MA'LUMOTLAR:

**Daromad:**
- Oylik daromad: {utils.format_number(income_monthly)} so'm
  - Ish haqi: {utils.format_number(income_salary)} so'm
  - Frilans: {utils.format_number(income_freelance)} so'm
  - Biznes: {utils.format_number(income_business)} so'm
  - Investitsiya: {utils.format_number(income_investment)} so'm
- Daromad dinamikasi: {answers.get('income_trend', 'ma\'lumot yo\'q')}

**Xarajatlar:**
- Oylik xarajat: {utils.format_number(expense_monthly)} so'm
  - Uy-joy: {utils.format_number(expense_housing)} so'm
  - Ovqat: {utils.format_number(expense_food)} so'm
  - Ko'ngilochar: {utils.format_number(expense_entertainment)} so'm
- Eng ko'p xarajat: {answers.get('expense_top3', 'ma\'lumot yo\'q')}
- Keraksiz xarajatlar: {answers.get('expense_unnecessary', 'ma\'lumot yo\'q')}

**Jamg'arma va aktivlar:**
- Hozirgi jamg'arma: {utils.format_number(savings)} so'm
- Zaxira fondi: {answers.get('emergency_fund', 'ma\'lumot yo\'q')}

**Qarzlar:**
- Umumiy qarz: {utils.format_number(debt_total)} so'm
- Qarz hissi: {answers.get('debt_feeling', 'ma\'lumot yo\'q')}

**O'z-o'zini baholash:**
- Moliyaviy holat bahosi: {answers.get('self_rating', 'ma\'lumot yo\'q')}/10
- Eng katta xato: {answers.get('biggest_mistake', 'ma\'lumot yo\'q')}
- Eng to'g'ri qaror: {answers.get('best_decision', 'ma\'lumot yo\'q')}

**Maqsadlar va rejalar:**
- 2025-yil maqsadlari: {answers.get('goals', 'ma\'lumot yo\'q')}
- Rejalashtirilgan harakatlar: {answers.get('actions', 'ma\'lumot yo\'q')}

📈 HISOBLANGAN KO'RSATKICHLAR:
- Jamg'arish darajasi: {savings_rate:.1f}%
- Qarz/daromad nisbati: {debt_to_income:.1f}%
- Oylik sof oqim: {utils.format_number(income_monthly - expense_monthly)} so'm

---

Iltimos, quyidagi formatda tahlil va tavsiyalar bering:

🎯 **ASOSIY XULOSALAR** (3-4 ta asosiy fikr)

⚠️ **DIQQAT QILISH KERAK BO'LGAN MASALALAR** (eng muhim 3 ta)

💡 **MOLIYAVIY MASLAHATLAR** (konkret va amaliy 5 ta tavsiya)

📈 **O'SISH IMKONIYATLARI** (daromadni oshirish va xarajatni kamaytirish yo'llari)

🎁 **AY TAVSIYASI** (bir oylik konkret harakat rejasi)

🌟 **UMUMIY XULOSA** (rag'batlantiruvchi va motivatsion)

MUHIM TALABLAR:
- O'zbekiston realiyatlariga mos bo'lsin (narxlar, ish bozori, madaniyat)
- Konkret raqamlar va misollar bilan
- Oddiy va tushunarli til
- Ijobiy va rag'batlantiruvchi ohang
- Amaliy va bajarish mumkin bo'lgan tavsiyalar
- Agar ma'lumot yetarli bo'lmasa, "ma'lumot yo'q" deb belgilangan qismlarni e'tiborga olmang
"""
        
        return prompt
    
    def _get_fallback_analysis(self) -> str:
        """
        Agar AI ishlamasa, standart tahlil
        """
        return """
🎯 **ASOSIY XULOSALAR**

✅ Siz moliyaviy holatizni tushunish uchun muhim qadam tashlayapsiz
✅ Ma'lumotlarni to'plash moliyaviy ongni oshirishning birinchi bosqichi
✅ Rejali yondashish sizga maqsadlarizga erishishga yordam beradi

⚠️ **DIQQAT QILISH KERAK BO'LGAN MASALALAR**

1. Oylik xarajatlarni aniq kuzatib boring
2. Zaxira fondni yarating (3-6 oylik xarajat)
3. Qarzlarni birinchi o'ringa qo'ying

💡 **MOLIYAVIY MASLAHATLAR**

1. **50/30/20 qoidasini qo'llang**: 50% zarur xarajatlar, 30% istaklar, 20% jamg'arma
2. **Har oyda avval jamg'arma**: Daromad kirishi bilanoq 10-20% jamg'armaga qo'ying
3. **Xarajatlarni kategoriyalang**: Har bir xarajatni yozib boring va oxirida tahlil qiling
4. **Keraksiz obunalarni to'xtating**: Foydalanmayotgan servislarni bekor qiling
5. **Qo'shimcha daromad manbalarini o'ylang**: Ko'nikmalaringizni pulga aylantiring

📈 **O'SISH IMKONIYATLARI**

💰 **Daromad oshirish:**
- Ko'nikmalaringizni rivojlantiring
- Frilans loyihalar qiling
- Online kurslar o'rganing

💸 **Xarajat kamaytirish:**
- Uy-da taom tayyorlang (kafe o'rniga)
- Ommaviy transportdan foydalaning
- Chegirmalar va aksiyalarni kuzatib boring

🎁 **AY TAVSIYASI**

**1-hafta**: Barcha xarajatlarni yozib boshlang (Excel yoki ilova)
**2-hafta**: Eng katta 3 ta xarajat kategoriyasini tahlil qiling
**3-hafta**: Har bir kategoriyada 10% qisqartirish rejasini tuzing
**4-hafta**: Qoldirilgan pulni jamg'armaga o'tkazing

🌟 **UMUMIY XULOSA**

Moliyaviy erkinlik - bu jarayon, natija emas. Siz bugun birinchi qadamni tashlayapsiz va bu juda muhim! 

Har bir kichik qadam sizni maqsadingizga yaqinlashtiradi. Sabr va izchillik bilan harakat qiling.

Esda tuting: "Pulni boshqarish - hayotni boshqarishdir. Kichik nazorat → katta hotirjamlik."

🚀 Omad tilaymiz! Siz albatta muvaffaq bo'lasiz!
"""
    
    def create_summary_text(self, user_data: Dict[str, Any]) -> str:
        """
        Qisqacha xulosani yaratish (AI tahlilsiz)
        """
        answers = user_data.get('answers', {})
        
        income = utils.parse_number(str(answers.get('income_monthly', 0))) or 0
        expense = utils.parse_number(str(answers.get('expense_monthly', 0))) or 0
        savings = utils.parse_number(str(answers.get('savings_current', 0))) or 0
        debt = utils.parse_number(str(answers.get('debt_total', 0))) or 0
        
        summary = f"""
📊 **SIZNING MOLIYAVIY SURATIZNGIZ**

💰 Oylik daromad: {utils.format_currency(income)}
💸 Oylik xarajat: {utils.format_currency(expense)}
💵 Oylik sof oqim: {utils.format_currency(income - expense)}

🏦 Jamg'arma: {utils.format_currency(savings)}
📉 Qarz: {utils.format_currency(debt)}

⭐ O'z-o'zini baholash: {answers.get('self_rating', 'N/A')}/10
🎯 Asosiy maqsad: {answers.get('goals', 'N/A')[:100]}...
"""
        
        return summary
