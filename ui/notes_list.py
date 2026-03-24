# ui/notes_list.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMenu, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from core.database import DatabaseManager
from core.models import Note


class NotesList(QWidget):
    note_selected = pyqtSignal(object)
    note_deleted = pyqtSignal()

    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.current_category_id = None
        self.setObjectName("centerPanel")
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title = QLabel("Notes")
        self.title.setObjectName("sectionTitle")

        self.list_widget = QListWidget()

        self.list_widget.setStyleSheet("""
            QListWidget {
                outline: 0;
            }
            QListWidget::item:selected,
            QListWidget::item:selected:active,
            QListWidget::item:selected:!active {
                background-color: #3d3472;
                color: #a99df5;
                border-left: 2px solid #7c6af7;
            }
        """)

        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)

        self.btn_new = QPushButton("+ New note")
        self.btn_new.setFixedHeight(38)
        self.btn_new.setEnabled(False)
        self.btn_new.setStyleSheet("""
            QPushButton {
                border: none;
                border-top: 1px solid #2a2a2e;
                border-radius: 0px;
                color: #5a5a6e;
                font-size: 12px;
                text-align: left;
                padding-left: 14px;
            }
            QPushButton:hover {
                color: #7c6af7;
                background-color: #e8e8f5;
            }
            QPushButton:disabled {
                color: #2a2a2e;
            }
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_new)

    def _connect_signals(self) -> None:
        self.list_widget.currentItemChanged.connect(self._on_note_changed)
        self.btn_new.clicked.connect(self._on_new_note)

    def load_notes(self, category_id: int) -> None:
        self.current_category_id = category_id
        self.list_widget.clear()
        self.btn_new.setEnabled(True)
        self.title.setText("Notes")
        notes = self.db.get_notes_by_category(category_id)
        if not notes:
            self._on_new_note()
        else:
            for note in notes:
                self._add_note_item(note)
            QTimer.singleShot(0, lambda: self.list_widget.setCurrentRow(0))

    def _add_note_item(self, note: Note) -> QListWidgetItem:
        item = QListWidgetItem(note.title)
        item.setData(Qt.ItemDataRole.UserRole, note)
        self.list_widget.addItem(item)
        return item

    def _on_note_changed(self, current: QListWidgetItem) -> None:
        if current is None:
            return
        note = current.data(Qt.ItemDataRole.UserRole)
        self.note_selected.emit(note)

    def _on_new_note(self) -> None:
        if self.current_category_id is None:
            return
        note = Note(
            title="New note",
            content="",
            category_id=self.current_category_id
        )
        note = self.db.create_note(note)
        item = self._add_note_item(note)
        self.list_widget.setCurrentItem(item)

    def _on_delete_note(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        note = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Delete note",
            f'Delete "{note.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_note(note.id)
            self.list_widget.takeItem(self.list_widget.row(item))
            self.note_deleted.emit()

    def _show_context_menu(self, position) -> None:
        item = self.list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        action = menu.exec(self.list_widget.mapToGlobal(position))
        if action == delete_action:
            self._on_delete_note()

    def update_current_note_title(self, note: object) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        item.setText(note.title)
        item.setData(Qt.ItemDataRole.UserRole, note)
