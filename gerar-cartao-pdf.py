#!/usr/bin/env python3
"""CR80 (85,5 × 54 mm): folha A4 com frente+verso e PDF no tamanho exato do cartão.

    pip install reportlab segno
    python3 gerar-qr.py && python3 gerar-cartao-pdf.py
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
CARD_W = 85.5 * mm
CARD_H = 54 * mm

BG = HexColor("#0e0708")
ACCENT = HexColor("#a5121c")
TEXT = HexColor("#f6ecec")
MUTED = HexColor("#a8898b")
BODY = HexColor("#d4c2c2")
DIM = HexColor("#7a5f61")
BORDER = HexColor("#3a151a")
MARK = HexColor("#666666")

pdfmetrics.registerFont(TTFont("LibSans", "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSansBold", "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibMono", "/usr/share/fonts/liberation/LiberationMono-Regular.ttf"))


def crop_marks(c, x, y, w, h, length=4 * mm, gap=1.2 * mm):
    c.saveState()
    c.setStrokeColor(MARK)
    c.setLineWidth(0.25)
    pairs = [
        (x, y + h, 0, 1, -1, 0),
        (x + w, y + h, 0, 1, 1, 0),
        (x, y, 0, -1, -1, 0),
        (x + w, y, 0, -1, 1, 0),
    ]
    for cx, cy, vdx, vdy, hdx, hdy in pairs:
        c.line(cx, cy + vdy * gap, cx, cy + vdy * (gap + length))
        c.line(cx + hdx * gap, cy, cx + hdx * (gap + length), cy)
    c.restoreState()


def draw_card(c, x, y, qr):
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, CARD_W, CARD_H)
    c.clipPath(p, stroke=0, fill=0)

    c.setFillColor(BG)
    c.rect(x, y, CARD_W, CARD_H, stroke=0, fill=1)
    c.setFillColor(ACCENT)
    c.rect(x, y + CARD_H - 0.7 * mm, CARD_W, 0.7 * mm, stroke=0, fill=1)

    pad = 3.2 * mm
    qr_box = 32 * mm
    qr_x = x + CARD_W - pad - qr_box
    qr_y = y + (CARD_H - qr_box) / 2
    c.setFillColor(white)
    c.rect(qr_x, qr_y, qr_box, qr_box, stroke=0, fill=1)
    inset = 1.6 * mm
    c.drawImage(
        qr,
        qr_x + inset,
        qr_y + inset,
        qr_box - 2 * inset,
        qr_box - 2 * inset,
        preserveAspectRatio=True,
        mask="auto",
    )

    tx = x + pad
    top = y + CARD_H - 6.2 * mm
    c.setFillColor(ACCENT)
    c.setFont("LibMono", 6.5)
    c.drawString(tx, top, "~/helenistica")

    c.setFillColor(TEXT)
    c.setFont("LibSansBold", 9.5)
    c.drawString(tx, top - 5.2 * mm, "Helena Bridi Lona")

    c.setFillColor(MUTED)
    c.setFont("LibMono", 5)
    c.drawString(tx, top - 9.4 * mm, "Escrita · Pesquisa · Dança")

    c.setFillColor(BODY)
    c.setFont("LibSans", 6.5)
    c.drawString(tx, y + 8.4 * mm, "Aponte a câmera aqui")

    c.setFillColor(DIM)
    c.setFont("LibMono", 4.4)
    c.drawString(tx, y + 5.4 * mm, "andredev21.github.io")
    c.drawString(tx, y + 3.4 * mm, "/cartao-helena/")

    c.restoreState()
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.2)
    c.rect(x, y, CARD_W, CARD_H, stroke=1, fill=0)


def draw_exact_page(c, qr):
    c.setFillColor(BG)
    c.rect(0, 0, CARD_W, CARD_H, stroke=0, fill=1)
    draw_card(c, 0, 0, qr)
    c.showPage()


def main():
    qr_path = ROOT / "qr-print.png"
    if not qr_path.exists():
        raise SystemExit("Roda primeiro: python3 gerar-qr.py")

    qr = ImageReader(str(qr_path))
    out_a4 = ROOT / "cartao-qr-a4.pdf"
    out_card = ROOT / "cartao-qr.pdf"

    c = canvas.Canvas(str(out_a4), pagesize=A4)
    c.setTitle("Helena Bridi Lona — adesivo/cartão 85,5 × 54 mm")
    c.setAuthor("Helena Bridi Lona")
    page_w, page_h = A4

    c.setFillColor(white)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    c.setFillColor(HexColor("#222222"))
    c.setFont("LibSans", 9)
    c.drawCentredString(page_w / 2, page_h - 14 * mm, "Imprimir em tamanho real (100%). Recortar nas marcas.")
    c.setFont("LibSans", 8)
    c.setFillColor(HexColor("#555555"))
    c.drawCentredString(
        page_w / 2,
        page_h - 18.5 * mm,
        "Duas faces 85,5 × 54 mm — colar frente e verso no cartão NFC ou imprimir o PDF do cartão.",
    )

    gap = 18 * mm
    total_h = CARD_H * 2 + gap
    x = (page_w - CARD_W) / 2
    y_top = (page_h - total_h) / 2 + CARD_H + gap
    y_bot = (page_h - total_h) / 2

    c.setFillColor(ACCENT)
    c.setFont("LibMono", 8)
    c.drawString(x, y_top + CARD_H + 3 * mm, "FRENTE")
    c.drawString(x, y_bot + CARD_H + 3 * mm, "VERSO")

    draw_card(c, x, y_top, qr)
    crop_marks(c, x, y_top, CARD_W, CARD_H)
    draw_card(c, x, y_bot, qr)
    crop_marks(c, x, y_bot, CARD_W, CARD_H)
    c.save()

    d = canvas.Canvas(str(out_card), pagesize=(CARD_W, CARD_H))
    d.setTitle("Helena Bridi Lona — cartão QR frente e verso")
    d.setAuthor("Helena Bridi Lona")
    draw_exact_page(d, qr)
    draw_exact_page(d, qr)
    d.save()

    print(out_a4)
    print(out_card)


if __name__ == "__main__":
    main()
