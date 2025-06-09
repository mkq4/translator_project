# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QPlainTextEdit
)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt

from constants import UI_TRANSLATIONS, LANGUAGES
from services.speak import speak_text

class HistoryScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # link at TranslatorApp
        self._build_ui()

    def _build_ui(self):
        self.layout = QVBoxLayout(self)

        #top bar
        top_bar = QHBoxLayout()
        self.title_label = QLabel(UI_TRANSLATIONS[self.parent.current_interface_lang]['history_title'])
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(self.title_label)
        
        self.clear_btn = QPushButton(UI_TRANSLATIONS[self.parent.current_interface_lang]['clear_history'])
        self.clear_btn.setIcon(QIcon("icons/trash.svg"))
        self.clear_btn.clicked.connect(self.parent.clear_history)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        top_bar.addWidget(self.clear_btn)
        
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.setFixedSize(26, 26)
        close_btn.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_screen))
        close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        top_bar.addWidget(close_btn)

        self.layout.addLayout(top_bar)

        #scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setSpacing(10)

        #if no history - default (no history)
        self.empty_label = QLabel(UI_TRANSLATIONS[self.parent.current_interface_lang]['no_history'])
        self.empty_label.setStyleSheet("color: #666; font-size: 14px;")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.empty_label)
        self.empty_label.hide()

        scroll.setWidget(self.container)
        self.layout.addWidget(scroll)

    def update_texts(self):
        t = UI_TRANSLATIONS[self.parent.current_interface_lang]
        self.title_label.setText(t['history_title'])
        self.clear_btn.setText(t['clear_history'])
        self.empty_label.setText(t['no_history'])
        
        #update history
        self.load_history()

    def load_history(self):
        #delete all cards
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget and widget != self.empty_label:
                widget.deleteLater()

        translations = self.parent.storage.get_translations(50)
        has_data = len(translations) > 0
        self.empty_label.setVisible(not has_data)
        self.clear_btn.setEnabled(has_data)

        if not has_data:
            return

        #current interface lang
        interface_lang = self.parent.current_interface_lang

        for idx, entry in enumerate(translations):
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

            #top string
            top = QHBoxLayout()
            #getting langs
            src_name = LANGUAGES.get(entry['source_lang'], {}).get(interface_lang, entry['source_lang'])
            tgt_name = LANGUAGES.get(entry['target_lang'], {}).get(interface_lang, entry['target_lang'])
            lang_label = QLabel(f"{src_name} → {tgt_name}")
            top.addWidget(lang_label)
            top.addStretch(1)
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("icons/trash.svg"))
            del_btn.setFixedSize(22, 22)
            del_btn.clicked.connect(lambda _, i=idx: self.parent.delete_translation(i))
            del_btn.setCursor(QCursor(Qt.PointingHandCursor))

            top.addWidget(del_btn)
            top.addStretch()

            card_layout.addLayout(top)

            #time
            time_label = QLabel(entry['timestamp'])
            time_label.setStyleSheet("color: #666;")
            card_layout.addWidget(time_label)

            #texts
            texts_layout = QHBoxLayout()

            #from text
            src_panel = QVBoxLayout()
            src_text = QPlainTextEdit()
            src_text.setPlainText(entry['source_text'])
            src_text.setReadOnly(True)
            src_text.setMaximumHeight(80)
            src_panel.addWidget(src_text)

            src_btns = QHBoxLayout()
            src_speak_btn = QPushButton()
            src_speak_btn.setIcon(QIcon("icons/speaker.svg"))
            src_speak_btn.setFixedSize(22, 22)
            src_speak_btn.clicked.connect(
                lambda _, txt=entry['source_text'], lang=entry['source_lang']: speak_text(txt, lang)
            )
            src_speak_btn.setCursor(QCursor(Qt.PointingHandCursor))
            src_btns.addWidget(src_speak_btn)

            src_copy_btn = QPushButton()
            src_copy_btn.setIcon(QIcon("icons/copy.svg"))
            src_copy_btn.setFixedSize(22, 22)
            src_copy_btn.clicked.connect(
                lambda _, txt=entry['source_text']: self.parent.copy_to_clipboard(txt)
            )
            src_copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
            src_btns.addWidget(src_copy_btn)
            src_btns.addStretch(1)

            src_panel.addLayout(src_btns)
            texts_layout.addLayout(src_panel)

            #result text
            tgt_panel = QVBoxLayout()
            tgt_text = QPlainTextEdit()
            tgt_text.setPlainText(entry['translated_text'])
            tgt_text.setReadOnly(True)
            tgt_text.setMaximumHeight(80)
            tgt_panel.addWidget(tgt_text)

            tgt_btns = QHBoxLayout()
            tgt_speak_btn = QPushButton()
            tgt_speak_btn.setIcon(QIcon("icons/speaker.svg"))
            tgt_speak_btn.setFixedSize(22, 22)
            tgt_speak_btn.clicked.connect(
                lambda _, txt=entry['translated_text'], lang=entry['target_lang']: speak_text(txt, lang)
            )
            tgt_speak_btn.setCursor(QCursor(Qt.PointingHandCursor))
            tgt_btns.addWidget(tgt_speak_btn)

            tgt_copy_btn = QPushButton()
            tgt_copy_btn.setIcon(QIcon("icons/copy.svg"))
            tgt_copy_btn.setFixedSize(22, 22)
            tgt_copy_btn.clicked.connect(
                lambda _, txt=entry['translated_text']: self.parent.copy_to_clipboard(txt)
            )
            tgt_copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
            tgt_btns.addWidget(tgt_copy_btn)
            tgt_btns.addStretch(1)

            tgt_panel.addLayout(tgt_btns)
            texts_layout.addLayout(tgt_panel)

            card_layout.addLayout(texts_layout)
            self.container_layout.addWidget(card)