import re
from typing import Optional, Union

def parse_number(text: str) -> Optional[float]:
    """
    Turli formatdagi raqamlarni parse qilish
    Masalan: "5000000", "5 000 000", "5mln", "5 million"
    """
    if not text:
        return None
    
    # Faqat matnni olib tashlash
    text = text.strip().lower()
    
    # 0 bo'lsa
    if text == '0' or text == 'yo\'q' or text == 'yoq':
        return 0
    
    # Million/mln belgilarini tekshirish
    multiplier = 1
    if 'mln' in text or 'million' in text or 'млн' in text:
        multiplier = 1_000_000
        text = re.sub(r'(mln|million|млн)', '', text)
    elif 'ming' in text or 'k' in text:
        multiplier = 1_000
        text = re.sub(r'(ming|k)', '', text)
    
    # Barcha raqamlarni ajratib olish
    numbers = re.findall(r'\d+[.,]?\d*', text)
    
    if not numbers:
        return None
    
    # Birinchi raqamni olish
    number_str = numbers[0].replace(',', '.')
    
    try:
        number = float(number_str) * multiplier
        return number
    except ValueError:
        return None

def format_number(number: Union[int, float]) -> str:
    """
    Raqamni chiroyli formatda ko'rsatish
    Masalan: 5000000 -> "5 000 000"
    """
    if number is None:
        return "0"
    
    # Million/mingga aylantirish
    if number >= 1_000_000:
        mln = number / 1_000_000
        if mln == int(mln):
            return f"{int(mln)} mln"
        return f"{mln:.1f} mln"
    
    if number >= 1_000:
        # Bo'sh joy bilan
        return f"{int(number):,}".replace(',', ' ')
    
    return str(int(number))

def validate_rating(text: str) -> Optional[int]:
    """
    1-10 oralig'idagi baholashni tekshirish
    """
    try:
        rating = int(text.strip())
        if 1 <= rating <= 10:
            return rating
        return None
    except ValueError:
        return None

def split_text_into_chunks(text: str, max_length: int = 4000) -> list:
    """
    Uzun matnni qismlarga bo'lish (Telegram limit 4096)
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def clean_text(text: str) -> str:
    """
    Matnni tozalash (keraksiz bo'shliqlar, belgilar)
    """
    # Bir nechta bo'shliqlarni bitta qilish
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text: str) -> list:
    """
    Matndan kalit so'zlarni ajratib olish
    """
    # Oddiy implementatsiya - so'zlarni ajratish
    words = re.findall(r'\b\w+\b', text.lower())
    # Stop-words ni olib tashlash (oddiy ro'yxat)
    stop_words = ['va', 'bilan', 'uchun', 'dan', 'ga', 'ni', 'bu', 'o', 'u']
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords

def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """
    Progress bar yaratish
    Masalan: ▓▓▓▓▓▒▒▒▒▒ 50%
    """
    filled = int(length * current / total)
    bar = '▓' * filled + '▒' * (length - filled)
    percentage = int(100 * current / total)
    return f"{bar} {percentage}%"

def format_currency(amount: float, currency: str = "so'm") -> str:
    """
    Pulni formatda ko'rsatish
    """
    formatted = format_number(amount)
    return f"{formatted} {currency}"

def safe_divide(a: float, b: float) -> float:
    """
    Xavfsiz bo'lish (0 ga bo'lishni oldini olish)
    """
    if b == 0:
        return 0
    return a / b

def calculate_percentage(part: float, total: float) -> float:
    """
    Foizni hisoblash
    """
    return safe_divide(part * 100, total)

def parse_list(text: str) -> list:
    """
    Ro'yxatni parse qilish
    Masalan: "kafe, kiyim, transport" -> ["kafe", "kiyim", "transport"]
    """
    # Vergul yoki yangi qatorga bo'lish
    items = re.split(r'[,\n]+', text)
    # Tozalash va bo'sh elementlarni olib tashlash
    items = [item.strip() for item in items if item.strip()]
    return items

def get_emoji_for_category(category: str) -> str:
    """
    Kategoriya uchun emoji qaytarish
    """
    emoji_map = {
        'daromad': '💰',
        'xarajat': '💸',
        'xarid': '🛍',
        'aktiv': '🏦',
        'qarz': '📉',
        'baho': '⭐',
        'maqsad': '🎯',
        'harakat': '✅'
    }
    return emoji_map.get(category.lower(), '📊')
