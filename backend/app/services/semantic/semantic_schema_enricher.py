from typing import List
from app.domain.models.table import Table
from app.domain.semantic.semantic_table import SemanticTable


class SemanticSchemaEnricher:

    def __init__(self, data_dictionary=None):
        self.data_dictionary = data_dictionary or {}

        self.table_domain_map = {
            "accounts": "core_banking",
            "transactions": "core_banking",
            "loans": "lending",
            "loan_payments": "lending",
            "credit_cards": "cards",
            "card_transactions": "cards",
            "customers": "customer_management",
            "branches": "operations",
        }

    def enrich(self, tables: List[Table]) -> List[SemanticTable]:

        enriched = []

        for table in tables:
            enriched.append(self._enrich_table(table))

        return enriched

    def _enrich_table(self, table: Table) -> SemanticTable:

        semantic = SemanticTable(
            name=table.name,
            description=table.description,
            synonym=table.synonym,
            business_domain=self.table_domain_map.get(table.name, "unknown"),
            tags=self._generate_tags(table),
            columns=table.columns
        )

        for col in semantic.columns:
            self._enrich_column(col)

        return semantic

    def _enrich_column(self, column):

        name = column.name.lower()

        if "amount" in name or "balance" in name:
            column.description = "monetary value"

        elif "date" in name or "time" in name:
            column.description = "temporal field"

        elif name.endswith("_id"):
            column.description = "reference identifier"

        else:
            column.description = "general attribute"

    def _generate_tags(self, table: Table) -> List[str]:

        tags = []

        for col in table.columns:

            name = col.name.lower()

            if "amount" in name:
                tags.append("financial")

            if "date" in name:
                tags.append("temporal")

            if col.primary_key:
                tags.append("entity")

            if col.foreign_key:
                tags.append("relational")

        return list(set(tags))