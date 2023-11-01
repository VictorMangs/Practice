import fitz  # PyMuPDF
import tabula
import pathlib

def extract_tables_from_pdf(pdf_file):
    # Step 1: Use PyMuPDF to extract text from the PDF
    pdf_document = fitz.open(pdf_file)
    pdf_text = ''
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()

    # Step 2: Use tabula-py to extract tables from the extracted text
    tables = tabula.read_pdf(pdf_file, pages="all")

    # If you want to save the extracted tables as CSV, you can do the following:
    for i, table in enumerate(tables):
        table.to_csv(f'table_{i}.csv', index=False)

    return tables

if __name__ == "__main__":
    pdf_file = pathlib.Path(pathlib.Path(__file__).parent / 'table.pdf')
    print(pathlib.Path(pathlib.Path(__file__).parent / 'table.pdf').exists())
    extracted_tables = extract_tables_from_pdf(pdf_file)
    for i, table in enumerate(extracted_tables):
        print(f"Table {i + 1}:\n{table}")
