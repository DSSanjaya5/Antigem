import pikepdf
from pikepdf import Pdf
from typing import List

class RotatePDF:

    def __init__(self, path):
        self.new_pdf = Pdf.new()
        self.filename = "antigem_rotated.pdf"
        self.file_path = path

    def rotate(self, pages: List=None, pdf=False, degree=90):
        if pdf:
            with pikepdf.open(self.file_path) as pdf:
                for i in range(len(pdf.pages)):
                    pdf.pages[i].Rotate = degree
                pdf.save(self.filename)
        else:
            pages = list(set(pages))
            pdf = pikepdf.open(self.file_path)
            pdf_len = len(pdf.pages)
            for i in pages:
                i = min(pdf_len, max(0, i))
                pdf.pages[i-1].Rotate = degree
            pdf.save(self.filename)
            pdf.close()
