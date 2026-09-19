# Cartão de contato — Helena Bridi Lona

Cartão digital fullscreen: tinta escura + vermelho `#a5121c` / `#850006`, tipografia literária (Cormorant), PT/EN.

URL: **https://andredev21.github.io/cartao-helena/**

```
index.html           o cartão digital
helena.vcf           contato pra agenda
favicon.svg
img/avatar.jpg
qr-print.png         QR preto/branco (impressão)
qr.png               QR nas cores do cartão
qr.svg               vetor pra gráfica
cartao-qr.pdf        PDF no tamanho CR80 (85,5 × 54 mm) — frente e verso
cartao-qr-a4.pdf     mesma arte em A4 com marcas de corte
gerar-qr.py
gerar-cartao-pdf.py
```

## IDV

- Fundo quase preto com undertone vermelho (`#0e0708`)
- Accent `#a5121c` e deep `#850006`
- Nome em serifa; chips e CTAs no mesmo vermelho

## Cartão físico / QR

1. `python3 -m venv .venv && .venv/bin/pip install segno reportlab`
2. `.venv/bin/python gerar-qr.py`
3. `.venv/bin/python gerar-cartao-pdf.py`
4. Imprime `cartao-qr.pdf` em tamanho real (100%) ou recorta a folha `cartao-qr-a4.pdf`.

Destino do QR: `https://andredev21.github.io/cartao-helena/`

## Publicar

```bash
git push origin main && git push origin main:gh-pages
```
