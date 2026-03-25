# ui/note_editor.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from core.database import DatabaseManager
from core.models import Note


class NoteEditor(QWidget):
    note_saved = pyqtSignal(object)
    has_unsaved_changes = pyqtSignal(bool)

    AUTOSAVE_DELAY_MS = 800

    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.current_note = None
        self.setObjectName("editorPanel")

        self._autosave_timer = QTimer(self)
        self._autosave_timer.setSingleShot(True)
        self._autosave_timer.timeout.connect(self._autosave)

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

        layout.addWidget(self.title_input)
        layout.addWidget(self.content_input, stretch=1)

    def _connect_signals(self) -> None:
        self.title_input.textChanged.connect(self._on_content_changed)
        self.content_input.textChanged.connect(self._on_content_changed)

    def load_note(self, note: Note) -> None:
        # Cancel any pending save for the previous note
        if self._autosave_timer.isActive():
            self._autosave_timer.stop()
            self._flush_save()

        self.current_note = note
        self._set_enabled(True)

        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)

        self.title_input.setText(note.title)
        self.content_input.setText(note.content)

        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)

        self.has_unsaved_changes.emit(False)

    def clear(self) -> None:
        if self._autosave_timer.isActive():
            self._autosave_timer.stop()
            self._flush_save()

        self.current_note = None
        self._set_enabled(False)

        self.title_input.blockSignals(True)
        self.content_input.blockSignals(True)

        self.title_input.clear()
        self.content_input.clear()

        self.title_input.blockSignals(False)
        self.content_input.blockSignals(False)

        self.has_unsaved_changes.emit(False)

    def _set_enabled(self, enabled: bool) -> None:
        self.title_input.setEnabled(enabled)
        self.content_input.setEnabled(enabled)

    def _on_content_changed(self) -> None:
        if self.current_note is None:
            return
        self.has_unsaved_changes.emit(True)
        self._autosave_timer.start(self.AUTOSAVE_DELAY_MS)

    def _autosave(self) -> None:
        self._flush_save()

    def _flush_save(self) -> None:
        """Immediately saves the current note if one is loaded. Safe to call anytime."""
        if self.current_note is None:
            return

        title = self.title_input.text().strip()
        content = self.content_input.toPlainText()

        if not title:
            return  # Don't save with empty title

        self.current_note.title = title
        self.current_note.content = content
        self.db.update_note(self.current_note)
        self.has_unsaved_changes.emit(False)
        self.note_saved.emit(self.current_note)