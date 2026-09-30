from io import BytesIO
import textwrap

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def to_docx(text: str) -> bytes:
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line if line.strip() else "")

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def to_pdf(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y_position = height - 50
    margin_left = 50

    for paragraph in text.splitlines():
        wrapped_lines = textwrap.wrap(paragraph, width=90) or [""]
        for line in wrapped_lines:
            if y_position < 50:
                pdf.showPage()
                y_position = height - 50
            pdf.drawString(margin_left, y_position, line)
            y_position -= 15

        y_position -= 10

    pdf.save()
    return buffer.getvalue()
