from app.knowledge.pdf_parser import extract_pdf_text
from app.knowledge.dictionary_parser import (
    extract_table_section, 
    parse_table_header, 
    extract_column_text, 
    normalize_text, 
    clean_lines, 
    merge_wrapped_lines, 
    parse_column_row,
    extract_table_section,
    parse_table)

text = extract_pdf_text("app/knowledge/dictionary/dictionary.pdf")

tables = extract_table_section(text)

#print(f"Found {len(tables)} tables")

#for table in tables[:5]:
    #print(table["table_name"])



#Test Header Parsing

customers = tables[0]

header = parse_table_header(customers["raw_text"])

#print(header)

#Extract Column Text

column_text = extract_column_text(tables[0]["raw_text"])

#for i, line in enumerate(column_text.splitlines()[:50]):
    #print(f"{i+1}: {repr(line)}")


#Normalize text

clean_text = normalize_text(column_text)

#print(clean_text[:1000])

column_text = extract_column_text(
    tables[0]["raw_text"]
)

lines = clean_lines(column_text)

rows = merge_wrapped_lines(lines)

#for row in rows[:10]:
    #print(row)


#for row in rows[:10]:
    #print(parse_column_row(row))

tables = extract_table_section(text)

customer_table = parse_table(tables[0])

print(customer_table)


