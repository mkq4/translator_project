import json
import os
from datetime import datetime

class TranslationsStorage:
    def __init__(self, file_path='translations.json'):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save_translation(self, source_text, translated_text, source_lang, target_lang):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        translation = {
            'timestamp': timestamp,
            'source_text': source_text,
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        
        translations = self._load_translations()
        translations.insert(0, translation)  # Добавляем новую запись в начало
        self._save_translations(translations)

    def get_translations(self, limit=50):
        translations = self._load_translations()
        return translations[:limit]

    def delete_translation(self, index):
        translations = self._load_translations()
        if 0 <= index < len(translations):
            translations.pop(index)
            self._save_translations(translations)

    def clear_translations(self):
        self._save_translations([])

    def _load_translations(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_translations(self, translations):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2) 