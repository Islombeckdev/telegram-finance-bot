import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import config

class DataManager:
    """Foydalanuvchi ma'lumotlarini boshqarish"""
    
    def __init__(self):
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Kerakli papkalarni yaratish"""
        os.makedirs(config.USERS_DIR, exist_ok=True)
        os.makedirs(config.ANALYTICS_DIR, exist_ok=True)
    
    def get_user_file_path(self, user_id: int) -> str:
        """Foydalanuvchi fayl yo'li"""
        return os.path.join(config.USERS_DIR, f"{user_id}.json")
    
    def load_user_data(self, user_id: int) -> Dict[str, Any]:
        """Foydalanuvchi ma'lumotlarini yuklash"""
        file_path = self.get_user_file_path(user_id)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Yangi foydalanuvchi uchun boshlang'ich struktura
        return {
            'user_id': user_id,
            'started_at': datetime.now().isoformat(),
            'current_question': 0,
            'answers': {},
            'session_id': self._generate_session_id(),
            'completed': False,
            'ai_analysis': None
        }
    
    def save_user_data(self, user_id: int, data: Dict[str, Any]):
        """Foydalanuvchi ma'lumotlarini saqlash"""
        file_path = self.get_user_file_path(user_id)
        data['updated_at'] = datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_answer(self, user_id: int, question_key: str, answer: Any, user_info: Dict = None):
        """Javobni saqlash va log qilish"""
        data = self.load_user_data(user_id)
        data['answers'][question_key] = answer
        
        # Keyingi savolga o'tish
        current_index = config.QUESTION_ORDER.index(question_key)
        if current_index < len(config.QUESTION_ORDER) - 1:
            data['current_question'] = current_index + 1
        else:
            data['completed'] = True
        
        self.save_user_data(user_id, data)
        
        # Analytics log
        self._log_session_event(
            user_id=user_id,
            session_id=data['session_id'],
            question_key=question_key,
            question_text=config.QUESTIONS[question_key]['text'],
            answer=answer,
            user_info=user_info
        )
    
    def save_ai_analysis(self, user_id: int, analysis: str):
        """AI tahlilini saqlash"""
        data = self.load_user_data(user_id)
        data['ai_analysis'] = analysis
        data['analysis_date'] = datetime.now().isoformat()
        self.save_user_data(user_id, data)
        
        # AI tahlilini alohida log qilish
        self._log_ai_analysis(user_id, data['session_id'], analysis)
    
    def _log_session_event(self, user_id: int, session_id: str, 
                          question_key: str, question_text: str, 
                          answer: Any, user_info: Dict = None):
        """Har bir savol-javobni log faylga yozish"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'session_id': session_id,
            'question_key': question_key,
            'question_text': question_text.replace('\n', ' ').strip(),
            'answer': answer,
            'section': config.QUESTIONS[question_key]['section']
        }
        
        if user_info:
            log_entry['user_info'] = {
                'username': user_info.get('username'),
                'first_name': user_info.get('first_name'),
                'language_code': user_info.get('language_code')
            }
        
        # JSONL formatida yozish (har bir qator - alohida JSON)
        with open(config.SESSIONS_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def _log_ai_analysis(self, user_id: int, session_id: str, analysis: str):
        """AI tahlilini log qilish"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'session_id': session_id,
            'event_type': 'ai_analysis',
            'analysis': analysis
        }
        
        with open(config.SESSIONS_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def _generate_session_id(self) -> str:
        """Sessiya ID yaratish"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def get_current_question(self, user_id: int) -> Optional[str]:
        """Joriy savolni olish"""
        data = self.load_user_data(user_id)
        
        if data['completed']:
            return None
        
        question_index = data['current_question']
        if question_index < len(config.QUESTION_ORDER):
            return config.QUESTION_ORDER[question_index]
        
        return None
    
    def reset_user_data(self, user_id: int):
        """Foydalanuvchi ma'lumotlarini tozalash (yangi sessiya)"""
        file_path = self.get_user_file_path(user_id)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def get_all_answers(self, user_id: int) -> Dict[str, Any]:
        """Barcha javoblarni olish"""
        data = self.load_user_data(user_id)
        return data.get('answers', {})
    
    def is_completed(self, user_id: int) -> bool:
        """So'rovnoma to'ldirilganmi?"""
        data = self.load_user_data(user_id)
        return data.get('completed', False)
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Umumiy statistika (CustDev uchun)"""
        user_files = [f for f in os.listdir(config.USERS_DIR) if f.endswith('.json')]
        
        stats = {
            'total_users': len(user_files),
            'completed_surveys': 0,
            'in_progress': 0
        }
        
        for file_name in user_files:
            with open(os.path.join(config.USERS_DIR, file_name), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('completed'):
                    stats['completed_surveys'] += 1
                else:
                    stats['in_progress'] += 1
        
        return stats
    
    def export_analytics(self) -> list:
        """Barcha session loglarini o'qish (tahlil uchun)"""
        if not os.path.exists(config.SESSIONS_LOG):
            return []
        
        logs = []
        with open(config.SESSIONS_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        return logs
