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
from translations import UI_TRANSLATIONS, LANGUAGES

LANGUAGE_TRANSLATIONS = {
    'af': {'ru': 'Африкаанс', 'en': 'Afrikaans'},
    'sq': {'ru': 'Албанский', 'en': 'Albanian'},
    'am': {'ru': 'Амхарский', 'en': 'Amharic'},
    'ar': {'ru': 'Арабский', 'en': 'Arabic'},
    'hy': {'ru': 'Армянский', 'en': 'Armenian'},
    'az': {'ru': 'Азербайджанский', 'en': 'Azerbaijani'},
    'eu': {'ru': 'Баскский', 'en': 'Basque'},
    'be': {'ru': 'Белорусский', 'en': 'Belarusian'},
    'bn': {'ru': 'Бенгальский', 'en': 'Bengali'},
    'bs': {'ru': 'Боснийский', 'en': 'Bosnian'},
    'bg': {'ru': 'Болгарский', 'en': 'Bulgarian'},
    'ca': {'ru': 'Каталанский', 'en': 'Catalan'},
    'ceb': {'ru': 'Себуано', 'en': 'Cebuano'},
    'zh-cn': {'ru': 'Китайский (упрощенный)', 'en': 'Chinese (Simplified)'},
    'zh-tw': {'ru': 'Китайский (традиционный)', 'en': 'Chinese (Traditional)'},
    'co': {'ru': 'Корсиканский', 'en': 'Corsican'},
    'hr': {'ru': 'Хорватский', 'en': 'Croatian'},
    'cs': {'ru': 'Чешский', 'en': 'Czech'},
    'da': {'ru': 'Датский', 'en': 'Danish'},
    'nl': {'ru': 'Голландский', 'en': 'Dutch'},
    'en': {'ru': 'Английский', 'en': 'English'},
    'eo': {'ru': 'Эсперанто', 'en': 'Esperanto'},
    'et': {'ru': 'Эстонский', 'en': 'Estonian'},
    'fi': {'ru': 'Финский', 'en': 'Finnish'},
    'fr': {'ru': 'Французский', 'en': 'French'},
    'fy': {'ru': 'Фризский', 'en': 'Frisian'},
    'gl': {'ru': 'Галисийский', 'en': 'Galician'},
    'ka': {'ru': 'Грузинский', 'en': 'Georgian'},
    'de': {'ru': 'Немецкий', 'en': 'German'},
    'el': {'ru': 'Греческий', 'en': 'Greek'},
    'gu': {'ru': 'Гуджарати', 'en': 'Gujarati'},
    'ht': {'ru': 'Гаитянский креольский', 'en': 'Haitian Creole'},
    'ha': {'ru': 'Хауса', 'en': 'Hausa'},
    'haw': {'ru': 'Гавайский', 'en': 'Hawaiian'},
    'he': {'ru': 'Иврит', 'en': 'Hebrew'},
    'hi': {'ru': 'Хинди', 'en': 'Hindi'},
    'hmn': {'ru': 'Хмонг', 'en': 'Hmong'},
    'hu': {'ru': 'Венгерский', 'en': 'Hungarian'},
    'is': {'ru': 'Исландский', 'en': 'Icelandic'},
    'ig': {'ru': 'Игбо', 'en': 'Igbo'},
    'id': {'ru': 'Индонезийский', 'en': 'Indonesian'},
    'ga': {'ru': 'Ирландский', 'en': 'Irish'},
    'it': {'ru': 'Итальянский', 'en': 'Italian'},
    'ja': {'ru': 'Японский', 'en': 'Japanese'},
    'jw': {'ru': 'Яванский', 'en': 'Javanese'},
    'kn': {'ru': 'Каннада', 'en': 'Kannada'},
    'kk': {'ru': 'Казахский', 'en': 'Kazakh'},
    'km': {'ru': 'Кхмерский', 'en': 'Khmer'},
    'ko': {'ru': 'Корейский', 'en': 'Korean'},
    'ku': {'ru': 'Курдский', 'en': 'Kurdish'},
    'ky': {'ru': 'Киргизский', 'en': 'Kyrgyz'},
    'lo': {'ru': 'Лаосский', 'en': 'Lao'},
    'la': {'ru': 'Латинский', 'en': 'Latin'},
    'lv': {'ru': 'Латышский', 'en': 'Latvian'},
    'lt': {'ru': 'Литовский', 'en': 'Lithuanian'},
    'lb': {'ru': 'Люксембургский', 'en': 'Luxembourgish'},
    'mk': {'ru': 'Македонский', 'en': 'Macedonian'},
    'mg': {'ru': 'Малагасийский', 'en': 'Malagasy'},
    'ms': {'ru': 'Малайский', 'en': 'Malay'},
    'ml': {'ru': 'Малаялам', 'en': 'Malayalam'},
    'mt': {'ru': 'Мальтийский', 'en': 'Maltese'},
    'mi': {'ru': 'Маори', 'en': 'Maori'},
    'mr': {'ru': 'Маратхи', 'en': 'Marathi'},
    'mn': {'ru': 'Монгольский', 'en': 'Mongolian'},
    'my': {'ru': 'Бирманский', 'en': 'Myanmar'},
    'ne': {'ru': 'Непальский', 'en': 'Nepali'},
    'no': {'ru': 'Норвежский', 'en': 'Norwegian'},
    'ny': {'ru': 'Ньянджа', 'en': 'Nyanja'},
    'or': {'ru': 'Ория', 'en': 'Odia'},
    'ps': {'ru': 'Пушту', 'en': 'Pashto'},
    'fa': {'ru': 'Персидский', 'en': 'Persian'},
    'pl': {'ru': 'Польский', 'en': 'Polish'},
    'pt': {'ru': 'Португальский', 'en': 'Portuguese'},
    'pa': {'ru': 'Панджаби', 'en': 'Punjabi'},
    'ro': {'ru': 'Румынский', 'en': 'Romanian'},
    'ru': {'ru': 'Русский', 'en': 'Russian'},
    'sm': {'ru': 'Самоанский', 'en': 'Samoan'},
    'gd': {'ru': 'Шотландский гэльский', 'en': 'Scots Gaelic'},
    'sr': {'ru': 'Сербский', 'en': 'Serbian'},
    'st': {'ru': 'Сесото', 'en': 'Sesotho'},
    'sn': {'ru': 'Шона', 'en': 'Shona'},
    'sd': {'ru': 'Синдхи', 'en': 'Sindhi'},
    'si': {'ru': 'Сингальский', 'en': 'Sinhala'},
    'sk': {'ru': 'Словацкий', 'en': 'Slovak'},
    'sl': {'ru': 'Словенский', 'en': 'Slovenian'},
    'so': {'ru': 'Сомалийский', 'en': 'Somali'},
    'es': {'ru': 'Испанский', 'en': 'Spanish'},
    'su': {'ru': 'Сунданский', 'en': 'Sundanese'},
    'sw': {'ru': 'Суахили', 'en': 'Swahili'},
    'sv': {'ru': 'Шведский', 'en': 'Swedish'},
    'tl': {'ru': 'Тагальский', 'en': 'Tagalog'},
    'tg': {'ru': 'Таджикский', 'en': 'Tajik'},
    'ta': {'ru': 'Тамильский', 'en': 'Tamil'},
    'tt': {'ru': 'Татарский', 'en': 'Tatar'},
    'te': {'ru': 'Телугу', 'en': 'Telugu'},
    'th': {'ru': 'Тайский', 'en': 'Thai'},
    'tr': {'ru': 'Турецкий', 'en': 'Turkish'},
    'tk': {'ru': 'Туркменский', 'en': 'Turkmen'},
    'uk': {'ru': 'Украинский', 'en': 'Ukrainian'},
    'ur': {'ru': 'Урду', 'en': 'Urdu'},
    'ug': {'ru': 'Уйгурский', 'en': 'Uyghur'},
    'uz': {'ru': 'Узбекский', 'en': 'Uzbek'},
    'vi': {'ru': 'Вьетнамский', 'en': 'Vietnamese'},
    'cy': {'ru': 'Валлийский', 'en': 'Welsh'},
    'xh': {'ru': 'Коса', 'en': 'Xhosa'},
    'yi': {'ru': 'Идиш', 'en': 'Yiddish'},
    'yo': {'ru': 'Йоруба', 'en': 'Yoruba'},
    'zu': {'ru': 'Зулу', 'en': 'Zulu'}
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
        self.current_language = 'ru'  # По умолчанию русский
        self.setWindowTitle(UI_TRANSLATIONS[self.current_language]['window_title'])
        self.setGeometry(100, 100, 800, 400)
        
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
        
        # Создаем экраны выбора языков
        self.source_language_screen = QWidget()
        self.setup_language_screen(self.source_language_screen, 'source')
        self.stack.addWidget(self.source_language_screen)
        
        self.target_language_screen = QWidget()
        self.setup_language_screen(self.target_language_screen, 'target')
        self.stack.addWidget(self.target_language_screen)
        
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
        
        # --- Первая строка: только языки, строго по центру ---
        lang_switcher_panel = QHBoxLayout()
        lang_switcher_panel.addStretch()
        self.source_lang_btn = QPushButton('Английский' if self.current_language == 'ru' else 'English')
        self.source_lang_btn.setFixedWidth(150)
        self.source_lang_btn.clicked.connect(lambda: self.show_language_selector('source'))
        swap_button = QPushButton("⇄")
        swap_button.setFixedWidth(40)
        swap_button.clicked.connect(self.swap_languages)
        self.target_lang_btn = QPushButton('Русский' if self.current_language == 'ru' else 'Russian')
        self.target_lang_btn.setFixedWidth(150)
        self.target_lang_btn.clicked.connect(lambda: self.show_language_selector('target'))
        lang_switcher_panel.addWidget(self.source_lang_btn)
        lang_switcher_panel.addWidget(swap_button)
        lang_switcher_panel.addWidget(self.target_lang_btn)
        lang_switcher_panel.addStretch()
        main_layout.addLayout(lang_switcher_panel)

        # Создаем горизонтальный layout для текстовых полей и кнопок
        text_panel = QHBoxLayout()
        
        # Создаем вертикальный layout для исходного текста и его кнопок
        source_panel = QVBoxLayout()
        self.source_text = QPlainTextEdit()
        self.source_text.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['source_placeholder'])
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
        self.target_text.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['target_placeholder'])
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
        
        # --- Статусбар с двумя кнопками для выбора языка интерфейса ---
        self.statusBar = QStatusBar()
        self.statusBar.setMaximumHeight(30)
        self.setStatusBar(self.statusBar)
        lang_label = QLabel(UI_TRANSLATIONS[self.current_language]['interface_language'])
        lang_label.setStyleSheet('font-size: 11px; padding-right: 4px;')
        self.statusBar.addPermanentWidget(lang_label)
        # Кнопки для выбора языка интерфейса
        self.lang_btn_ru = QPushButton('Русский')
        self.lang_btn_en = QPushButton('English')
        self.lang_btn_ru.setStyleSheet('font-size: 11px; min-width: 60px;')
        self.lang_btn_en.setStyleSheet('font-size: 11px; min-width: 60px;')
        self.lang_btn_ru.clicked.connect(lambda: self.set_interface_language('ru'))
        self.lang_btn_en.clicked.connect(lambda: self.set_interface_language('en'))
        self.statusBar.addPermanentWidget(self.lang_btn_ru)
        self.statusBar.addPermanentWidget(self.lang_btn_en)
        self.update_lang_buttons()

        # Добавляем курсор для всех кнопок
        self.source_lang_btn.setCursor(Qt.PointingHandCursor)
        self.target_lang_btn.setCursor(Qt.PointingHandCursor)
        swap_button.setCursor(Qt.PointingHandCursor)
        self.source_speak_btn.setCursor(Qt.PointingHandCursor)
        self.source_copy_btn.setCursor(Qt.PointingHandCursor)
        self.clear_source_btn.setCursor(Qt.PointingHandCursor)
        self.target_speak_btn.setCursor(Qt.PointingHandCursor)
        self.target_copy_btn.setCursor(Qt.PointingHandCursor)
        self.history_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn_ru.setCursor(Qt.PointingHandCursor)
        self.lang_btn_en.setCursor(Qt.PointingHandCursor)

    def set_interface_language(self, lang_code):
        if lang_code == 'ru':
            self.current_language = 'ru'
            self.lang_btn_ru.setDisabled(True)
            self.lang_btn_en.setDisabled(False)
        else:
            self.current_language = 'en'
            self.lang_btn_ru.setDisabled(False)
            self.lang_btn_en.setDisabled(True)
        
        # Сохраняем текущие языки
        current_source = self.source_lang_btn.text()
        current_target = self.target_lang_btn.text()
        
        # Находим коды языков по текущим названиям
        source_code = None
        target_code = None
        
        # Ищем коды для обоих языков интерфейса
        for code, names in LANGUAGE_TRANSLATIONS.items():
            if names['ru'] == current_source or names['en'] == current_source:
                source_code = code
            if names['ru'] == current_target or names['en'] == current_target:
                target_code = code
        
        # Устанавливаем языки с новыми переводами
        if source_code:
            self.source_lang_btn.setText(LANGUAGE_TRANSLATIONS[source_code][self.current_language])
        if target_code:
            self.target_lang_btn.setText(LANGUAGE_TRANSLATIONS[target_code][self.current_language])
        
        self.update_interface_language()
        # Быстро обновляем экраны
        current_screen = self.stack.currentWidget()
        self.stack.setCurrentWidget(self.source_language_screen)
        self.stack.setCurrentWidget(self.target_language_screen)
        self.stack.setCurrentWidget(self.history_screen)
        self.stack.setCurrentWidget(self.main_screen)
        self.main_screen.update()
        self.history_screen.update()
        self.source_language_screen.update()
        self.target_language_screen.update()
        self.source_text.update()
        self.target_text.update()
        self.update_lang_buttons()

    def update_lang_buttons(self):
        if self.current_language == 'ru':
            self.lang_btn_ru.setDisabled(True)
            self.lang_btn_en.setDisabled(False)
        else:
            self.lang_btn_ru.setDisabled(False)
            self.lang_btn_en.setDisabled(True)

    def update_interface_language(self):
        # Обновляем заголовок окна
        self.setWindowTitle(UI_TRANSLATIONS[self.current_language]['window_title'])
        
        # Обновляем плейсхолдеры
        self.source_text.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['source_placeholder'])
        self.target_text.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['target_placeholder'])
        
        # Обновляем метку языка интерфейса
        for widget in self.main_screen.findChildren(QLabel):
            if widget.text() in [UI_TRANSLATIONS['ru']['interface_language'], UI_TRANSLATIONS['en']['interface_language']]:
                widget.setText(UI_TRANSLATIONS[self.current_language]['interface_language'])
        
        # Обновляем заголовки и тексты в экране истории
        if hasattr(self, 'history_screen'):
            for widget in self.history_screen.findChildren(QLabel):
                if widget.text() in [UI_TRANSLATIONS['ru']['history_title'], UI_TRANSLATIONS['en']['history_title']]:
                    widget.setText(UI_TRANSLATIONS[self.current_language]['history_title'])
            
            for widget in self.history_screen.findChildren(QPushButton):
                if widget.text() in [UI_TRANSLATIONS['ru']['clear_history'], UI_TRANSLATIONS['en']['clear_history']]:
                    widget.setText(UI_TRANSLATIONS[self.current_language]['clear_history'])
        
        # Обновляем заголовки и тексты в экранах выбора языков
        if hasattr(self, 'source_language_screen') and hasattr(self, 'target_language_screen'):
            for widget in self.source_language_screen.findChildren(QLabel):
                if widget.text() in [UI_TRANSLATIONS['ru']['source_language'], UI_TRANSLATIONS['en']['source_language']]:
                    widget.setText(UI_TRANSLATIONS[self.current_language]['source_language'])
                elif widget.text() in [UI_TRANSLATIONS['ru']['target_language'], UI_TRANSLATIONS['en']['target_language']]:
                    widget.setText(UI_TRANSLATIONS[self.current_language]['target_language'])
            
            for widget in self.source_language_screen.findChildren(QLineEdit):
                widget.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['search_placeholder'])
            
            for widget in self.target_language_screen.findChildren(QLineEdit):
                widget.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['search_placeholder'])
        
        # Обновляем тексты в диалогах подтверждения
        self.delete_confirmation_text = UI_TRANSLATIONS[self.current_language]['delete_confirmation']
        self.clear_confirmation_text = UI_TRANSLATIONS[self.current_language]['clear_confirmation']

    def setup_history_screen(self):
        layout = QVBoxLayout(self.history_screen)
        
        # Создаем верхнюю панель
        top_panel = QHBoxLayout()
        
        # Заголовок
        title = QLabel(UI_TRANSLATIONS[self.current_language]['history_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_panel.addWidget(title)
        
        # Кнопка очистки истории
        clear_btn = QPushButton(UI_TRANSLATIONS[self.current_language]['clear_history'])
        clear_btn.setIcon(QIcon("icons/trash.svg"))
        clear_btn.clicked.connect(self.clear_history)
        top_panel.addWidget(clear_btn)
        
        # Кнопка закрытия
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.setFixedSize(26, 26)
        close_btn.setStyleSheet("QPushButton { background: transparent; border: none; padding: 0; cursor: pointer; } QPushButton:hover { background: #ececec; }")
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

    def setup_language_screen(self, screen, target):
        layout = QVBoxLayout(screen)
        
        # Создаем верхнюю панель
        top_panel = QHBoxLayout()
        
        # Заголовок
        title = QLabel(UI_TRANSLATIONS[self.current_language][f'{target}_language'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_panel.addWidget(title)
        
        # Кнопка закрытия
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.setFixedSize(22, 22)
        close_btn.setStyleSheet("QPushButton { background: transparent; border: none; padding: 0; cursor: pointer; } QPushButton:hover { background: #ececec; }")
        close_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_screen))
        top_panel.addWidget(close_btn)
        
        layout.addLayout(top_panel)
        
        # Создаем вертикальный layout для списка языков
        language_panel = QVBoxLayout()
        
        # Поле поиска
        search = QLineEdit()
        search.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['search_placeholder'])
        search.textChanged.connect(lambda: self.filter_languages(target))
        language_panel.addWidget(search)
        
        # Список языков
        list_widget = QListWidget()
        list_widget.itemClicked.connect(lambda item: self.select_language(target, item))
        language_panel.addWidget(list_widget)
        
        layout.addLayout(language_panel)
        
        # Сохраняем ссылки на виджеты
        if target == 'source':
            self.source_search = search
            self.source_list = list_widget
        else:
            self.target_search = search
            self.target_list = list_widget
        
        # Заполняем список языков для текущего экрана
        self.populate_language_list(target)

    def populate_language_list(self, target):
        list_widget = self.source_list if target == 'source' else self.target_list
        list_widget.clear()
        
        # Добавляем языки в список
        for code in LANGUAGE_TRANSLATIONS.keys():
            # Используем локализованные названия языков из словаря
            localized_name = LANGUAGE_TRANSLATIONS[code][self.current_language]
            list_widget.addItem(localized_name)
        
        # Устанавливаем текущий выбранный язык
        current_lang = self.source_lang_btn.text() if target == 'source' else self.target_lang_btn.text()
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == current_lang:
                list_widget.setCurrentRow(i)
                break

    def filter_languages(self, target):
        search_text = self.source_search.text().lower() if target == 'source' else self.target_search.text().lower()
        list_widget = self.source_list if target == 'source' else self.target_list
        
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setHidden(search_text not in item.text().lower())

    def show_language_selector(self, target):
        self.current_language_target = target
        # Выбираем нужный экран в зависимости от target
        screen = self.source_language_screen if target == 'source' else self.target_language_screen
        self.stack.setCurrentWidget(screen)
        
        # Обновляем заголовок и тексты
        for widget in screen.findChildren(QLabel):
            if widget.text() in [UI_TRANSLATIONS['ru'][f'{target}_language'], UI_TRANSLATIONS['en'][f'{target}_language']]:
                widget.setText(UI_TRANSLATIONS[self.current_language][f'{target}_language'])
        
        for widget in screen.findChildren(QLineEdit):
            widget.setPlaceholderText(UI_TRANSLATIONS[self.current_language]['search_placeholder'])
        
        # Обновляем список языков
        self.populate_language_list(target)

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
        source_lang = None
        target_lang = None
        
        # Ищем код языка в словаре, учитывая текущий язык интерфейса
        for code, name in LANGUAGES.items():
            if self.current_language == 'ru':
                # Для русского интерфейса ищем русские названия
                if name == self.source_lang_btn.text():
                    source_lang = code.split('_')[0]  # Берем только код языка без суффикса
                if name == self.target_lang_btn.text():
                    target_lang = code.split('_')[0]
            else:
                # Для английского интерфейса ищем английские названия
                if name == self.source_lang_btn.text():
                    source_lang = code
                if name == self.target_lang_btn.text():
                    target_lang = code
        
        if not source_lang or not target_lang:
            self.statusBar.showMessage(
                UI_TRANSLATIONS[self.current_language]['translation_error'].format('Language not found'), 
                3000
            )
            return

        # Если уже есть активный перевод, отменяем его
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()
            self.current_thread.wait()

        # Создаем и запускаем новый поток для перевода
        self.current_thread = TranslatorThread(text, source_lang, target_lang)
        self.current_thread.finished.connect(self.translation_finished)
        self.current_thread.start()
        
        self.statusBar.showMessage(UI_TRANSLATIONS[self.current_language]['translation_started'], 3000)

    def translation_finished(self, result, error):
        if error:
            self.statusBar.showMessage(
                UI_TRANSLATIONS[self.current_language]['translation_error'].format(str(error)), 
                3000
            )
        else:
            self.target_text.setPlainText(result)
            self.statusBar.showMessage(UI_TRANSLATIONS[self.current_language]['translation_completed'], 3000)
            
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
            
            # Преобразуем код языка для gTTS
            gtts_lang = lang
            if lang.endswith('_ru'):
                gtts_lang = lang.split('_')[0]
            
            # Создаем и сохраняем аудио
            tts = gTTS(text=text, lang=gtts_lang)
            tts.save(self.current_audio_file)
            
            # Воспроизводим
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()
            
            self.statusBar.showMessage(UI_TRANSLATIONS[self.current_language]['playback_started'], 3000)
            
        except Exception as e:
            self.statusBar.showMessage(
                UI_TRANSLATIONS[self.current_language]['playback_error'].format(str(e)), 
                3000
            )

    def copy_text(self, text):
        if text.strip():
            pyperclip.copy(text)
            self.statusBar.showMessage(UI_TRANSLATIONS[self.current_language]['copy_message'], 3000)

    def clear_source_text(self):
        self.source_text.clear()
        self.target_text.clear()
        self.statusBar.showMessage(UI_TRANSLATIONS[self.current_language]['clear_message'], 3000)

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
            header = QVBoxLayout()
            
            # Верхняя панель с языками и кнопкой удаления
            top_panel = QHBoxLayout()
            
            # Информация о языках
            lang_info = QLabel(f"{LANGUAGES.get(source_lang, source_lang)} → {LANGUAGES.get(target_lang, target_lang)}")
            top_panel.addWidget(lang_info)
            
            # Кнопка удаления
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/trash.svg"))
            delete_btn.setFixedSize(22, 22)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet("QPushButton { background: transparent; border: none; padding: 0; } QPushButton:hover { background: #ececec; }")
            delete_btn.clicked.connect(lambda checked, rid=rowid: self.delete_translation(rid))
            top_panel.addWidget(delete_btn)
            
            header.addLayout(top_panel)
            
            # Время
            time_info = QLabel(timestamp)
            time_info.setStyleSheet("color: #666;")
            header.addWidget(time_info)
            
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
            self.delete_confirmation_text,
            '',
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
            self.clear_confirmation_text,
            '',
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