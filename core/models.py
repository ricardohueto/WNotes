# core/models.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    name: str
    id: Optional[int] = None


@dataclass
class Note:
    title: str
    content: str
    category_id: int
    id: Optional[int] = None
