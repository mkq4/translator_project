# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import TranslatorApp

def main():
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
