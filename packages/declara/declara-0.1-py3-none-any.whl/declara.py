"""Declara, a library for generating Boreas declaration forms"""

__version__ = "0.1"

from collections import namedtuple
from io import BytesIO
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter, PdfFileReader
from datetime import date

class Declara:
    Row = namedtuple("Row", ["description", "amount"])

    def __init__(self):
        self.reader = PdfReader("Declaratieformulier_v3F.pdf")
        self.writer = PdfWriter()

        page = self.reader.pages[0]
        self.writer.add_page(page)

        self.rows = []
        self.attachments = []

        self.name = ""
        self.iban = ""

    def get_description(self, idx):
        try:
            return self.rows[idx].description
        except IndexError:
            return ""

    def get_amount(self, idx):
        try:
            return f"{self.rows[idx].amount:.2f}".replace(".", ",")
        except IndexError:
            return ""

    def produce(self, output_file=None, custom_date=None):
        if not custom_date:
            d = date.today().isoformat()
        else:
            d = custom_date.isoformat()
        
        ds = d.split("-")

        if not output_file:
            output_file = f"Declaratie {ds[2]}-{ds[1]}-{ds[0]}.pdf"

        year = ds[0]
        month = ds[1]
        day = ds[2]

        total = 0
        for row in self.rows:
            total += float(row.amount)

        data = {
            "Date-dd": day,
            "date-mm": month,
            "date-jjjj": year,
            "name": self.name,
            "iban": self.iban,
            "omschr1": self.get_description(0),
            "Text1": self.get_description(1),
            "Text2": self.get_description(2),
            "Text3": self.get_description(3),
            "Text4": self.get_description(4),
            "Text5": self.get_description(5),
            "Text6": self.get_description(6),
            "Text7": self.get_description(7),
            "bedrag1": self.get_amount(0),
            "Text15": self.get_amount(1),
            "Text16": self.get_amount(2),
            "Text17": self.get_amount(3),
            "Text18": self.get_amount(4),
            "Text19": self.get_amount(5),
            "Text20": self.get_amount(6),
            "Text21": self.get_amount(7),
            "Text22": f"{total:.2f}".replace(".", ","),
        }

        self.writer.update_page_form_field_values(
            self.writer.pages[0], data
        )

        for attachment in self.attachments:
            page = self.writer.add_blank_page(self.writer.pages[0].mediaBox.width, self.writer.pages[0].mediaBox.height)
            buf = BytesIO()
            can = canvas.Canvas(buf)

            can.drawImage(attachment, 100, 75, width=400, preserveAspectRatio=True, anchor='sw')
            can.save()
            buf.seek(0)

            new_pdf = PdfFileReader(buf)

            page.mergePage(new_pdf.getPage(0))
        

        with open(output_file, "wb") as output_stream:
            self.writer.write(output_stream)
