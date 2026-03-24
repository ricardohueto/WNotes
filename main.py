# main.py
import sys
from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from ui.main_window import MainWindow
from core.utils import get_resource_path

def get_resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path


def load_stylesheet(app: QApplication) -> None:
    qss_path = get_resource_path("styles/theme.qss")
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("WNotes")
    app.setOrganizationName("WNotes")

    icon_path = get_resource_path("assets/icons/icon.ico")
    app.setWindowIcon(QIcon(str(icon_path)))

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
