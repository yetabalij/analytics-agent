from pydantic import BaseModel


class Relationship(BaseModel):
    """
    Represents a foreign-key relationship.
    """

    source_table: str

    source_column: str

    target_table: str

    target_column: str