from pdfminer.high_level import extract_text

def parse_pdf(path):
    text = extract_text(path)
    return text