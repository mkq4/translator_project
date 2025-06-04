# services/translate.py

from PySide6.QtCore import QThread, Signal
from deep_translator import GoogleTranslator

class TranslatorThread(QThread):
    """
    QThread: переводит текст в фоне и по завершении выдаёт сигнал finished(translated_text, exception).
    """
    finished = Signal(str, Exception)

    def __init__(self, text, source_lang, target_lang):
        super().__init__()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang

    def run(self):
        try:
            if not self.text.strip():
                self.finished.emit("", None)
                return
            print(self.text)
            translator = GoogleTranslator(
                source=self.source_lang,
                target=self.target_lang
            )
            translated = translator.translate(self.text)
            self.finished.emit(translated, None)

        except Exception as e:
            self.finished.emit("", e)
