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