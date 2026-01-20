import os
import ctypes
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap

def get_downloads_folder():
    # Try Windows native API
    try:
        from ctypes import wintypes, windll

        CSIDL_DOWNLOADS = 0x000c
        SHGFP_TYPE_CURRENT = 0

        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        windll.shell32.SHGetFolderPathW(
            None, CSIDL_DOWNLOADS, None, SHGFP_TYPE_CURRENT, buf
        )

        path = buf.value.strip()
        if path and os.path.exists(path):
            return path
    except:
        pass

    # Fallback 1: User home Downloads
    home_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.exists(home_downloads):
        return home_downloads

    # Fallback 2: Create Downloads in home
    os.makedirs(home_downloads, exist_ok=True)
    return home_downloads

def get_unique_filename(folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base}({counter}){ext}"
        counter += 1

    return new_filename

def export_chat_to_pdf(chat_history, filename="youtube_notes.pdf"):
    downloads_path = get_downloads_folder()

    # Absolute safety check
    if not downloads_path:
        raise RuntimeError("Could not determine Downloads folder path.")

    unique_filename = get_unique_filename(downloads_path, filename)
    file_path = os.path.join(downloads_path, unique_filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    x_margin = 1 * inch
    y_margin = height - 1 * inch

    text = c.beginText(x_margin, y_margin)
    text.setFont("Helvetica", 11)

    for msg in chat_history:
        role = "Q: " if msg["role"] == "user" else "A: "
        wrapped_lines = textwrap.wrap(role + msg["content"], 90)

        for line in wrapped_lines:
            if text.getY() < 1 * inch:
                c.showPage()
                text = c.beginText(x_margin, height - 1 * inch)
                text.setFont("Helvetica", 11)
            text.textLine(line)

        text.textLine("")

    c.drawText(text)
    c.save()

    return file_path

