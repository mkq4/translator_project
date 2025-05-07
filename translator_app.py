import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QPushButton,
                             QPlainTextEdit, QStatusBar, QScrollArea, QLabel,
                             QFrame, QMessageBox, QStackedWidget, QLineEdit,
                             QListWidget)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import tempfile
import os
import sqlite3
from datetime import datetime
import pyperclip

LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ny': 'Nyanja',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tl': 'Tagalog',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
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
        
        # Инициализация pygame для воспроизведения звука
        pygame.mixer.init()
        self.current_audio_file = None
        
        # Инициализация базы данных
        self.init_db()
        
        # Инициализация таймера для задержки перевода
        self.translation_timer = QTimer()
        self.translation_timer.setSingleShot(True)
        self.translation_timer.timeout.connect(self.do_translation)
        
        # Инициализация переменной для хранения текущего потока перевода
        self.current_thread = None
        
        # Создаем стек виджетов для разных экранов
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Создаем основной экран
        self.main_screen = QWidget()
        self.setup_main_screen()
        self.stack.addWidget(self.main_screen)
        
        # Создаем экран истории
        self.history_screen = QWidget()
        self.setup_history_screen()
        self.stack.addWidget(self.history_screen)
        
        # Создаем экран выбора языков
        self.language_screen = QWidget()
        self.setup_language_screen()
        self.stack.addWidget(self.language_screen)
        
        # Показываем главный экран
        self.stack.setCurrentWidget(self.main_screen)

    def init_db(self):
        self.conn = sqlite3.connect('translations.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations
            (timestamp TEXT, source_text TEXT, translated_text TEXT,
             source_lang TEXT, target_lang TEXT)
        ''')
        self.conn.commit()

    def save_translation(self, source_text, translated_text, source_lang, target_lang):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO translations 
            (timestamp, source_text, translated_text, source_lang, target_lang)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, source_text, translated_text, source_lang, target_lang))
        self.conn.commit()

    def setup_main_screen(self):
        # Создаем центральный виджет и главный layout
        main_layout = QVBoxLayout(self.main_screen)
        
        # Создаем верхнюю панель с выбором языков
        top_panel = QHBoxLayout()
        
        # Кнопки выбора языков
        self.source_lang_btn = QPushButton(LANGUAGES['en'])
        self.source_lang_btn.clicked.connect(lambda: self.show_language_selector('source'))
        
        # Кнопка смены языков
        swap_button = QPushButton("⇄")
        swap_button.setFixedWidth(40)
        swap_button.clicked.connect(self.swap_languages)
        
        self.target_lang_btn = QPushButton(LANGUAGES['ru'])
        self.target_lang_btn.clicked.connect(lambda: self.show_language_selector('target'))
        
        top_panel.addWidget(self.source_lang_btn)
        top_panel.addWidget(swap_button)
        top_panel.addWidget(self.target_lang_btn)
        main_layout.addLayout(top_panel)

        # Создаем горизонтальный layout для текстовых полей и кнопок
        text_panel = QHBoxLayout()
        
        # Создаем вертикальный layout для исходного текста и его кнопок
        source_panel = QVBoxLayout()
        self.source_text = QPlainTextEdit()
        self.source_text.setPlaceholderText("Введите текст для перевода...")
        self.source_text.textChanged.connect(self.on_text_changed)
        source_panel.addWidget(self.source_text)
        
        # Кнопки для исходного текста
        source_buttons = QHBoxLayout()
        self.source_speak_btn = QPushButton()
        self.source_speak_btn.setIcon(QIcon("icons/speaker.svg"))
        self.source_speak_btn.clicked.connect(lambda: self.speak_text(
            self.source_text.toPlainText(),
            next(code for code, name in LANGUAGES.items() if name == self.source_lang_btn.text())
        ))
        
        self.source_copy_btn = QPushButton()
        self.source_copy_btn.setIcon(QIcon("icons/copy.svg"))
        self.source_copy_btn.clicked.connect(lambda: self.copy_text(self.source_text.toPlainText()))
        
        self.clear_source_btn = QPushButton()
        self.clear_source_btn.setIcon(QIcon("icons/clear.svg"))
        self.clear_source_btn.clicked.connect(self.clear_source_text)
        
        source_buttons.addWidget(self.source_speak_btn)
        source_buttons.addWidget(self.source_copy_btn)
        source_buttons.addWidget(self.clear_source_btn)
        source_buttons.addStretch()
        source_panel.addLayout(source_buttons)
        
        # Создаем вертикальный layout для целевого текста и его кнопок
        target_panel = QVBoxLayout()
        self.target_text = QPlainTextEdit()
        self.target_text.setPlaceholderText("Перевод появится здесь...")
        self.target_text.setReadOnly(True)
        target_panel.addWidget(self.target_text)
        
        # Кнопки для целевого текста
        target_buttons = QHBoxLayout()
        self.target_speak_btn = QPushButton()
        self.target_speak_btn.setIcon(QIcon("icons/speaker.svg"))
        self.target_speak_btn.clicked.connect(lambda: self.speak_text(
            self.target_text.toPlainText(),
            next(code for code, name in LANGUAGES.items() if name == self.target_lang_btn.text())
        ))
        
        self.target_copy_btn = QPushButton()
        self.target_copy_btn.setIcon(QIcon("icons/copy.svg"))
        self.target_copy_btn.clicked.connect(lambda: self.copy_text(self.target_text.toPlainText()))
        
        self.history_btn = QPushButton()
        self.history_btn.setIcon(QIcon("icons/history.svg"))
        self.history_btn.clicked.connect(self.show_history)
        
        target_buttons.addWidget(self.target_speak_btn)
        target_buttons.addWidget(self.target_copy_btn)
        target_buttons.addWidget(self.history_btn)
        target_buttons.addStretch()
        target_panel.addLayout(target_buttons)
        
        # Добавляем панели с текстом и кнопками в горизонтальный layout
        text_panel.addLayout(source_panel)
        text_panel.addLayout(target_panel)
        
        # Добавляем горизонтальный layout в главный layout
        main_layout.addLayout(text_panel)
        
        # Создаем статусбар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def setup_history_screen(self):
        layout = QVBoxLayout(self.history_screen)
        
        # Создаем верхнюю панель
        top_panel = QHBoxLayout()
        
        # Заголовок
        title = QLabel("История переводов")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_panel.addWidget(title)
        
        # Кнопка очистки истории
        clear_btn = QPushButton("Очистить историю")
        clear_btn.setIcon(QIcon("icons/trash.svg"))
        clear_btn.clicked.connect(self.clear_history)
        top_panel.addWidget(clear_btn)
        
        # Кнопка закрытия
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_screen))
        top_panel.addWidget(close_btn)
        
        layout.addLayout(top_panel)
        
        # Создаем область прокрутки
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Создаем контейнер для записей
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setAlignment(Qt.AlignTop)
        self.history_layout.setSpacing(10)
        
        scroll.setWidget(self.history_container)
        layout.addWidget(scroll)

    def setup_language_screen(self):
        layout = QVBoxLayout(self.language_screen)
        
        # Создаем верхнюю панель
        top_panel = QHBoxLayout()
        
        # Заголовок
        title = QLabel("Выбор языка")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_panel.addWidget(title)
        
        # Кнопка закрытия
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_screen))
        top_panel.addWidget(close_btn)
        
        layout.addLayout(top_panel)
        
        # Создаем горизонтальный layout для списков языков
        languages_panel = QHBoxLayout()
        
        # Панель для исходного языка
        source_panel = QVBoxLayout()
        source_label = QLabel("Исходный язык")
        source_label.setStyleSheet("font-weight: bold;")
        source_panel.addWidget(source_label)
        
        # Поле поиска для исходного языка
        self.source_search = QLineEdit()
        self.source_search.setPlaceholderText("Поиск языка...")
        self.source_search.textChanged.connect(lambda: self.filter_languages('source'))
        source_panel.addWidget(self.source_search)
        
        # Список языков для исходного языка
        self.source_list = QListWidget()
        self.source_list.itemClicked.connect(lambda item: self.select_language('source', item))
        source_panel.addWidget(self.source_list)
        
        # Панель для целевого языка
        target_panel = QVBoxLayout()
        target_label = QLabel("Целевой язык")
        target_label.setStyleSheet("font-weight: bold;")
        target_panel.addWidget(target_label)
        
        # Поле поиска для целевого языка
        self.target_search = QLineEdit()
        self.target_search.setPlaceholderText("Поиск языка...")
        self.target_search.textChanged.connect(lambda: self.filter_languages('target'))
        target_panel.addWidget(self.target_search)
        
        # Список языков для целевого языка
        self.target_list = QListWidget()
        self.target_list.itemClicked.connect(lambda item: self.select_language('target', item))
        target_panel.addWidget(self.target_list)
        
        languages_panel.addLayout(source_panel)
        languages_panel.addLayout(target_panel)
        layout.addLayout(languages_panel)
        
        # Заполняем списки языков
        self.populate_language_lists()

    def populate_language_lists(self):
        # Очищаем списки
        self.source_list.clear()
        self.target_list.clear()
        
        # Добавляем языки в списки
        for code, name in LANGUAGES.items():
            self.source_list.addItem(name)
            self.target_list.addItem(name)
        
        # Устанавливаем текущие выбранные языки
        current_source = self.source_lang_btn.text()
        current_target = self.target_lang_btn.text()
        
        for i in range(self.source_list.count()):
            if self.source_list.item(i).text() == current_source:
                self.source_list.setCurrentRow(i)
                break
                
        for i in range(self.target_list.count()):
            if self.target_list.item(i).text() == current_target:
                self.target_list.setCurrentRow(i)
                break

    def filter_languages(self, target):
        search_text = self.source_search.text().lower() if target == 'source' else self.target_search.text().lower()
        list_widget = self.source_list if target == 'source' else self.target_list
        
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setHidden(search_text not in item.text().lower())

    def show_language_selector(self, target):
        self.current_language_target = target
        self.populate_language_lists()
        self.stack.setCurrentWidget(self.language_screen)

    def select_language(self, target, item):
        if target == 'source':
            self.source_lang_btn.setText(item.text())
        else:
            self.target_lang_btn.setText(item.text())
        self.stack.setCurrentWidget(self.main_screen)
        self.do_translation()

    def swap_languages(self):
        source_text = self.source_lang_btn.text()
        target_text = self.target_lang_btn.text()
        
        self.source_lang_btn.setText(target_text)
        self.target_lang_btn.setText(source_text)
        
        source_text = self.source_text.toPlainText()
        target_text = self.target_text.toPlainText()
        
        if source_text or target_text:
            self.source_text.setPlainText(target_text)
            self.target_text.clear()
            self.do_translation()

    def on_text_changed(self):
        # Сбрасываем и перезапускаем таймер при каждом изменении текста
        self.translation_timer.stop()
        
        # Отменяем предыдущий перевод, если он еще выполняется
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()
        
        # Запускаем перевод через 300мс после последнего изменения
        self.translation_timer.start(300)

    def do_translation(self):
        # Получаем текст для перевода
        text = self.source_text.toPlainText().strip()
        if not text:
            self.target_text.clear()
            return

        # Получаем коды языков
        source_lang = next(code for code, name in LANGUAGES.items() if name == self.source_lang_btn.text())
        target_lang = next(code for code, name in LANGUAGES.items() if name == self.target_lang_btn.text())

        # Если уже есть активный перевод, отменяем его
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()

        # Создаем и запускаем новый поток для перевода
        self.current_thread = TranslatorThread(text, source_lang, target_lang)
        self.current_thread.finished.connect(self.translation_finished)
        self.current_thread.start()
        
        self.statusBar.showMessage("Выполняется перевод...")

    def translation_finished(self, result, error):
        if error:
            self.statusBar.showMessage(f"Ошибка перевода: {str(error)}", 3000)
        else:
            self.target_text.setPlainText(result)
            self.statusBar.showMessage("Перевод завершен", 3000)
            
            # Сохраняем перевод в историю
            source_text = self.source_text.toPlainText()
            source_lang = next(code for code, name in LANGUAGES.items() if name == self.source_lang_btn.text())
            target_lang = next(code for code, name in LANGUAGES.items() if name == self.target_lang_btn.text())
            self.save_translation(source_text, result, source_lang, target_lang)
        
        self.current_thread = None

    def speak_text(self, text, lang):
        if not text.strip():
            return
            
        try:
            # Очищаем предыдущий временный файл
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                try:
                    os.remove(self.current_audio_file)
                except:
                    pass

            # Создаем временный файл
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                self.current_audio_file = temp_file.name
                
            # Создаем и сохраняем аудио
            tts = gTTS(text=text, lang=lang)
            tts.save(self.current_audio_file)
            
            # Воспроизводим
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()
            
            self.statusBar.showMessage("Воспроизведение...", 3000)
            
        except Exception as e:
            self.statusBar.showMessage(f"Ошибка воспроизведения: {str(e)}", 3000)

    def copy_text(self, text):
        if text.strip():
            pyperclip.copy(text)
            self.statusBar.showMessage("Текст скопирован в буфер обмена", 3000)

    def clear_source_text(self):
        self.source_text.clear()
        self.target_text.clear()
        self.statusBar.showMessage("Текст очищен", 3000)

    def show_history(self):
        self.load_history()
        self.stack.setCurrentWidget(self.history_screen)

    def load_history(self):
        # Очищаем текущую историю
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Загружаем последние 50 переводов
        self.cursor.execute('''
            SELECT rowid, timestamp, source_text, translated_text, source_lang, target_lang 
            FROM translations 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        translations = self.cursor.fetchall()
        
        for rowid, timestamp, source_text, translated_text, source_lang, target_lang in translations:
            # Создаем карточку для записи
            card = QFrame()
            card.setObjectName("historyCard")
            card.setStyleSheet("""
                #historyCard {
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            
            card_layout = QVBoxLayout(card)
            
            # Верхняя панель с информацией о языках и времени
            header = QHBoxLayout()
            
            # Информация о языках
            lang_info = QLabel(f"{LANGUAGES.get(source_lang, source_lang)} → {LANGUAGES.get(target_lang, target_lang)}")
            header.addWidget(lang_info)
            
            # Время
            time_info = QLabel(timestamp)
            time_info.setStyleSheet("color: #666;")
            header.addWidget(time_info)
            
            # Кнопка удаления
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/trash.svg"))
            delete_btn.clicked.connect(lambda checked, rid=rowid: self.delete_translation(rid))
            header.addWidget(delete_btn)
            
            card_layout.addLayout(header)
            
            # Тексты перевода
            texts = QHBoxLayout()
            
            # Исходный текст
            source = QPlainTextEdit()
            source.setPlainText(source_text)
            source.setReadOnly(True)
            source.setMaximumHeight(100)
            texts.addWidget(source)
            
            # Перевод
            target = QPlainTextEdit()
            target.setPlainText(translated_text)
            target.setReadOnly(True)
            target.setMaximumHeight(100)
            texts.addWidget(target)
            
            card_layout.addLayout(texts)
            
            self.history_layout.addWidget(card)

    def delete_translation(self, rowid):
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите удалить эту запись?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cursor.execute('DELETE FROM translations WHERE rowid = ?', (rowid,))
            self.conn.commit()
            self.load_history()

    def clear_history(self):
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите очистить всю историю переводов?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cursor.execute('DELETE FROM translations')
            self.conn.commit()
            self.load_history()

    def closeEvent(self, event):
        # Очищаем временный файл при закрытии
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                os.remove(self.current_audio_file)
            except:
                pass
        # Закрываем соединение с базой данных
        self.conn.close()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec()) 