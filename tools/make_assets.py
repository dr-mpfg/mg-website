#!/usr/bin/env python3
"""One-off asset generation with Pillow: favicon.ico, apple-touch-icon.png, img/og-share.png.
    python3 tools/make_assets.py
Re-run after changing the palette or the positioning line."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER, INK, ACCENT = (246, 242, 234), (27, 29, 34), (31, 111, 181)
SERIF_BOLD = os.path.join(ROOT, 'fonts', 'SourceSerif4-Semibold.woff2')
SANS = os.path.join(ROOT, 'fonts', 'IBMPlexSans-Medium.woff2')

def font(path, size):
    for p in (path, path.replace('.woff2', '.ttf')):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size)

def t_mark(draw, x, y, size, width, colour=INK):
    draw.line([(x, y), (x + size, y)], fill=colour, width=width)
    draw.line([(x + size / 2, y), (x + size / 2, y + size * 0.95)], fill=colour, width=width)

def icon(px):
    im = Image.new('RGB', (px, px), PAPER)
    d = ImageDraw.Draw(im)
    t_mark(d, px * 0.16, px * 0.25, px * 0.68, max(2, round(px * 0.085)))
    return im

def main():
    icon(32).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32)])
    icon(180).save(os.path.join(ROOT, 'apple-touch-icon.png'))
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    t_mark(d, 80, 80, 56, 5)
    d.text((80, 170), 'Dr Matteo Giordano', font=font(SANS, 28), fill=(107, 111, 118))
    f = font(SERIF_BOLD, 60)
    y = 225
    for line in ('Macro-financial strategist.', 'Shipping, monetary structures,', 'and off-balance-sheet finance.'):
        d.text((80, y), line, font=f, fill=INK); y += 74
    d.line([(80, 500), (1120, 500)], fill=ACCENT, width=2)
    d.text((80, 525), 'mg-macro.vercel.app', font=font(SANS, 26), fill=(107, 111, 118))
    im.save(os.path.join(ROOT, 'img', 'og-share.png'), optimize=True)
    print('wrote favicon.ico, apple-touch-icon.png, img/og-share.png')

if __name__ == '__main__':
    main()
