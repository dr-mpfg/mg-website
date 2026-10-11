#!/usr/bin/env python3
"""One-off asset generation with Pillow: favicon.ico, apple-touch-icon.png, img/og-share.png.
    python3 tools/make_assets.py
Re-run after changing the palette or the positioning line."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER, INK, ACCENT, MUTED = (246, 242, 234), (27, 29, 34), (31, 111, 181), (107, 111, 118)
SANS_SEMI = os.path.join(ROOT, 'fonts', 'IBMPlexSans-SemiBold.woff2')
SANS = os.path.join(ROOT, 'fonts', 'IBMPlexSans-Medium.woff2')
SERIF = os.path.join(ROOT, 'fonts', 'SourceSerif4-Regular.woff2')

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError as e:
        raise SystemExit('cannot load %s: %s' % (path, e))

def monogram(px):
    """Ink square with MG in paper."""
    im = Image.new('RGB', (px, px), INK)
    d = ImageDraw.Draw(im)
    f = font(SANS_SEMI, round(px * 0.46))
    d.text((px / 2, px / 2), 'MG', font=f, fill=PAPER, anchor='mm')
    return im

def main():
    monogram(64).resize((32, 32), Image.LANCZOS).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32)])
    monogram(180).save(os.path.join(ROOT, 'apple-touch-icon.png'))
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (W, 8)], fill=INK)
    d.text((80, 84), 'DR MATTEO GIORDANO', font=font(SANS, 24), fill=MUTED)
    f = font(SANS_SEMI, 62); y = 140
    for line in ('Macro-financial strategist.', 'Shipping, monetary structures,', 'and off-balance-sheet finance.'):
        d.text((80, y), line, font=f, fill=INK); y += 74
    d.line([(80, 392), (1120, 392)], fill=INK, width=1)
    fs = font(SERIF, 27); y = 414
    for line in ('Sovereign risk · Eurozone monetary systems · Industrial strategy', 'Geopolitical and defence economics · Trade, freight and credit'):
        d.text((80, y), line, font=fs, fill=INK); y += 40
    d.text((80, 545), 'mg-macro.vercel.app', font=font(SANS, 24), fill=MUTED)
    im.save(os.path.join(ROOT, 'img', 'og-share.png'), optimize=True)
    print('wrote favicon.ico, apple-touch-icon.png, img/og-share.png')

if __name__ == '__main__':
    main()
