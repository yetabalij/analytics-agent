from typing import List, Optional
from pydantic import BaseModel
from app.domain.models.column import Column


class SemanticTable(BaseModel):
    """
    Enriched version of Table with business meaning.
    """

    name: str

    description: Optional[str] = None

    synonym: Optional[str] = None

    business_domain: str = "unknown"

    tags: List[str] = []

    columns: List[Column] = []