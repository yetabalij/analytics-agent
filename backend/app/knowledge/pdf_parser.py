import pdfplumber

def extract_pdf_text(pdf_path):

    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)   
            
    return "\n".join(all_text)