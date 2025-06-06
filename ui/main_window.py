from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QPlainTextEdit, QStatusBar, QStackedWidget, QLabel,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

import gtts.lang

from constants import UI_TRANSLATIONS, LANGUAGES
from services.storage import TranslationsStorage
from services.translate import TranslatorThread
from services.speak import speak_text

from ui.history_screen import HistoryScreen
from ui.language_selector import LanguageSelector

gtts_langs = gtts.lang.tts_langs()

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        #default langs
        self.source_lang_code = 'en' 
        self.target_lang_code = 'ru'

        #interface lang
        self.current_interface_lang = 'ru'

        #storage
        self.storage = TranslationsStorage()

        #timers
        self.translation_timer = QTimer()
        self.translation_timer.setSingleShot(True)
        self.translation_timer.timeout.connect(self.do_translation)

        #thread translate 
        self.translation_thread = None

        #screens stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        #creating screens
        self.main_screen = QWidget()
        self.history_screen = HistoryScreen(self)
        self.source_lang_selector = LanguageSelector(self, 'source')
        self.target_lang_selector = LanguageSelector(self, 'target')

        #setting up ui
        self.setup_main_screen()
        self.stack.addWidget(self.main_screen)
        self.stack.addWidget(self.history_screen)
        self.stack.addWidget(self.source_lang_selector)
        self.stack.addWidget(self.target_lang_selector)

        #main screen as base
        self.stack.setCurrentWidget(self.main_screen)
        self.update_interface_texts()
        self.update_speaker_buttons()

    def setup_main_screen(self):
        self.setWindowTitle(UI_TRANSLATIONS[self.current_interface_lang]['window_title'])
        self.setGeometry(100, 100, 700, 300)
        layout = QVBoxLayout(self.main_screen)

        #langs select
        lang_panel = QHBoxLayout()
        lang_panel.addStretch()

        self.src_btn = QPushButton(LANGUAGES[self.source_lang_code][self.current_interface_lang])
        self.src_btn.setFixedWidth(150)
        self.src_btn.clicked.connect(lambda: self.show_language_selector('source'))

        swap_btn = QPushButton("⇄")
        swap_btn.setFixedWidth(40)
        swap_btn.clicked.connect(self.swap_languages)

        self.tgt_btn = QPushButton(LANGUAGES[self.target_lang_code][self.current_interface_lang])
        self.tgt_btn.setFixedWidth(150)
        self.tgt_btn.clicked.connect(lambda: self.show_language_selector('target'))

        lang_panel.addWidget(self.src_btn)
        lang_panel.addWidget(swap_btn)
        lang_panel.addWidget(self.tgt_btn)
        lang_panel.addStretch()
        layout.addLayout(lang_panel)

        texts_layout = QHBoxLayout()

        # left col
        left_layout = QVBoxLayout()

        self.source_text = QPlainTextEdit()
        self.source_text.setPlaceholderText(UI_TRANSLATIONS[self.current_interface_lang]['source_placeholder'])
        self.source_text.textChanged.connect(self.on_source_text_changed)
        left_layout.addWidget(self.source_text)

        src_buttons = QHBoxLayout()
        self.src_speak_btn = QPushButton()
        self.src_speak_btn.setIcon(QIcon("icons/speaker.svg"))
        self.src_speak_btn.clicked.connect(self.speak_source)
        src_buttons.addWidget(self.src_speak_btn)

        self.src_copy_btn = QPushButton()
        self.src_copy_btn.setIcon(QIcon("icons/copy.svg"))
        self.src_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.source_text.toPlainText()))
        src_buttons.addWidget(self.src_copy_btn)

        self.clear_src_btn = QPushButton()
        self.clear_src_btn.setIcon(QIcon("icons/clear.svg"))
        self.clear_src_btn.clicked.connect(self.clear_source_text)
        src_buttons.addWidget(self.clear_src_btn)

        src_buttons.addStretch()
        left_layout.addLayout(src_buttons)

        texts_layout.addLayout(left_layout)

        # rght col
        right_layout = QVBoxLayout()

        self.target_text = QPlainTextEdit()
        self.target_text.setPlaceholderText(UI_TRANSLATIONS[self.current_interface_lang]['target_placeholder'])
        self.target_text.setReadOnly(True)
        right_layout.addWidget(self.target_text)

        tgt_buttons = QHBoxLayout()
        self.tgt_speak_btn = QPushButton()
        self.tgt_speak_btn.setIcon(QIcon("icons/speaker.svg"))
        self.tgt_speak_btn.clicked.connect(self.speak_target)
        tgt_buttons.addWidget(self.tgt_speak_btn)

        self.tgt_copy_btn = QPushButton()
        self.tgt_copy_btn.setIcon(QIcon("icons/copy.svg"))
        self.tgt_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.target_text.toPlainText()))
        tgt_buttons.addWidget(self.tgt_copy_btn)

        self.history_btn = QPushButton()
        self.history_btn.setIcon(QIcon("icons/history.svg"))
        self.history_btn.clicked.connect(self.show_history)
        tgt_buttons.addWidget(self.history_btn)

        tgt_buttons.addStretch()
        right_layout.addLayout(tgt_buttons)

        texts_layout.addLayout(right_layout)
        layout.addLayout(texts_layout)

        #status bar && interface lang
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.interface_lang_label = QLabel(UI_TRANSLATIONS[self.current_interface_lang]['interface_language'])
        self.interface_lang_label.setStyleSheet('font-size: 11px; padding-right: 4px;')
        self.status_bar.addPermanentWidget(self.interface_lang_label)

        self.btn_ru = QPushButton('Русский')
        self.btn_en = QPushButton('English')
        self.btn_ru.setStyleSheet('font-size: 11px; min-width: 60px;')
        self.btn_en.setStyleSheet('font-size: 11px; min-width: 60px;')
        self.btn_ru.clicked.connect(lambda: self.change_interface_lang('ru'))
        self.btn_en.clicked.connect(lambda: self.change_interface_lang('en'))
        self.status_bar.addPermanentWidget(self.btn_ru)
        self.status_bar.addPermanentWidget(self.btn_en)

        self.update_lang_buttons()

    def update_interface_texts(self):
        t = UI_TRANSLATIONS[self.current_interface_lang]
        self.setWindowTitle(t['window_title'])

        #update placeholders
        if not self.source_text.toPlainText():
            self.source_text.setPlaceholderText(t['source_placeholder'])

        if not self.target_text.toPlainText():
            self.target_text.setPlaceholderText(t['target_placeholder'])

        #update some text
        self.interface_lang_label.setText(t['interface_language'])

        self.btn_ru.setText('Русский')
        self.btn_en.setText('English')
        self.update_lang_buttons()

        #update text button lang
        self.src_btn.setText(LANGUAGES[self.source_lang_code][self.current_interface_lang])
        self.tgt_btn.setText(LANGUAGES[self.target_lang_code][self.current_interface_lang])

        #update text at other langs
        self.history_screen.update_texts()
        self.source_lang_selector.update_texts()
        self.target_lang_selector.update_texts()

    def update_lang_buttons(self):
        if self.current_interface_lang == 'ru':
            self.btn_ru.setEnabled(False)
            self.btn_en.setEnabled(True)
        else:
            self.btn_ru.setEnabled(True)
            self.btn_en.setEnabled(False)

    def change_interface_lang(self, lang_code):
        """
        Changes UI lang and updates texts.
        """
        self.current_interface_lang = lang_code
        self.update_interface_texts()

        previous = self.stack.currentWidget()
        
        if previous != self.main_screen:  # workaround
            self.stack.setCurrentWidget(self.main_screen)    
        else:
            self.stack.setCurrentWidget(self.history_screen)

        self.stack.setCurrentWidget(previous)

    def on_source_text_changed(self):
        self.translation_timer.start(500)
        self.update_speaker_buttons()

    def do_translation(self):
        text = self.source_text.toPlainText()
        if len(text.strip()) > 0:  # show msg if text not empty
            if self.translation_thread and self.translation_thread.isRunning():
                self.translation_thread.terminate()

            self.status_bar.showMessage(
                UI_TRANSLATIONS[self.current_interface_lang]['translation_started'], 2000
            )

            self.translation_thread = TranslatorThread(text, self.source_lang_code, self.target_lang_code)
            self.translation_thread.finished.connect(self.on_translation_finished)
            self.translation_thread.start()

    def on_translation_finished(self, translated_text, exception):
        if exception:
            self.status_bar.showMessage(
                UI_TRANSLATIONS[self.current_interface_lang]['translation_error'].format(str(exception)),
                3000
            )
            self.target_text.setPlainText("")
            return

        self.target_text.setPlainText(translated_text)
        self.status_bar.showMessage(
            UI_TRANSLATIONS[self.current_interface_lang]['translation_completed'], 2000
        )
        # Сохраняем в историю
        self.storage.save_translation(
            self.source_text.toPlainText(),
            translated_text,
            self.source_lang_code,
            self.target_lang_code        
        )
        self.update_speaker_buttons()

    def speak_source(self):
        lang = self.source_lang_code        
        speak_text(
            self.source_text.toPlainText(),
            lang,
            on_status=lambda msg: self.status_bar.showMessage(
                UI_TRANSLATIONS[self.current_interface_lang].get(msg, msg), 2000
            )
        )

    def speak_target(self):
        lang = self.target_lang_code        
        speak_text(
            self.target_text.toPlainText(),
            lang,
            on_status=lambda msg: self.status_bar.showMessage(
                UI_TRANSLATIONS[self.current_interface_lang].get(msg, msg), 2000
            )
        )

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.status_bar.showMessage(
            UI_TRANSLATIONS[self.current_interface_lang]['copy_message'], 2000
        )

    def clear_source_text(self):
        self.source_text.clear()
        self.target_text.clear()
        self.status_bar.showMessage(
            UI_TRANSLATIONS[self.current_interface_lang]['clear_message'], 2000
        )
        self.update_speaker_buttons()

    def show_history(self):
        self.history_screen.load_history()
        self.stack.setCurrentWidget(self.history_screen)

    def show_language_selector(self, which):
        if which == 'source':
            self.source_lang_selector.populate_language_list(self.source_lang_code)
            self.stack.setCurrentWidget(self.source_lang_selector)
        else:
            self.target_lang_selector.populate_language_list(self.target_lang_code)
            self.stack.setCurrentWidget(self.target_lang_selector)

    def swap_languages(self):
        self.source_lang_code, self.target_lang_code = self.target_lang_code, self.source_lang_code
        self.src_btn.setText(LANGUAGES[self.source_lang_code][self.current_interface_lang])
        self.tgt_btn.setText(LANGUAGES[self.target_lang_code][self.current_interface_lang])
        self.source_text.clear()
        self.target_text.clear()
        self.update_speaker_buttons()

    def update_speaker_buttons(self): #active or not speaker buttons
        src_supported = self.source_lang_code in gtts_langs
        tgt_supported = self.target_lang_code in gtts_langs

        src_text = self.source_text.toPlainText().strip()
        tgt_text = self.target_text.toPlainText().strip()

        self.src_speak_btn.setEnabled(src_supported and bool(src_text))
        self.tgt_speak_btn.setEnabled(tgt_supported and bool(tgt_text))

        #hints
        if not src_supported:
            self.src_speak_btn.setToolTip(UI_TRANSLATIONS[self.current_interface_lang]['tts_not_supported'])
        elif not src_text:
            self.src_speak_btn.setToolTip(UI_TRANSLATIONS[self.current_interface_lang]['no_text'])
        else:
            self.src_speak_btn.setToolTip("")

        if not tgt_supported:
            self.tgt_speak_btn.setToolTip(UI_TRANSLATIONS[self.current_interface_lang]['tts_not_supported'])
        elif not tgt_text:
            self.tgt_speak_btn.setToolTip(UI_TRANSLATIONS[self.current_interface_lang]['no_text'])
        else:
            self.tgt_speak_btn.setToolTip("")

    def change_selected_language(self, which, lang_code):
        if which == 'source':
            self.source_lang_code = lang_code
            self.src_btn.setText(LANGUAGES[lang_code][self.current_interface_lang])
        else:
            self.target_lang_code = lang_code
            self.tgt_btn.setText(LANGUAGES[lang_code][self.current_interface_lang])

        self.stack.setCurrentWidget(self.main_screen)
        self.on_source_text_changed()

    def delete_history_item(self, index):
        self.storage.delete_translation(index)
        self.history_screen.load_history()

    def clear_history(self):
        self.storage.clear_translations()
        self.history_screen.load_history()

    def closeEvent(self, event):
        event.accept()

    def delete_translation(self, index: int):
        self.storage.delete_translation(index)
        self.history_screen.load_history()