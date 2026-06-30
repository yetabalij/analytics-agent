from typing import List, Optional

from pydantic import BaseModel, Field


class ColumnMetadata(BaseModel):
    """
    Represents a single database column.
    """

    name: str = Field(
        ...,
        description="Database column name"
    )

    data_type: str = Field(
        ...,
        description="Database data type"
    )

    description: Optional[str] = Field(
        default=None,
        description="Business meaning of the column"
    )

    nullable: bool = Field(
        default=True,
        description="Whether NULL values are allowed"
    )

    primary_key: bool = Field(
        default=False,
        description="Whether this column is part of the primary key"
    )

    foreign_key: bool = Field(
        default=False,
        description="Whether this column is a foreign key"
    )

    references_table: Optional[str] = Field(
        default=None,
        description="Referenced table if foreign key"
    )

    references_column: Optional[str] = Field(
        default=None,
        description="Referenced column if foreign key"
    )

    aliases: List[str] = Field(
        default_factory=list,
        description="Alternative business names"
    )

    sample_values: List[str] = Field(
        default_factory=list,
        description="Example values"
    )

    model_config = {
        "extra": "ignore",
        "validate_assignment":True,
    }