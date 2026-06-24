import os
from app.knowledge.pdf_parser import extract_pdf_text


tests_dir = os.path.dirname(__file__)
pdf_path = os.path.normpath(os.path.join(tests_dir, "..", "knowledge", "dictionary", "dictionary.pdf"))

# extract all tables (full content)
text = extract_pdf_text(pdf_path)

# ensure metadata dir exists and write full raw output
metadata_dir = os.path.normpath(os.path.join(tests_dir, "..", "knowledge", "metadata"))
os.makedirs(metadata_dir, exist_ok=True)
out_path = os.path.join(metadata_dir, "raw_dictionary.txt")
with open(out_path, "w", encoding="utf-8") as f:
	f.write(text)

print(f"Wrote raw tables to: {out_path}")