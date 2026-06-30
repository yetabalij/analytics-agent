from typing import Optional

from pydantic import BaseModel


class Column(BaseModel):
    """
    Represents one database column.
    """

    name: str

    data_type: str

    nullable: bool = True

    description: Optional[str] = None

    primary_key: bool = False

    foreign_key: bool = False

    references_table: Optional[str] = None

    references_column: Optional[str] = None