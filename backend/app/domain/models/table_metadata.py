from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.models.column_metadata import ColumnMetadata


class TableMetadata(BaseModel):
    """
    Represents a database table.
    """

    name: str = Field(
        ...,
        description="Database table name"
    )

    synonym: Optional[str] = Field(
        default=None,
        description="Business synonym or short name"
    )

    description: Optional[str] = Field(
        default=None,
        description="Business description of the table"
    )

    columns: List[ColumnMetadata] = Field(
        default_factory=list,
        description="Columns belonging to this table"
    )

    primary_keys: List[str] = Field(
        default_factory=list,
        description="Primary key column names"
    )

    foreign_keys: List[str] = Field(
        default_factory=list,
        description="Foreign key column names"
    )

    aliases: List[str] = Field(
        default_factory=list,
        description="Alternative business names"
    )

    business_domain: Optional[str] = Field(
        default=None,
        description="Business domain such as Customer, Loan, Account"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Search tags"
    )

    model_config = {
        "extra": "ignore",
        "validate_assignment": True,
    }