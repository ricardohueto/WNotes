# ui/note_editor.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from core.database import DatabaseManager
from core.models import Note


class NoteEditor(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.current_note = None
        self.setObjectName("editorPanel")
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Note title...")
        self.title_input.setEnabled(False)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Start writing...")
        self.content_input.setEnabled(False)

        footer = QWidget()
        footer.setObjectName("editorFooter")
        footer.setFixedHeight(52)
        footer.setStyleSheet("""
            QWidget#editorFooter {
                border-top: 1px solid #2a2a2e;
                background-color: #1e1e24;
            }
        """)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 0, 16, 0)
        footer_layout.setSpacing(8)

        self.btn_delete = QPushButton("Delete")
        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("primaryButton")
        self.btn_delete.setEnabled(False)
        self.btn_save.setEnabled(False)

        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_delete)
        footer_layout.addWidget(self.btn_save)

        layout.addWidget(self.title_input)
        layout.addWidget(self.content_input, stretch=1)
        layout.addWidget(footer)

    def _connect_signals(self) -> None:
        self.btn_save.clicked.connect(self._on_save)
        self.btn_delete.clicked.connect(self._on_delete)
        self.title_input.textChanged.connect(self._on_content_changed)
        self.content_input.textChanged.connect(self._on_content_changed)

    def load_note(self, note: Note) -> None:
        self.current_note = note
        self._set_enabled(True)

        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)

        self.title_input.setText(note.title)
        self.content_input.setText(note.content)

        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)

        self.btn_save.setStyleSheet("")

    def clear(self) -> None:
        self.current_note = None
        self._set_enabled(False)

        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)

        self.title_input.clear()
        self.content_input.clear()

        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)

    def _set_enabled(self, enabled: bool) -> None:
        self.title_input.setEnabled(enabled)
        self.content_input.setEnabled(enabled)
        self.btn_save.setEnabled(enabled)
        self.btn_delete.setEnabled(enabled)

    def _on_content_changed(self) -> None:
        if self.current_note is None:
            return
        self.btn_save.setStyleSheet("""
            QPushButton#primaryButton {
                background-color: #9d8ff9;
            }
        """)

    def _on_save(self) -> None:
        if self.current_note is None:
            return

        title = self.title_input.text().strip()
        content = self.content_input.toPlainText()

        if not title:
            self.title_input.setPlaceholderText("Title cannot be empty")
            return

        self.current_note.title = title
        self.current_note.content = content
        self.db.update_note(self.current_note)
        self.btn_save.setStyleSheet("")

    def _on_delete(self) -> None:
        if self.current_note is None:
            return
        reply = QMessageBox.question(
            self,
            "Delete note",
            f'Delete "{self.current_note.title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_note(self.current_note.id)
            self.clear()
