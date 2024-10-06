from typing import List
from pikepdf import Pdf

class MergePDF:

    def __init__(self):
        self.new_pdf = Pdf.new()
        self.filename = "antigem_merged.pdf"
    
    def _save(self):
        self.new_pdf.save(self.filename)

    def merge(self, pdfs: List[Pdf], save=True):
        if not pdfs:
            raise ValueError("List of pdf cannot be none")
        if len(pdfs)<2:
            raise ValueError("Atleast two pdfs are requiured to merge")
        for pdf in pdfs:
            pdf_file = Pdf.open(pdf)
            self.new_pdf.pages.extend(pdf_file.pages)
            pdf_file.close()
        if save:
            self._save()
