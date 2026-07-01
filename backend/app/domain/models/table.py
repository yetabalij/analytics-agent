from typing import List, Optional

from pydantic import BaseModel

from app.domain.models.column import Column
from app.domain.models.relationship import Relationship


class Table(BaseModel):
    """
    Represents one database table.
    """

    name: str

    description: Optional[str] = None

    synonym: Optional[str] = None

    columns: List[Column] = []

    primary_keys: List[str] = []

    foreign_keys: List[str] = []

    relationships: List[Relationship] = []