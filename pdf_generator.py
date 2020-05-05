from fpdf import FPDF
import pdfkit
import glob
import os
from fnmatch import fnmatch
import html

# path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# pdfkit.from_file('prueba.html', 'out.pdf', configuration=config)

class File:

    def __init__(self, path, file_type, filename):
        self.path = path
        self.file_type = file_type
        self.filename = filename

class PDFCode:
    def __init__(self, dirname):
        self.dirname = dirname
        
        self.files = self.read_files_dir(self.dirname)
    

    def read_files_dir(self, dirname, file_types=[".java"]):
        files_found = []
        # pattern = [".java"]

        for path, subdirs, files in os.walk(dirname):
            for name in files:
                if name.lower().endswith(tuple(file_types)):
                    filename, file_extension = os.path.splitext(name)

                    file = File(path + os.path.sep + name, file_extension.replace('.',''), filename)
                    files_found.append(file)

        return files_found

    def set_dir(self, dirname):
        """
        Para funcionar sin necesidad que mover los archivos, se podrá
        dar la ruta absoluta del proyecto para que pueda ser agregado
        """
        self.dirname = dirname

    def convert_html_to_pdf(self, file):
        """
        Debido a que cada archivo java genera un html, este deberá ser 
        convertido en un pdf.
        El proceso se deberá repetir por cada archivo
        """

        options = {
            'quiet': ''
        }

        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdfkit.from_file(file.path, 'pdfs/' + file.filename +'.pdf', configuration=config, options=options)

    def create_html_of_file(self, file, style="atom-one-light", template='default.html'):
        """
        Cada archivo java necesita ser pasado a un html para luego ser procesado
        y convertido a pdf
        """
        template = self.get_template(template)

        f = open(file.path, 'r+')
        str_file = """"""
        for line in f.readlines():
            if not line.isspace():
                str_file += line
        f.close()
        
        encoded_file = html.escape(str_file)

        template = template.replace('{code}', encoded_file)
        template = template.replace('{filename}', file.filename)
        template = template.replace('{file_type}', '"lang-' + file.file_type + '"')

        html_file = open(f"html_files/{file.filename}.html", 'w')
        html_file.write(template)
        html_file.close()

    def convert_all_files_to_html(self):
        for file in self.files:
            print(f"Leyendo {file.filename}.{file.file_type}...")
            self.create_html_of_file(file)

    def convert_all_html_to_pdf(self):
        pdf_files = self.read_files_dir('html_files', ['.html'])
        for file in pdf_files:
            print(f"Convirtiendo {file.filename}.{file.file_type} a un archivo PDF")
            self.convert_html_to_pdf(file)

    def merge_files(self):
        from PyPDF2 import PdfFileMerger

        pdfs = self.read_files_dir(file_types=['.pdf'], dirname='pdfs')

        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append(pdf.path)

        merger.write("result.pdf")
        merger.close()

    def get_template(self, name):

        f = open(name, 'r+')
        str_file = """"""

        for line in f.readlines():
            if not line.isspace():
                str_file += line
        f.close()

        return str_file

    def generate_project_pdf(self):
        self.convert_all_files_to_html()
        self.convert_all_html_to_pdf()
        self.merge_files()

if __name__ == "__main__":
    pdf = PDFCode(r"D:\OneDrive - Universidad Autonoma de Yucatan\LIS\4to Semestre\Estructura de datos\Unidad 5\Tarea 3\Codigo\src")
    # pdf.merge_files()
    # pdf.read_files_dir()
    # print(pdf.files)
    # pdf.create_html_of_file(pdf.files[0])
    # pdf.conver_html_to_pdf(pdf.files[0])
    pdf.generate_project_pdf()