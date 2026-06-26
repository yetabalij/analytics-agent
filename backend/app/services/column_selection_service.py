class ColumnSelector:

    def select_columns(self, question, table):

        question = question.lower()
        columns = table["columns"]

        selected = set()

        for col in columns:
            name = col["name"].lower()

            # direct match
            if name in question:
                selected.add(col["name"])

            # heuristics
            if "date" in question and "date" in name:
                selected.add(col["name"])

            if "branch" in question and "branch" in name:
                selected.add(col["name"])

            if "account" in question and "account" in name:
                selected.add(col["name"])

            if "customer" in question and "customer" in name:
                selected.add(col["name"])

        return list(selected)