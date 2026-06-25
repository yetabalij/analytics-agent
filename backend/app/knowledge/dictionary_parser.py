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
    matches = list(re.finditer(pattern, text))

    sections = []

    for i, match in enumerate(matches):
        table_name = match.group(1).strip().lower()
        start = match.start()

        end = matches[i + 1].start() if i < len(matches) - 1 else len(text)

        sections.append({
            "table_name": table_name,
            "raw_text": text[start:end]
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
        description = description_match.group(1).replace("\n", " ").strip()

    return {
        "synonym": synonym,
        "description": description
    }


def extract_column_text(table_text):

    # start at Column Name section
    start_match = re.search(r"Column Name", table_text)

    if not start_match:
        return ""

    start_index = start_match.start()

    # stop at next table or footer-like pattern
    end_match = re.search(
        r"\nTable Name|\nEnd of Table|\nPage \d+",
        table_text[start_index:]
    )

    if end_match:
        end_index = start_index + end_match.start()
        return table_text[start_index:end_index]

    return table_text[start_index:]


def normalize_text(text):
    text = text.replace("\r", "")
    text = re.sub(r"[ ]+", " ", text)
    return text


def clean_lines(column_text):
    lines = []

    for line in column_text.splitlines():
        line = line.strip()

        if not line:
            continue

        # remove junk markers
        if line.lower() in {"keys", "primary keys", "foreign keys"}:
            continue

        # remove table headers accidentally inside columns
        if "table name" in line.lower():
            continue

        lines.append(line)

    return lines


def merge_wrapped_lines(lines):
    merged = []

    current = ""

    datatype_pattern = re.compile(
        r'^[A-Za-z_][A-Za-z0-9_]*\s+'
        r'(INT|VARCHAR|DATE|DATETIME|TIMESTAMP|BOOLEAN|DECIMAL|ENUM|TEXT|TINYINT)',
        re.IGNORECASE
    )

    for line in lines:

        if datatype_pattern.match(line):
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
        r'^([A-Za-z_][A-Za-z0-9_]*)\s+'
        r'(INT|VARCHAR\(\d+\)|DATE|DATETIME|TIMESTAMP|BOOLEAN|'
        r'DECIMAL\(\d+,\d+\)|ENUM\(.*?\)|TEXT|TINYINT)\s*'
        r'(.*)$'
    )

    match = re.match(pattern, row.strip(), re.IGNORECASE)

    if not match:
        return None

    name = match.group(1).strip().lower()
    dtype = match.group(2).strip().lower()
    desc = match.group(3).strip()

    # 🔥 extra cleanup (prevents broken merges like "customers.custome r_id")
    desc = re.sub(r"\s+", " ", desc)

    return {
        "name": name,
        "data_type": dtype,
        "description": desc if desc else None
    }


def parse_table(table_section):

    header = parse_table_header(table_section["raw_text"])

    column_text = extract_column_text(table_section["raw_text"])

    lines = clean_lines(column_text)
    rows = merge_wrapped_lines(lines)

    columns = []
    seen = set()

    for row in rows:

        parsed = parse_column_row(row)

        if not parsed:
            continue

        # 🔥 HARD FIX: remove accidental header contamination
        if len(parsed["name"]) > 40:
            continue

        if parsed["name"] in seen:
            continue

        seen.add(parsed["name"])
        columns.append(parsed)

    return {
        "table": table_section["table_name"],
        "synonym": header["synonym"],
        "description": header["description"],
        "columns": columns
    }