from typing import List, Optional
from pydantic import BaseModel

from app.domain.models.column import Column


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

    aliases: List[str] = []

    business_domain: Optional[str] = None

    tags: List[str] = []