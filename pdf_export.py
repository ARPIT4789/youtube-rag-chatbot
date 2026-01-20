from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_pdf_bytes(messages):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 40

    c.setFont("Helvetica", 10)

    for msg in messages:
        text = f"{msg['role'].upper()}: {msg['content']}"
        for line in text.split("\n"):
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(40, y, line)
            y -= 14

        y -= 10

    c.save()
    buffer.seek(0)
    return buffer


