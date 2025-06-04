# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from constants import UI_TRANSLATIONS, LANGUAGES

class LanguageSelector(QWidget):
    def __init__(self, parent, target: str):
        """
        target: 'source' или 'target'
        parent: экземпляр TranslatorApp
        """
        super().__init__()
        self.parent = parent
        self.target = target
        self._build_ui()

    def _build_ui(self):
        self.layout = QVBoxLayout(self)

        # Верхний бар: заголовок экрана и кнопка закрыть
        top_bar = QHBoxLayout()
        key = 'source_language' if self.target == 'source' else 'target_language'
        self.title_label = QLabel(UI_TRANSLATIONS[self.parent.current_interface_lang][key])
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(self.title_label)

        top_bar.addStretch(1)
        
        close_btn = QPushButton()
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.setFixedSize(26, 26)
        close_btn.clicked.connect(lambda: self.parent.stack.setCurrentWidget(self.parent.main_screen))
        top_bar.addWidget(close_btn)

        self.layout.addLayout(top_bar)

        # Строка поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            UI_TRANSLATIONS[self.parent.current_interface_lang]['search_placeholder']
        )
        self.search_input.textChanged.connect(self._filter_languages)
        self.layout.addWidget(self.search_input)

        # Список языков
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._select_language)
        self.layout.addWidget(self.list_widget)

        # Заполняем список всеми языками
        self.populate_language_list(self._get_current_code())

    def update_texts(self):
        """
        При смене языка интерфейса изменяем плейсхолдеры, заголовок и список языков.
        """
        t = UI_TRANSLATIONS[self.parent.current_interface_lang]
        key = 'source_language' if self.target == 'source' else 'target_language'
        self.title_label.setText(t[key])
        self.search_input.setPlaceholderText(t['search_placeholder'])
        # Перезаполняем список с локализованными названиями
        self.populate_language_list(self._get_current_code())

    def populate_language_list(self, current_code: str = ""):
        self.list_widget.clear()
        
        # Текущий язык интерфейса
        interface_lang = self.parent.current_interface_lang
        
        # Сортируем языки по локализованным названиям
        sorted_items = sorted(
            LANGUAGES.items(),
            key=lambda x: x[1][interface_lang].lower()
        )
        # Перемещаем текущий язык в начало
        sorted_items = sorted(
            sorted_items,
            key=lambda x: x[0] != current_code
        )

        for code, names in sorted_items:
            # Используем название на текущем языке интерфейса
            name = names.get(interface_lang, code)
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, code)
            self.list_widget.addItem(item)
            if code == current_code:
                item.setSelected(True)

    def _get_current_code(self) -> str:
        """
        Возвращает текущий код языка для данного target (source/target).
        """
        if self.target == 'source':
            return self.parent.source_lang_code
        else:
            return self.parent.target_lang_code

    def _filter_languages(self, text: str):
        """
        Скрытие / показ элементов списка по совпадению с текстом поиска.
        """
        lower = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            name = item.text().lower()
            item.setHidden(lower not in name)

    def _select_language(self, item: QListWidgetItem):
        try:
            code = item.data(Qt.UserRole)
            if code is None:
                return
            # Текущий язык интерфейса
            interface_lang = self.parent.current_interface_lang
            if self.target == 'source':
                if code == self.parent.target_lang_code:
                    self.parent.swap_languages()
                else:
                    self.parent.source_lang_code = code
                    self.parent.src_btn.setText(LANGUAGES.get(code, {}).get(interface_lang, code))
            else:
                if code == self.parent.source_lang_code:
                    self.parent.swap_languages()
                else:
                    self.parent.target_lang_code = code
                    self.parent.tgt_btn.setText(LANGUAGES.get(code, {}).get(interface_lang, code))
            self.parent.update_speaker_buttons()
            self.parent.stack.setCurrentWidget(self.parent.main_screen)
            self.parent.on_source_text_changed()
        except Exception as e:
            print(f"Error in _select_language: {e}")
        finally:
            self.search_input.setText("")