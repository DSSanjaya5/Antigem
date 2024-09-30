import os
import zipfile
from pikepdf import Pdf
from typing import List

class SplitPDF():

    def __init__(self, path, range: List = None, extract: List = None, merge=False):
        self.pdf = Pdf.open(path)
        self.filename = self.pdf.filename.removesuffix('.pdf')
        self.extract = extract
        self.range = range
        self.merge = merge

    def split_pdf(self):
        if self.merge:
            self.output_file = f'antigem_{self.filename}_split.pdf'
            self.output = Pdf.new()
        else:
            self.zip_file = f"antigem_{self.filename}_split.zip"
        if self.extract:
            self.extract_pdf()
        if range:
            self.range()
        
    def add_file_to_zip(self, zip_file_path, file_to_add):
        with zipfile.ZipFile(zip_file_path, 'a') as zip_ref:
            zip_ref.write(file_to_add)
        
    def extract_pdf(self):
        if self.merge:
            for index in self.extract:
                self.output.pages.append(self.pdf.pages[index-1])
            self.output.save(self.output_file)
        else:
            for index in self.extract:
                new_pdf = Pdf.new()
                new_pdf.pages.append(self.pdf.pages[index-1])
                file = f'antigem_{self.filename}_{index:02d}.pdf'
                new_pdf.save(file)
                self.add_file_to_zip(self.zip_file, file)
                if os.path.isfile(file):
                    os.remove(file)
            
    def range_pdf(self):
        if self.merge:
            for r in self.range:
                self.output.pages.append(self.pdf.pages[r[0]-1:r[1]])
            self.output.save(self.output_file)
        else:
            for r in self.range:
                new_pdf = Pdf.new()
                new_pdf.pages.append(self.pdf.pages[r[0]-1:r[1]])
                file = f'antigem_{self.filename}_{r[0]}_{r[1]}.pdf'
                new_pdf.save(file)
                self.add_file_to_zip(self.zip_file, file)
                if os.path.isfile(file):
                    os.remove(file)

if __name__ == '__main__':
    sp = SplitPDF("../../test_pdf.pdf", range=[], extract=[])
    sp.split_pdf()