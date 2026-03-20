"""
AirportMS - Airport Management System
Entry point
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor

from core.database import DatabaseManager
from core.app_state import AppState
from ui.main_window import MainWindow


def create_splash(app):
    """Create a styled splash screen."""
    pixmap = QPixmap(600, 300)
    pixmap.fill(QColor("#0a0e1a"))
    painter = QPainter(pixmap)
    painter.setPen(QColor("#00d4ff"))
    font = QFont("Consolas", 28, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "✈  AirportMS")
    font2 = QFont("Consolas", 11)
    painter.setFont(font2)
    painter.setPen(QColor("#4a9eff"))
    painter.drawText(0, 240, 600, 40, Qt.AlignCenter, "Airport Management System  v1.0")
    painter.setPen(QColor("#2a4a6a"))
    painter.drawText(0, 265, 600, 30, Qt.AlignCenter, "Initializing database...")
    painter.end()
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    return splash


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AirportMS")
    app.setOrganizationName("AirportMS")

    # Global dark style
    app.setStyleSheet("""
        QToolTip {
            background-color: #1a2035;
            color: #00d4ff;
            border: 1px solid #00d4ff;
            padding: 4px;
            font-size: 12px;
        }
    """)

    splash = create_splash(app)
    splash.show()
    app.processEvents()

    # Init DB
    db = DatabaseManager()
    db.initialize()

    # Init app state
    state = AppState(db)

    QTimer.singleShot(1800, splash.close)

    window = MainWindow(db, state)
    window.showFullScreen()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
