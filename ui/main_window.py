# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from core.database import DatabaseManager
from ui.category_panel import CategoryPanel
from ui.notes_list import NotesList
from ui.note_editor import NoteEditor
from core.utils import get_resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()

    def _setup_window(self) -> None:
        self.setWindowTitle("WNotes")
        self.setMinimumSize(800, 540)
        self.resize(1100, 680)

        icon_path = get_resource_path("assets/icons/icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))  # ← añade esta línea


    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.category_panel = CategoryPanel(self.db)
        self.notes_list = NotesList(self.db)
        self.note_editor = NoteEditor(self.db)

        self.splitter.addWidget(self.category_panel)
        self.splitter.addWidget(self.notes_list)
        self.splitter.addWidget(self.note_editor)

        self.splitter.setSizes([200, 240, 660])
        self.splitter.setChildrenCollapsible(False)

        main_layout.addWidget(self.splitter)

    # ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from core.database import DatabaseManager
from ui.category_panel import CategoryPanel
from ui.notes_list import NotesList
from ui.note_editor import NoteEditor
from core.utils import get_resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()

    def _setup_window(self) -> None:
        self.setWindowTitle("WNotes")
        self.setMinimumSize(800, 540)
        self.resize(1100, 680)

        icon_path = get_resource_path("assets/icons/icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))  # ← añade esta línea


    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.category_panel = CategoryPanel(self.db)
        self.notes_list = NotesList(self.db)
        self.note_editor = NoteEditor(self.db)

        self.splitter.addWidget(self.category_panel)
        self.splitter.addWidget(self.notes_list)
        self.splitter.addWidget(self.note_editor)

        self.splitter.setSizes([200, 240, 660])
        self.splitter.setChildrenCollapsible(False)

        main_layout.addWidget(self.splitter)

    def _connect_signals(self) -> None:
        self.category_panel.category_selected.connect(self.notes_list.load_notes)
        self.category_panel.category_selected.connect(self.note_editor.clear)
        self.notes_list.note_selected.connect(self.note_editor.load_note)
        self.notes_list.note_deleted.connect(self.note_editor.clear)
        self.note_editor.note_saved.connect(self.notes_list.update_current_note_title)
        self.note_editor.has_unsaved_changes.connect(self._on_unsaved_changes)

    def _on_unsaved_changes(self, has_changes: bool) -> None:
        self.setWindowTitle("● WNotes" if has_changes else "WNotes")

    def closeEvent(self, event) -> None:
        self.db.close()
        event.accept()

    def _load_initial_data(self) -> None:
        self.category_panel.load_categories()

    def closeEvent(self, event) -> None:
        self.db.close()
        event.accept()