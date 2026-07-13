from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "Joshua-T-Hester-EPK.pdf"
PHOTO = ROOT / "images" / "jh-1.jpg"

PAGE_W, PAGE_H = letter
INK = HexColor("#070608")
PANEL = HexColor("#100D13")
PLUM = HexColor("#241532")
VIOLET = HexColor("#8B5CF6")
VIOLET_LIGHT = HexColor("#A78BFA")
PARCHMENT = HexColor("#EEE9E1")
MUTED = HexColor("#A7A0AA")
SUBTLE = HexColor("#6D6870")
LINE = HexColor("#2A252D")

EMAIL = "mailto:joshuahestermusic@gmail.com"
WEBSITE = "https://www.joshuahestermusic.com"


def register_fonts():
    pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))
    pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


def draw_crop(c, image_path, x, y, width, height, focus_x=0.5, focus_y=0.5):
    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        iw, ih = image.size
        image_data = BytesIO()
        image.save(image_data, format="JPEG", quality=89, optimize=True)
        image_data.seek(0)
    scale = max(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    dx = x - (dw - width) * focus_x
    dy = y - (dh - height) * focus_y
    c.saveState()
    path = c.beginPath()
    path.rect(x, y, width, height)
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(ImageReader(image_data), dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.restoreState()


def draw_label(c, text, x, y, color=VIOLET):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 6.4)
    c.drawString(x, y, text.upper())


def draw_paragraph(c, text, x, y_top, width, font="Arial", size=8.5, leading=12, color=MUTED):
    style = ParagraphStyle(
        name="epk",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
        splitLongWords=False,
    )
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(c, x, y_top - height)
    return height


def draw_link(c, label, url, x, y, font="Arial-Bold", size=8, color=PARCHMENT, arrow=True):
    text = f"{label}  ->" if arrow else label
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)
    width = pdfmetrics.stringWidth(text, font, size)
    c.linkURL(url, (x, y - 2, x + width, y + size + 2), relative=0, thickness=0)
    return width


def build_pdf():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    c.setTitle("Joshua T. Hester - Electronic Press Kit")
    c.setAuthor("Joshua T. Hester")
    c.setSubject("Americana and folk singer-songwriter electronic press kit")
    c.setKeywords("Joshua T. Hester, EPK, Americana, folk, Wisconsin, singer-songwriter")

    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Hero image and overlay.
    image_x = 338
    image_y = 405
    draw_crop(c, PHOTO, image_x, image_y, PAGE_W - image_x, PAGE_H - image_y, focus_x=0.54, focus_y=0.40)
    c.saveState()
    c.setFillColor(INK)
    c.setFillAlpha(0.12)
    c.rect(image_x, image_y, PAGE_W - image_x, PAGE_H - image_y, stroke=0, fill=1)
    for step in range(18):
        c.setFillAlpha(0.32 * (1 - step / 18))
        c.rect(image_x + step * 5, image_y, 6, PAGE_H - image_y, stroke=0, fill=1)
    c.restoreState()

    # Top identity.
    draw_label(c, "Electronic Press Kit / 2026", 34, 750)
    c.setFillColor(PARCHMENT)
    c.setFont("Georgia", 43)
    c.drawString(31, 691, "Joshua T.")
    c.setFillColor(VIOLET_LIGHT)
    c.setFont("Georgia-Italic", 49)
    c.drawString(31, 638, "Hester")

    c.setStrokeColor(VIOLET)
    c.setLineWidth(2)
    c.line(34, 604, 85, 604)
    c.setFillColor(PARCHMENT)
    c.setFont("Arial-Bold", 9)
    c.drawString(99, 600, "AMERICANA  /  FOLK  /  ROOTS")

    summary = (
        "Wisconsin-made songs rooted in storytelling, lived experience, "
        "and the traditions of American roots music."
    )
    draw_paragraph(c, summary, 34, 570, 254, font="Georgia", size=13.5, leading=18, color=PARCHMENT)

    c.setFillColor(PLUM)
    c.roundRect(34, 439, 251, 67, 10, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#44255D"))
    c.roundRect(34, 439, 251, 67, 10, stroke=1, fill=0)
    draw_label(c, "Booking and inquiries", 50, 487, VIOLET_LIGHT)
    draw_link(c, "joshuahestermusic@gmail.com", EMAIL, 50, 461, size=9, arrow=False)

    # Main lower content field.
    c.setFillColor(PANEL)
    c.rect(0, 55, PAGE_W, 350, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.line(0, 405, PAGE_W, 405)

    # Bio column.
    left_x = 34
    left_w = 322
    draw_label(c, "Artist Bio", left_x, 374)
    c.setFillColor(PARCHMENT)
    c.setFont("Georgia", 22)
    c.drawString(left_x, 341, "Honest songs. Road-tested craft.")

    bio_lede = (
        "Joshua T. Hester is a Wisconsin-based Americana and folk singer-songwriter "
        "whose music is rooted in storytelling, lived experience, and American roots music."
    )
    used = draw_paragraph(c, bio_lede, left_x, 319, left_w, font="Georgia", size=10.5, leading=14, color=PARCHMENT)

    bio_body = (
        "For more than a decade, Hester toured the Midwest as a member of Listening Party, "
        "playing hundreds of shows in listening rooms, clubs, theaters, fairs, and festivals. "
        "A multi-instrumentalist on guitar, bass, and mandolin, he now performs under his own "
        "name, blending folk, country, Americana, and roots influences into character-driven "
        "songs with a distinctly Midwestern perspective."
    )
    draw_paragraph(c, bio_body, left_x, 309 - used, left_w, size=7.9, leading=11, color=MUTED)

    draw_label(c, "Selected Experience", left_x, 194)
    highlights = [
        ("SUMMERFEST", "Festival"),
        ("MILE OF MUSIC", "Festival"),
        ("WI STATE FAIR", "Fair"),
    ]
    box_w = 100
    for index, (name, category) in enumerate(highlights):
        x = left_x + index * 109
        c.setFillColor(INK)
        c.roundRect(x, 118, box_w, 59, 7, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(x, 118, box_w, 59, 7, stroke=1, fill=0)
        c.setFillColor(SUBTLE)
        c.setFont("Arial-Bold", 5.6)
        c.drawString(x + 10, 157, category.upper())
        c.setFillColor(PARCHMENT)
        c.setFont("Georgia", 10.3)
        c.drawString(x + 10, 134, name)

    c.setFillColor(MUTED)
    c.setFont("Arial", 7.3)
    c.drawString(left_x, 91, "10+ years touring  /  Hundreds of live performances  /  Wisconsin, USA")

    # Media and contact column.
    right_x = 386
    right_w = 192
    c.setStrokeColor(LINE)
    c.line(372, 83, 372, 376)
    draw_label(c, "Selected Media", right_x, 374)
    media = [
        ("The End is Nigh", "https://youtu.be/cxJRvBB9Irc"),
        ("Andy's Song", "https://youtu.be/OSkZ3FQ7hcI"),
        ("Sick Day", "https://youtu.be/sC0MnJHd2hw"),
    ]
    y = 343
    for index, (name, url) in enumerate(media, start=1):
        c.setFillColor(SUBTLE)
        c.setFont("Arial-Bold", 6)
        c.drawString(right_x, y + 8, f"0{index}  /  VIDEO")
        draw_link(c, name, url, right_x, y - 8, font="Georgia", size=11.5, color=PARCHMENT)
        c.setStrokeColor(LINE)
        c.line(right_x, y - 20, right_x + right_w, y - 20)
        y -= 54

    draw_label(c, "Follow", right_x, 180)
    social_links = [
        ("YouTube", "https://www.youtube.com/@joshuahestermusic"),
        ("Instagram", "https://www.instagram.com/joshuahestermusic/"),
        ("Facebook", "https://www.facebook.com/joshuathester/"),
        ("TikTok", "https://www.tiktok.com/@joshuahestermusic"),
    ]
    positions = [(right_x, 154), (right_x + 95, 154), (right_x, 128), (right_x + 95, 128)]
    for (label, url), (x, y) in zip(social_links, positions):
        draw_link(c, label, url, x, y, size=7.5, color=MUTED)

    draw_label(c, "Official Website", right_x, 95)
    draw_link(c, "joshuahestermusic.com", WEBSITE, right_x, 74, size=8.5, color=VIOLET_LIGHT, arrow=False)

    # Footer.
    c.setFillColor(PLUM)
    c.rect(0, 0, PAGE_W, 55, stroke=0, fill=1)
    c.setFillColor(PARCHMENT)
    c.setFont("Georgia-Italic", 12)
    c.drawString(34, 22, "Tell the truth. Serve the song.")
    draw_link(c, "BOOK JOSHUA", EMAIL + "?subject=Booking%20Inquiry%20for%20Joshua%20T.%20Hester", 466, 23, size=7.3, color=PARCHMENT)

    c.showPage()
    c.save()

    reader = PdfReader(str(OUTPUT))
    assert len(reader.pages) == 1, "EPK must remain a single page"
    annotations = reader.pages[0].get("/Annots", [])
    assert len(annotations) >= 10, "Expected clickable email, website, social, and media links"
    print(f"Created {OUTPUT}")
    print(f"Pages: {len(reader.pages)}; clickable link annotations: {len(annotations)}")


if __name__ == "__main__":
    build_pdf()
