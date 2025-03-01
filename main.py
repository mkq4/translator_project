import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Переводчик")
        self.setGeometry(100, 100, 500, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Введите текст...")

        # Поле вывода перевода
        self.text_output = QTextEdit(self)
        self.text_output.setPlaceholderText("Перевод...")
        self.text_output.setReadOnly(True)  # Только для чтения

        # Выпадающие списки для выбора языков
        self.from_lang = QComboBox(self)
        self.from_lang.addItems(["Русский", "Английский", "Французский"])

        self.to_lang = QComboBox(self)
        self.to_lang.addItems(["Английский", "Русский", "Французский"])

        # Кнопка перевода
        self.self.translate_button = QPushButton("Перевести", self)
        self.self.translate_button.clicked.connect(self.translate_text)

        # Метод для перевода текста
        def translate_text(self):
            input_text = self.text_input.toPlainText()
            # Здесь будет логика перевода
            translated_text = input_text  # Временная заглушка
            self.text_output.setText(translated_text)

        # Горизонтальный layout для списков языков
        langs_layout = QHBoxLayout()
        langs_layout.addWidget(self.from_lang)
        langs_layout.addWidget(self.to_lang)

        # Горизонтальный layout для ввода и вывода
        input_output_layout = QHBoxLayout()
        input_output_layout.addWidget(self.text_input)
        input_output_layout.addWidget(self.text_output)

        # Вертикальный layout (объединяет всё)
        main_layout = QVBoxLayout()
        main_layout.addLayout(langs_layout)  # Добавляем списки языков
        main_layout.addLayout(input_output_layout)  # Добавляем поля ввода/вывода
        main_layout.addWidget(self.translate_button)  # Добавляем кнопку перевода

        central_widget.setLayout(main_layout)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec())

