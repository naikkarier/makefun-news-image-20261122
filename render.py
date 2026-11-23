"""Render the 22 November 2026 world-news front page, 1024x1024 PNG.

Deterministic: no randomness, no timestamps, no network. Running this
script twice writes identical bytes (PIL writes no time chunk).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 232)
INK = (20, 24, 38)
NAVY = (16, 32, 64)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (14, 110, 110)
GREY = (90, 92, 102)
WHITE = (255, 255, 255)
SEA = (28, 68, 110)

F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, color, width, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y

def tanker(draw, x, y, s):
    # simple oil tanker silhouette on waves
    draw.rectangle([x, y, x + 220 * s, y + 34 * s], fill=(60, 60, 70))
    draw.rectangle([x + 150 * s, y - 26 * s, x + 190 * s, y], fill=(60, 60, 70))
    draw.rectangle([x + 165 * s, y - 44 * s, x + 176 * s, y - 26 * s], fill=(60, 60, 70))
    for i in range(5):
        wx = x + i * 46 * s
        draw.arc([wx, y + 34 * s, wx + 44 * s, y + 52 * s], 0, 180, fill=(120, 180, 220), width=3)
    # flame
    draw.polygon([(x + 30 * s, y - 6 * s), (x + 48 * s, y - 52 * s), (x + 66 * s, y - 6 * s)],
                 fill=(230, 120, 30))
    draw.polygon([(x + 40 * s, y - 6 * s), (x + 48 * s, y - 30 * s), (x + 56 * s, y - 6 * s)],
                 fill=(245, 200, 60))

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 18), "THE WORLD TODAY", font=font(SERIF, 58), fill=WHITE)
    d.text((32, 84), "SUNDAY 22 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=font(SANS_B, 20), fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=RED)
    # hero: Hormuz
    d.rectangle([24, 142, 660, 470], fill=NAVY)
    d.rectangle([24, 142, 660, 470], outline=GOLD, width=3)
    d.text((48, 156), "COP31", font=font(SERIF, 48), fill=WHITE)
    d.text((48, 212), "COLLAPSES", font=font(SERIF, 48), fill=WHITE)
    y = text_block(d, 48, 276, "Climate talks end with no deal in Antalya, Turkey.",
                   font(SANS_B, 24), GOLD, 590, 32)
    text_block(d, 48, y + 4,
               "The EU rejected a final text with no mention of fossil fuels.",
               font(SANS, 21), (220, 225, 235), 590, 28)
    for i in range(12):
        wx = 48 + i * 50
        d.arc([wx, 452, wx + 48, 468], 0, 180, fill=(120, 180, 220), width=3)
    d.text((48, 428), "NEARLY 200 COUNTRIES, NO AGREEMENT",
           font=font(SANS_B, 20), fill=(245, 200, 60))
    # COP31 panel, right of hero
    d.rectangle([684, 142, 1000, 470], fill=(255, 255, 255))
    d.rectangle([684, 142, 1000, 470], outline=INK, width=3)
    d.rectangle([684, 142, 1000, 196], fill=RED)
    d.text((706, 152), "LIBYA", font=font(SANS_B, 22), fill=WHITE)
    d.text((706, 206), "WARSHIP", font=font(SERIF, 48), fill=INK)
    d.text((706, 262), "HIT AT SEA", font=font(SERIF, 38), fill=RED)
    text_block(d, 706, 322,
               "Suspected Ukrainian sea drones strike a Russian warship at Benghazi.",
               font(SANS, 21), INK, 272, 28)
    d.text((706, 436), "Second ship hit too", font=font(SANS_B, 18), fill=GREY)
    # middle grid: 4 stories, 2x2
    stories = [
        ("MEXICO", RED, "Cartel boss captured",
         "El Chapo Isidro seized in Sinaloa. 11 killed in the raid, four soldiers."),
        ("UKRAINE", INK, "Missile hits hometown",
         "A Russian strike on Kryvyi Rih kills a boy, 7, and a woman, 20. 60 wounded."),
        ("MARKETS", TEAL, "Stocks fall on AI fears",
         "S&P 500 down 3.7%, Nasdaq 5.3%. Japan's Nikkei drops 5.06%."),
        ("JUSTICE", NAVY, "Genocide verdict",
         "World Court: Myanmar committed genocide against the Rohingya in 2017."),
    ]
    x0, y0, cw, ch, gap = 24, 494, 476, 200, 24
    for i, (tag, col, head, body) in enumerate(stories):
        x = x0 + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=WHITE)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=2)
        d.rectangle([x, y, x + cw, y + 40], fill=col)
        d.text((x + 16, y + 8), tag, font=font(SANS_B, 20), fill=WHITE)
        text_block(d, x + 16, y + 52, head, font(SANS_B, 24), INK, cw - 32, 30)
        text_block(d, x + 16, y + 116, body, font(SANS, 19), GREY, cw - 32, 25)
    # bottom strip: sport + Gaza + Sudan
    d.rectangle([24, 942, 1000, 1000], fill=INK)
    d.text((40, 964), "BAHRAIN  Iran strikes, 2 injured  •  INDONESIA  Factory fire, 3 dead  •  USA  Democrats win 258",
           font=font(SANS_B, 15), fill=WHITE)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
