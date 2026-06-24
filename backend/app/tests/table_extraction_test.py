from app.knowledge.pdf_parser import extract_pdf_text
from app.knowledge.dictionary_parser import extract_table_section, parse_table_header

text = extract_pdf_text("app/knowledge/dictionary/dictionary.pdf")

tables = extract_table_section(text)

print(f"Found {len(tables)} tables")

#for table in tables[:5]:
    #print(table["table_name"])



#Test Header Parsing

customers = tables[0]

header = parse_table_header(customers["raw_text"])

print(header)