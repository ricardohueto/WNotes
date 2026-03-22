# core/database.py
import sqlite3
from pathlib import Path
from core.models import Category, Note

DB_PATH = Path(__file__).parent.parent / "data" / "wnotes.db"


class DatabaseManager:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                content     TEXT NOT NULL DEFAULT '',
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                    ON DELETE CASCADE
            )
        """)
        self.connection.commit()

    # ── Categories ──────────────────────────────────────────

    def get_all_categories(self) -> list[Category]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        return [Category(id=row["id"], name=row["name"]) for row in cursor.fetchall()]

    def create_category(self, name: str) -> Category:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.connection.commit()
        return Category(id=cursor.lastrowid, name=name)

    def update_category(self, category: Category) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (category.name, category.id)
        )
        self.connection.commit()

    def delete_category(self, category_id: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.connection.commit()

    # ── Notes ────────────────────────────────────────────────

    def get_notes_by_category(self, category_id: int) -> list[Note]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, title, content, category_id FROM notes WHERE category_id = ? ORDER BY title",
            (category_id,)
        )
        return [
            Note(id=row["id"], title=row["title"], content=row["content"], category_id=row["category_id"])
            for row in cursor.fetchall()
        ]

    def create_note(self, note: Note) -> Note:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, category_id) VALUES (?, ?, ?)",
            (note.title, note.content, note.category_id)
        )
        self.connection.commit()
        note.id = cursor.lastrowid
        return note

    def update_note(self, note: Note) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
            (note.title, note.content, note.id)
        )
        self.connection.commit()

    def delete_note(self, note_id: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()