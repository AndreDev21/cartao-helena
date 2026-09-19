#!/usr/bin/env python3
"""Gera os QR codes do cartão da Helena.

    pip install segno
    python3 gerar-qr.py

Sai: qr.svg, qr-print.png, qr.png
"""

import segno

URL = "https://andredev21.github.io/cartao-helena/"
ACCENT = "#a5121c"
ESCURO = "#0e0708"


def main():
    qr = segno.make(URL, error="h")
    qr.save("qr.svg", scale=10, border=4, dark=ESCURO, light="#ffffff")
    qr.save("qr-print.png", scale=20, border=4, dark="#000000", light="#ffffff")
    qr.save("qr.png", scale=16, border=4, dark=ACCENT, light=ESCURO)
    print(f"QR gerado para: {URL}")
    print("  qr.svg        vetor / gráfica")
    print("  qr-print.png  impressão / cartão (preto no branco)")
    print("  qr.png        tela, cores do cartão")


if __name__ == "__main__":
    main()
