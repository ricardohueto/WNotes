# ui/category_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QInputDialog, QMessageBox, QMenu
)
from PyQt6.QtCore import pyqtSignal, Qt
from core.database import DatabaseManager
from core.models import Category


class CategoryPanel(QWidget):
    category_selected = pyqtSignal(int)

    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.setObjectName("leftPanel")
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Categories")
        title.setObjectName("sectionTitle")

        self.list_widget = QListWidget()

        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)

        self.btn_new = QPushButton("+ New category")
        self.btn_new.setFixedHeight(38)
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
                background-color: #7c6af708;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_new)

    def _connect_signals(self) -> None:
        self.list_widget.currentItemChanged.connect(self._on_category_changed)
        self.list_widget.itemDoubleClicked.connect(self._on_rename_category)
        self.btn_new.clicked.connect(self._on_new_category)

    def load_categories(self) -> None:
        self.list_widget.clear()
        categories = self.db.get_all_categories()
        for category in categories:
            self._add_category_item(category)

    def _add_category_item(self, category: Category) -> QListWidgetItem:
        item = QListWidgetItem(category.name)
        item.setData(Qt.ItemDataRole.UserRole, category.id)
        self.list_widget.addItem(item)
        return item

    def _on_category_changed(self, current: QListWidgetItem) -> None:
        if current is None:
            return
        category_id = current.data(Qt.ItemDataRole.UserRole)
        self.category_selected.emit(category_id)

    def _on_new_category(self) -> None:
        name, ok = QInputDialog.getText(
            self, "New category", "Category name:"
        )
        if ok and name.strip():
            category = self.db.create_category(name.strip())
            item = self._add_category_item(category)
            self.list_widget.setCurrentItem(item)

    def _on_rename_category(self, item: QListWidgetItem) -> None:
        current_name = item.text()
        name, ok = QInputDialog.getText(
            self, "Rename category", "New name:", text=current_name
        )
        if ok and name.strip():
            category_id = item.data(Qt.ItemDataRole.UserRole)
            category = Category(id=category_id, name=name.strip())
            self.db.update_category(category)
            item.setText(name.strip())

    def _on_delete_category(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        name = item.text()
        reply = QMessageBox.question(
            self,
            "Delete category",
            f'Delete "{name}" and all its notes?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            category_id = item.data(Qt.ItemDataRole.UserRole)
            self.db.delete_category(category_id)
            self.list_widget.takeItem(self.list_widget.row(item))

    def _show_context_menu(self, position) -> None:
        item = self.list_widget.itemAt(position)
        if item is None:
            return
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        action = menu.exec(self.list_widget.mapToGlobal(position))
        if action == rename_action:
            self._on_rename_category(item)
        elif action == delete_action:
            self._on_delete_category()