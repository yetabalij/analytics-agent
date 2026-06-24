import re

def extract_table_section(text):
    pattern = r"Table Name\s+([^\n]+)"

    matches = list(re.finditer(pattern,text))

    sections = []

    for i, match in enumerate(matches):

        table_name = match.group(1).strip()
        start = match.start()

        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(text)

        table_text = text[start:end]

        sections.append({
            "table_name": table_name.lower(),
            "raw_text": table_text
        })
    
    return sections


def parse_table_header(table_text):
        
    synonym = None
    description = None

    synonym_match = re.search(r"Table Synonym\s+([^\n]+)", table_text)

    if synonym_match:
        synonym = synonym_match.group(1).strip()
        
    description_match = re.search(
        r"Table Comments\s+(.+?)(?:Column Name)",
        table_text,
        re.DOTALL
    )

    if description_match:
        description = (
            description_match
            .group(1)
            .replace("\n", " ")
            .strip()
        )

    return {
        "synonym": synonym,
        "description": description
    }