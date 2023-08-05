from w6libs.PyPDF2 import PdfFileReader


def pdf2txt(path):
    # creating a pdf reader object
    pdf_reader = PdfFileReader(path, 'rb')

    # extract pdf version
    pdf_version = ''
    # pdf_reader.stream.seek(0)
    # pdf_version = pdf_reader.stream.readline().decode().strip()

    # extracting text from page
    pdf_text = ""
    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        pdf_text += page_obj.extract_text()
    return pdf_version, pdf_text
