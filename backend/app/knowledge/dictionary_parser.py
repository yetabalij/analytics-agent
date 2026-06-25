import re
import pdfplumber

def extract_pdf_text(pdf_path):

    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)   
            
    return "\n".join(all_text)


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

def extract_column_text(table_text):

    match = re.search(
        r"Column Name.*?Foreign.*?\n(.*)",
        table_text,
        re.DOTALL
    )

    if not match:
        return ""

    return match.group(1)

def normalize_text(text):

    text = text.replace("\r", "")

    #remove repeated spaces

    text = re.sub(r"[ ]+", " ", text)

    return text


def clean_lines(column_text):

    lines = []

    for line in column_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.lower() == "keys":
            continue

        lines.append(line)

    return lines

def merge_wrapped_lines(lines):

    merged = []

    current = ""

    datatype_pattern = (
        r'^(?:'
        r'[A-Za-z_][A-Za-z0-9_]*'
        r')\s+'
        r'(?:'
        r'INT|VARCHAR|DATE|DATETIME|TIMESTAMP|'
        r'BOOLEAN|DECIMAL|ENUM|TEXT'
        r')'
    )

    for line in lines:

        if re.match(
            datatype_pattern,
            line,
            re.IGNORECASE
        ):

            if current:
                merged.append(current)

            current = line

        else:
            current += " " + line

    if current:
        merged.append(current)

    return merged

def parse_column_row(row):

    pattern = (
        r'^'
        r'([A-Za-z_][A-Za-z0-9_]*)'
        r'\s+'
        r'('
        r'INT'
        r'|DATE'
        r'|DATETIME'
        r'|TIMESTAMP'
        r'|BOOLEAN'
        r'|TEXT'
        r'|VARCHAR\(\d+\)'
        r'|DECIMAL\(\d+,\d+\)'
        r'|ENUM\(.*?\)'
        r')'
        r'\s*(.*)$'
    )

    match = re.match(
        pattern,
        row,
        re.IGNORECASE
    )

    if not match:
        return None

    return {
        "name": match.group(1).strip().lower(),
        "data_type": match.group(2).strip(),
        "description": match.group(3).strip()
    }

def parse_table(table_section):

    header = parse_table_header(
        table_section["raw_text"]
    )

    column_text = extract_column_text(
        table_section["raw_text"]
    )

    lines = clean_lines(column_text)

    rows = merge_wrapped_lines(lines)

    columns = []
    seen = set()

    for row in rows:

        parsed = parse_column_row(row)

        if not parsed:
            continue

        col_name = parsed["name"]

        if col_name in seen:
            continue

        seen.add(col_name)
        columns.append(parsed)

    return {
        "table": table_section["table_name"],
        "synonym": header["synonym"],
        "description": header["description"],
        "columns": columns
    }