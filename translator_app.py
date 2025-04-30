import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QPushButton,
                             QPlainTextEdit, QStatusBar)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from deep_translator import GoogleTranslator

LANGUAGES = {
    'en': 'English',
    'ru': 'Russian',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'pl': 'Polish',
    'ar': 'Arabic',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese Simplified',
    'zh-tw': 'Chinese Traditional',
    'vi': 'Vietnamese',
    'cs': 'Czech',
    'da': 'Danish',
    'fi': 'Finnish',
    'el': 'Greek',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'ms': 'Malay',
    'no': 'Norwegian',
    'ro': 'Romanian',
    'sk': 'Slovak',
    'sv': 'Swedish',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian'
}

class TranslatorThread(QThread):
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

            translator = GoogleTranslator(
                source=self.source_lang,
                target=self.target_lang
            )
            translated = translator.translate(self.text)
            self.finished.emit(translated if translated else "", None)
        except Exception as e:
            self.finished.emit("", e)

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Переводчик")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем верхнюю панель с выбором языков
        top_panel = QHBoxLayout()
        
        # Комбобокс для выбора исходного языка
        self.source_lang = QComboBox()
        for code, name in LANGUAGES.items():
            self.source_lang.addItem(name, code)
        self.source_lang.setCurrentText(LANGUAGES['en'])
        
        # Кнопка смены языков
        swap_button = QPushButton("⇄")
        swap_button.setFixedWidth(40)
        swap_button.clicked.connect(self.swap_languages)
        
        # Комбобокс для выбора целевого языка
        self.target_lang = QComboBox()
        for code, name in LANGUAGES.items():
            self.target_lang.addItem(name, code)
        self.target_lang.setCurrentText(LANGUAGES['ru'])
        
        top_panel.addWidget(self.source_lang)
        top_panel.addWidget(swap_button)
        top_panel.addWidget(self.target_lang)
        main_layout.addLayout(top_panel)
        
        # Создаем поля для ввода и вывода текста
        self.source_text = QPlainTextEdit()
        self.source_text.setPlaceholderText("Введите текст для перевода...")
        self.source_text.textChanged.connect(self.start_translation_timer)
        
        self.target_text = QPlainTextEdit()
        self.target_text.setPlaceholderText("Перевод появится здесь...")
        self.target_text.setReadOnly(True)
        
        main_layout.addWidget(self.source_text)
        main_layout.addWidget(self.target_text)
        
        # Создаем статусбар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Инициализируем таймер для задержки перевода
        self.translation_timer = QTimer()
        self.translation_timer.setSingleShot(True)
        self.translation_timer.timeout.connect(self.translate_text)
        
        # Инициализируем переменную для хранения текущего потока перевода
        self.current_thread = None

    def swap_languages(self):
        source_idx = self.source_lang.currentIndex()
        target_idx = self.target_lang.currentIndex()
        
        self.source_lang.setCurrentIndex(target_idx)
        self.target_lang.setCurrentIndex(source_idx)
        
        source_text = self.source_text.toPlainText()
        target_text = self.target_text.toPlainText()
        
        if source_text or target_text:
            self.source_text.setPlainText(target_text)
            self.target_text.clear()
            self.translate_text()

    def start_translation_timer(self):
        self.translation_timer.start(1000)  # Задержка 1 секунда

    def translation_finished(self, result, error):
        if error:
            self.statusBar.showMessage(f"Ошибка перевода: {str(error)}", 3000)
        else:
            self.target_text.setPlainText(result)
            self.statusBar.showMessage("Перевод завершен", 3000)
        
        self.current_thread = None

    def translate_text(self):
        text = self.source_text.toPlainText()
        source_lang = self.source_lang.currentData()
        target_lang = self.target_lang.currentData()
        
        if self.current_thread:
            self.current_thread.quit()
        
        self.current_thread = TranslatorThread(text, source_lang, target_lang)
        self.current_thread.finished.connect(self.translation_finished)
        self.current_thread.start()
        
        self.statusBar.showMessage("Выполняется перевод...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec()) 