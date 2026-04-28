#!/usr/bin/env python3
"""
GitHub Commander - Main Entry Point
A comprehensive GitHub desktop application for Linux
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GitHub Commander")
    app.setOrganizationName("GitHub Commander")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
