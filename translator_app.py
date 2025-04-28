import sys
import sqlite3
import asyncio
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QTextEdit, QPushButton,
                             QScrollArea, QMessageBox, QLabel, QStackedWidget,
                             QLineEdit, QFrame)
from PySide6.QtCore import Qt, QThread, Signal, QSize, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QCursor
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import os
import tempfile

class IconButton(QPushButton):
    def __init__(self, icon_path, size=24, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size, size))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(size + 16, size + 16)
        self.setStyleSheet("""
            IconButton {
                background: transparent;
                border: none;
            }
            IconButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
        """)
        self.success_timer = QTimer(self)
        self.success_timer.setSingleShot(True)
        self.success_timer.timeout.connect(self.reset_icon)
        self.original_icon = icon_path

    def show_success(self):
        self.setIcon(QIcon("icons/check.svg"))
        self.success_timer.start(1000)  # Показываем галочку на 1 секунду

    def reset_icon(self):
        self.setIcon(QIcon(self.original_icon))

class TranslatorThread(QThread):
    finished = Signal(str, Exception)

    def __init__(self, text, source_lang, target_lang):
        super().__init__()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang

    def run(self):
        try:
            translator = Translator()
            result = translator.translate(
                self.text,
                src=self.source_lang,
                dest=self.target_lang
            )
            self.finished.emit(result.text, None)
        except Exception as e:
            self.finished.emit("", e)

class LanguageSelector(QWidget):
    language_selected = Signal(str, str)  # code, name

    def __init__(self, languages, parent=None):
        super().__init__(parent)
        self.languages = languages
        self.setup_ui()
        self.setStyleSheet("background-color: #282828;")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Добавляем заголовок и кнопку закрытия
        header = QHBoxLayout()
        title = QLabel("Выбор языка")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        
        close_btn = IconButton("icons/close.svg")
        close_btn.clicked.connect(lambda: self.parent().setCurrentWidget(self.parent().parent().main_screen))
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(close_btn)
        main_layout.addLayout(header)

        # Основной контейнер для панелей выбора языка
        lang_container = QHBoxLayout()
        lang_container.setSpacing(20)

        # Левая панель
        left_panel = QVBoxLayout()
        search_container_left = QFrame()
        search_container_left.setStyleSheet("""
            QFrame {
                background-color: #3B3B3B;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        search_layout_left = QHBoxLayout(search_container_left)
        search_layout_left.setContentsMargins(10, 0, 10, 0)
        
        search_icon_left = QLabel()
        search_icon_left.setPixmap(QIcon("icons/search.svg").pixmap(QSize(20, 20)))
        search_layout_left.addWidget(search_icon_left)
        
        self.left_search = QLineEdit()
        self.left_search.setPlaceholderText("Поиск языка...")
        self.left_search.setMinimumHeight(45)
        self.left_search.textChanged.connect(self.filter_left_languages)
        search_layout_left.addWidget(self.left_search)
        left_panel.addWidget(search_container_left)

        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.left_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #3B3B3B;
                border: none;
                border-radius: 8px;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        self.left_languages_widget = QWidget()
        self.left_languages_layout = QVBoxLayout(self.left_languages_widget)
        self.left_languages_layout.setAlignment(Qt.AlignTop)
        self.left_languages_layout.setSpacing(8)
        self.left_languages_layout.setContentsMargins(8, 8, 8, 8)
        self.left_scroll.setWidget(self.left_languages_widget)
        left_panel.addWidget(self.left_scroll)

        # Правая панель
        right_panel = QVBoxLayout()
        search_container_right = QFrame()
        search_container_right.setStyleSheet("""
            QFrame {
                background-color: #3B3B3B;
                border-radius: 8px;
                padding: 5px 5px 5px;
            }
        """)
        search_layout_right = QHBoxLayout(search_container_right)
        search_layout_right.setContentsMargins(10, 0, 10, 0)
        
        search_icon_right = QLabel()
        search_icon_right.setPixmap(QIcon("icons/search.svg").pixmap(QSize(20, 20)))
        search_layout_right.addWidget(search_icon_right)
        
        self.right_search = QLineEdit()
        self.right_search.setPlaceholderText("Поиск языка...")
        self.right_search.setMinimumHeight(45)
        self.right_search.textChanged.connect(self.filter_right_languages)
        search_layout_right.addWidget(self.right_search)
        right_panel.addWidget(search_container_right)

        self.right_scroll = QScrollArea()
        self.right_scroll.setWidgetResizable(True)
        self.right_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #3B3B3B;
                border: none;
                border-radius: 8px;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        self.right_languages_widget = QWidget()
        self.right_languages_layout = QVBoxLayout(self.right_languages_widget)
        self.right_languages_layout.setAlignment(Qt.AlignTop)
        self.right_languages_layout.setSpacing(8)
        self.right_languages_layout.setContentsMargins(8, 8, 8, 8)
        self.right_scroll.setWidget(self.right_languages_widget)
        right_panel.addWidget(self.right_scroll)

        # Добавляем панели в контейнер
        lang_container.addLayout(left_panel)
        lang_container.addLayout(right_panel)
        main_layout.addLayout(lang_container)

        # Заполняем списки языков
        self.populate_languages()

        # Стилизация
        self.setStyleSheet("""
            QWidget {
                background-color: #282828;
            }
            QLineEdit {
                background-color: transparent;
                color: white;
                border: none;
                border-left: 1px solid rgba(255, 255, 255, 0.3);
                padding: 8px 8px 8px 16px;
                font-size: 16px;
                margin-left: 8px;
            }
            QLineEdit::placeholder {
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: center;
                font-size: 16px;
                font-family: monospace;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: #4CAF50;
            }
            QLabel {
                color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def populate_languages(self):
        for code, name in self.languages.items():
            # Левая панель
            left_btn = QPushButton(name.capitalize())
            left_btn.setProperty('code', code)
            left_btn.setCursor(QCursor(Qt.PointingHandCursor))
            left_btn.clicked.connect(lambda checked, c=code, n=name: self.on_language_selected(c, n))
            self.left_languages_layout.addWidget(left_btn)

            # Правая панель
            right_btn = QPushButton(name.capitalize())
            right_btn.setProperty('code', code)
            right_btn.setCursor(QCursor(Qt.PointingHandCursor))
            right_btn.clicked.connect(lambda checked, c=code, n=name: self.on_language_selected(c, n))
            self.right_languages_layout.addWidget(right_btn)

    def on_language_selected(self, code, name):
        # Сбрасываем текст в полях поиска
        self.left_search.clear()
        self.right_search.clear()
        # Отправляем сигнал о выборе языка
        self.language_selected.emit(code, name.capitalize())

    def filter_languages(self, text, layout):
        text = text.lower()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget:
                name = widget.text().lower()
                widget.setVisible(text in name)

    def filter_left_languages(self, text):
        self.filter_languages(text, self.left_languages_layout)

    def filter_right_languages(self, text):
        self.filter_languages(text, self.right_languages_layout)

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.init_db()
        self.setup_ui()
        self.setup_styles()
        self.translator_thread = None
        self.current_audio_file = None
        self.current_lang_target = None
        
        # Добавляем таймер для отложенного перевода
        self.translate_timer = QTimer()
        self.translate_timer.setSingleShot(True)
        self.translate_timer.timeout.connect(self.do_translation)

    def init_db(self):
        # Как горилла строит своё гнездо - создаём базу данных
        self.conn = sqlite3.connect('translations.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations
            (timestamp TEXT, source_text TEXT, translated_text TEXT,
             source_lang TEXT, target_lang TEXT)
        ''')
        self.conn.commit()

    def setup_ui(self):
        self.setWindowTitle('Переводчик')
        self.setMinimumSize(1000, 700)

        # Создаем стек виджетов для разных экранов
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Создаем основной экран
        self.main_screen = QWidget()
        self.setup_main_screen()
        self.stack.addWidget(self.main_screen)

        # Создаем экран выбора языка
        self.lang_select_screen = LanguageSelector(LANGUAGES)
        self.lang_select_screen.language_selected.connect(self.on_language_selected)
        self.stack.addWidget(self.lang_select_screen)

        # Создаем экран истории
        self.history_screen = QWidget()
        self.setup_history_screen()
        self.stack.addWidget(self.history_screen)

        # Показываем главный экран
        self.stack.setCurrentWidget(self.main_screen)

    def setup_main_screen(self):
        layout = QVBoxLayout(self.main_screen)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header с языками
        header = QHBoxLayout()
        header.setAlignment(Qt.AlignCenter)
        
        self.source_lang_btn = QPushButton("English")
        self.source_lang_btn.setProperty('code', 'en')
        self.source_lang_btn.setObjectName("languageButton")
        self.source_lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.source_lang_btn.clicked.connect(lambda: self.show_language_selector("source"))
        
        self.swap_btn = QPushButton()
        self.swap_btn.setIcon(QIcon("icons/swap.svg"))
        self.swap_btn.setObjectName("swapButton")
        self.swap_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.swap_btn.clicked.connect(self.swap_languages)
        
        self.target_lang_btn = QPushButton("Русский")
        self.target_lang_btn.setProperty('code', 'ru')
        self.target_lang_btn.setObjectName("languageButton")
        self.target_lang_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.target_lang_btn.clicked.connect(lambda: self.show_language_selector("target"))
        
        header.addStretch()
        header.addWidget(self.source_lang_btn)
        header.addWidget(self.swap_btn)
        header.addWidget(self.target_lang_btn)
        header.addStretch()
        
        layout.addLayout(header)

        # Контейнеры для текста
        text_container = QHBoxLayout()
        
        # Исходный текст
        source_container = QVBoxLayout()
        self.source_text = QTextEdit()
        self.source_text.setPlaceholderText("Введите текст для перевода...")
        self.source_text.textChanged.connect(self.on_text_changed)
        
        source_buttons = QHBoxLayout()
        self.source_clear = IconButton("icons/clear.svg")
        self.source_clear.clicked.connect(self.clear_source)
        self.source_speak = IconButton("icons/speaker.svg")
        self.source_speak.clicked.connect(lambda: self.speak_text(self.source_text.toPlainText(), "source"))
        self.source_copy = IconButton("icons/copy.svg")
        self.source_copy.clicked.connect(lambda: self.copy_text(self.source_text.toPlainText(), "source"))
        
        self.translate_btn = QPushButton("Translate")
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.translate_btn.clicked.connect(self.translate_text)
        
        source_buttons.addWidget(self.source_clear)
        source_buttons.addWidget(self.source_speak)
        source_buttons.addWidget(self.source_copy)
        source_buttons.addStretch()
        source_buttons.addWidget(self.translate_btn)
        
        source_container.addWidget(self.source_text)
        source_container.addLayout(source_buttons)
        
        # Перевод
        target_container = QVBoxLayout()
        self.target_text = QTextEdit()
        self.target_text.setReadOnly(True)
        self.target_text.setPlaceholderText("Перевод появится здесь...")
        
        target_buttons = QHBoxLayout()
        self.history_btn = IconButton("icons/history.svg")
        self.history_btn.clicked.connect(self.show_history)
        self.target_speak = IconButton("icons/speaker.svg")
        self.target_speak.clicked.connect(lambda: self.speak_text(self.target_text.toPlainText(), "target"))
        self.target_copy = IconButton("icons/copy.svg")
        self.target_copy.clicked.connect(lambda: self.copy_text(self.target_text.toPlainText(), "target"))
        
        target_buttons.addWidget(self.history_btn)
        target_buttons.addWidget(self.target_speak)
        target_buttons.addWidget(self.target_copy)
        target_buttons.addStretch()
        
        target_container.addWidget(self.target_text)
        target_container.addLayout(target_buttons)
        
        text_container.addLayout(source_container)
        text_container.addLayout(target_container)
        
        layout.addLayout(text_container)

    def setup_history_screen(self):
        layout = QVBoxLayout(self.history_screen)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Заголовок
        header = QHBoxLayout()
        title = QLabel("История переводов")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        close_btn = IconButton("icons/close.svg")
        close_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_screen))
        
        clear_btn = QPushButton("Очистить историю")
        clear_btn.setIcon(QIcon("icons/trash.svg"))
        clear_btn.setIconSize(QSize(25, 25))
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_history)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border: none;
                padding: 8px 16px;
                color: white;
                border-radius: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        clear_btn.setLayoutDirection(Qt.RightToLeft)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(clear_btn)
        header.addWidget(close_btn)
        
        layout.addLayout(header)

        # Контейнер для истории
        history_container = QWidget()
        history_container.setObjectName("historyWidget")
        self.history_layout = QVBoxLayout(history_container)
        self.history_layout.setAlignment(Qt.AlignTop)
        
        scroll = QScrollArea()
        scroll.setWidget(history_container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        layout.addWidget(scroll)
        
        # Загружаем историю
        self.load_history()

    def setup_styles(self):
        # Устанавливаем темную тему
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        # Общие стили для приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282828;
            }
            QTextEdit {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QComboBox {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QScrollArea {
                background-color: #333333;
                border: none;
                border-radius: 8px;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            IconButton {
                background: transparent;
                border: none;
            }
            IconButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            #languageButton {
                background-color: #333333;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                text-align: center;
            }
            #swapButton {
                background-color: transparent;
                padding: 8px;
                border-radius: 4px;
            }
            #historyWidget {
                background-color: #333333;
                border-radius: 8px;
                padding: 10px;
            }
            #historyEntry {
                background-color: #444444;
                border-radius: 4px;
                padding: 10px;
                margin: 5px 0;
            }
        """)

    def show_language_selector(self, target):
        self.current_lang_target = target  # Сохраняем цель выбора языка
        self.stack.setCurrentWidget(self.lang_select_screen)

    def on_language_selected(self, code, name):
        if self.current_lang_target == "source":
            self.source_lang_btn.setText(name)
            self.source_lang_btn.setProperty('code', code)
        else:
            self.target_lang_btn.setText(name)
            self.target_lang_btn.setProperty('code', code)
        
        self.stack.setCurrentWidget(self.main_screen)
        self.translate_text()  # Обновляем перевод с новым языком

    def show_history(self):
        self.load_history()
        self.stack.setCurrentWidget(self.history_screen)

    def clear_source(self):
        self.source_text.clear()
        self.source_clear.show_success()

    def copy_text(self, text, source):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            if source == 'source':
                self.source_copy.show_success()
            else:
                self.target_copy.show_success()

    def speak_text(self, text, source):
        if not text:
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
                
            # Определяем язык текста
            lang = self.source_lang_btn.property('code') if source == 'source' else self.target_lang_btn.property('code')
            
            # Создаем и сохраняем аудио
            tts = gTTS(text=text, lang=lang)
            tts.save(self.current_audio_file)
            
            # Воспроизводим
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()
            
            # Показываем галочку
            if source == 'source':
                self.source_speak.show_success()
            else:
                self.target_speak.show_success()
            
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка',
                              f'Не удалось озвучить текст: {str(e)}')

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
            self.load_history()  # Перезагружаем пустую историю

    def on_text_changed(self):
        # Сбрасываем и перезапускаем таймер при каждом изменении текста
        self.translate_timer.stop()
        # Запускаем перевод через 1 секунду после последнего изменения
        self.translate_timer.start(1000)

    def translate_text(self):
        # Этот метод теперь вызывается только по кнопке
        self.do_translation()

    def do_translation(self):
        # Получаем текст для перевода
        text = self.source_text.toPlainText().strip()
        if not text:
            self.target_text.clear()
            return

        # Получаем коды языков
        source_lang = self.source_lang_btn.property('code')
        target_lang = self.target_lang_btn.property('code')

        # Если уже есть активный перевод, отменяем его
        if self.translator_thread and self.translator_thread.isRunning():
            self.translator_thread.terminate()
            self.translator_thread.wait()

        # Отключаем кнопку перевода
        self.translate_btn.setEnabled(False)
        self.translate_btn.setText("Переводим...")

        # Создаем и запускаем новый поток для перевода
        self.translator_thread = TranslatorThread(text, source_lang, target_lang)
        self.translator_thread.finished.connect(self.handle_translation)
        self.translator_thread.start()

    def handle_translation(self, translated_text, error):
        # Включаем кнопку обратно
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText("Translate")

        if error:
            QMessageBox.warning(self, "Ошибка", str(error))
            return

        self.target_text.setText(translated_text)
        
        # Сохраняем перевод в базу данных
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source_text = self.source_text.toPlainText()
        source_lang = self.source_lang_btn.property('code')
        target_lang = self.target_lang_btn.property('code')
        
        self.cursor.execute('''
            INSERT INTO translations 
            (timestamp, source_text, translated_text, source_lang, target_lang)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, source_text, translated_text, source_lang, target_lang))
        self.conn.commit()

        # Обновляем историю
        self.load_history()

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
            # Создаем виджет для записи
            entry = QFrame()
            entry.setObjectName("historyEntry")
            entry_layout = QVBoxLayout(entry)

            # Добавляем информацию о языках и времени
            header = QHBoxLayout()
            lang_info = QLabel(f"{source_lang.upper()} → {target_lang.upper()}")
            time_info = QLabel(timestamp)
            time_info.setStyleSheet("color: #888888;")
            
            delete_btn = IconButton("icons/delete.svg")
            delete_btn.clicked.connect(lambda checked, rid=rowid: self.delete_entry(rid))
            
            header.addWidget(lang_info)
            header.addStretch()
            header.addWidget(time_info)
            header.addWidget(delete_btn)
            entry_layout.addLayout(header)

            # Добавляем тексты
            text_container = QFrame()
            text_layout = QHBoxLayout(text_container)
            text_layout.setContentsMargins(0, 0, 0, 0)

            # Исходный текст
            source_container = QVBoxLayout()
            source = QTextEdit()
            source.setPlainText(source_text)
            source.setReadOnly(True)
            source.setMaximumHeight(100)
            source_container.addWidget(source)

            source_buttons = QHBoxLayout()
            speak_source = IconButton("icons/speaker.svg")
            speak_source.clicked.connect(lambda checked, text=source_text: self.speak_text(text, "source"))
            copy_source = IconButton("icons/copy.svg")
            copy_source.clicked.connect(lambda checked, text=source_text: self.copy_text(text, "source"))
            
            source_buttons.addWidget(speak_source)
            source_buttons.addWidget(copy_source)
            source_buttons.addStretch()
            source_container.addLayout(source_buttons)

            # Перевод
            target_container = QVBoxLayout()
            target = QTextEdit()
            target.setPlainText(translated_text)
            target.setReadOnly(True)
            target.setMaximumHeight(100)
            target_container.addWidget(target)

            target_buttons = QHBoxLayout()
            speak_target = IconButton("icons/speaker.svg")
            speak_target.clicked.connect(lambda checked, text=translated_text: self.speak_text(text, "target"))
            copy_target = IconButton("icons/copy.svg")
            copy_target.clicked.connect(lambda checked, text=translated_text: self.copy_text(text, "target"))
            
            target_buttons.addWidget(speak_target)
            target_buttons.addWidget(copy_target)
            target_buttons.addStretch()
            target_container.addLayout(target_buttons)

            text_layout.addLayout(source_container)
            text_layout.addLayout(target_container)
            entry_layout.addWidget(text_container)

            self.history_layout.addWidget(entry)

    def delete_entry(self, rowid):
        # Как обезьянка выбрасывает испорченный банан - удаляем запись
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
            self.load_history()  # Перезагружаем историю

    def swap_languages(self):
        # Меняем языки местами
        source_text = self.source_lang_btn.text()
        source_code = self.source_lang_btn.property('code')
        target_text = self.target_lang_btn.text()
        target_code = self.target_lang_btn.property('code')
        
        self.source_lang_btn.setText(target_text)
        self.source_lang_btn.setProperty('code', target_code)
        self.target_lang_btn.setText(source_text)
        self.target_lang_btn.setProperty('code', source_code)

    def closeEvent(self, event):
        # Как обезьянка прибирается в своём домике - закрываем соединение с БД
        self.conn.close()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec()) 