import os
import zipfile
from pikepdf import Pdf
from typing import List


class SplitPDF:

    def __init__(self, path):
        self.pdf = Pdf.open(path)
        self.filename = os.path.basename(path).removesuffix(".pdf")
        self.pdf_len = len(self.pdf.pages)
        print(self.pdf_len)

    def add_file_to_zip(self, zip_file_path, file_to_add):
        with zipfile.ZipFile(zip_file_path, "a") as zip_ref:
            zip_ref.write(file_to_add)

    def prepare_output(self, merge):
        if merge:
            self.output_filename = f"antigem_{self.filename}_split.pdf"
            self.output_pdf = Pdf.new()
        else:
            self.zip_file = f"antigem_{self.filename}_split.zip"

    def split_range(self, range_of_pages: List = None, merge=False):
        if not range_of_pages:
            raise ValueError("Range cannot be empty.")
        if len(range_of_pages) == 1:
            merge = True
        self.prepare_output(merge)
        if merge:
            for r in range_of_pages:
                r = sorted(r)
                r[0] = max(1, r[0])
                r[1] = min(r[1], self.pdf_len)
                self.output_pdf.pages.extend(self.pdf.pages[r[0] - 1 : r[1]])
            self.output_pdf.save(self.output_filename)
        else:
            for r in range_of_pages:
                r = sorted(r)
                r[0] = max(1, r[0])
                r[1] = min(r[1], self.pdf_len)
                new_pdf = Pdf.new()
                new_pdf.pages.extend(self.pdf.pages[r[0] - 1 : r[1]])
                file = f"antigem_{self.filename}_{r[0]}_{r[1]}.pdf"
                new_pdf.save(file)
                self.add_file_to_zip(self.zip_file, file)
                if os.path.isfile(file):
                    os.remove(file)

    def split_extract(self, extract_pages: List = None, merge=False):
        if not extract_pages:
            raise ValueError("Range cannot be empty.")
        if len(extract_pages) == 1:
            merge = True
        self.prepare_output(merge)
        if merge:
            for index in extract_pages:
                index = min(self.pdf_len, max(0, index))
                self.output_pdf.pages.append(self.pdf.pages[index - 1])
            self.output_pdf.save(self.output_filename)
        else:
            for index in extract_pages:
                index = min(self.pdf_len, max(0, index))
                new_pdf = Pdf.new()
                new_pdf.pages.append(self.pdf.pages[index - 1])
                file = f"antigem_{self.filename}_{index:02d}.pdf"
                new_pdf.save(file)
                self.add_file_to_zip(self.zip_file, file)
                if os.path.isfile(file):
                    os.remove(file)


# def sample_pdf():
#     """Create a simple PDF with 5 pages for testing."""
#     pdf_path = os.path.join("test_pdf.pdf")
#     pdf = Pdf.new()
#     for i in range(5):
#         pdf.add_blank_page()
#     pdf.save(str(pdf_path))
#     return str(pdf_path)

# if __name__ == '__main__':
#     sp = SplitPDF(path=sample_pdf(), range=[[1,3]])
#     sp.split_pdf()
