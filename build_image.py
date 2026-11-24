#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: 'THE DAILY GLOBE'.

A newspaper front page in black ink on cream paper. All facts come from
NEWS-BRIEF.md (verified 24 Nov 2026); nothing is invented. Deterministic:
same input, same bytes, no timestamps, no randomness, no network.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 240, 221)      # cream newsprint
INK = (20, 20, 20)          # near-black ink
FAINT = (90, 84, 70)        # muted grey-brown for small labels
RED = (139, 26, 26)         # dark red accent for kickers
SEA = (39, 75, 99)          # sea blue in the lead illustration
SKY = (205, 216, 222)       # pale sky in the lead illustration

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Regular.ttf")
SERIF_B = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "dejavu", "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, cx, y, text, fnt, fill, tracking=3):
    """Draw centred text with letter tracking."""
    total = sum(draw.textlength(ch, font=fnt) for ch in text) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return total


def rule(draw, x0, x1, y, weight=1):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=INK)


def draw_lead_illustration(draw, x, y, w, h):
    """Simple black-and-white scene: naval drones over a corvette at sea."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    # sky and sea
    horizon = y + int(h * 0.52)
    draw.rectangle([x + 2, y + 2, x + w - 2, horizon], fill=SKY)
    draw.rectangle([x + 2, horizon, x + w - 2, y + h - 2], fill=SEA)
    # haze lines in the sky
    for i, yy in enumerate(range(y + 14, horizon - 8, 13)):
        draw.line([(x + 14, yy), (x + 14 + 44 - i * 6, yy)], fill=(120, 130, 138), width=2)
    # corvette silhouette on the water
    hull_y = horizon + int(h * 0.22)
    hull = [
        (x + 52, hull_y), (x + w - 58, hull_y),
        (x + w - 78, hull_y + 20), (x + 66, hull_y + 20),
    ]
    draw.polygon(hull, fill=INK)
    # superstructure and mast
    draw.rectangle([x + 128, hull_y - 24, x + 196, hull_y], fill=INK)
    draw.rectangle([x + 156, hull_y - 40, x + 162, hull_y - 24], fill=INK)
    draw.rectangle([x + 148, hull_y - 46, x + 170, hull_y - 40], fill=INK)
    # explosion burst at the bow
    bx, by = x + w - 70, hull_y - 14
    for dx, dy in [(0, -15), (11, -9), (15, 2), (9, 11), (-2, 15),
                   (-13, 9), (-15, -2), (-9, -11)]:
        draw.line([(bx, by), (bx + dx, by + dy)], fill=(255, 196, 66), width=3)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 196, 66))
    # three naval drones above, with dashed attack lines to the ship
    for dx, dy in [(x + 62, y + 20), (x + 128, y + 11), (x + 196, y + 24)]:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
        draw.line([(dx - 9, dy - 6), (dx + 9, dy - 6)], fill=INK, width=2)
        draw.line([(dx - 9, dy + 6), (dx + 9, dy + 6)], fill=INK, width=2)
        yy = dy + 10
        while yy < hull_y - 4:
            draw.line([(dx, yy), (dx, min(yy + 6, hull_y - 4))], fill=INK, width=1)
            yy += 12
    # caption, small and clear of the burst
    cap = "UKRAINIAN DRONES STRIKE AT BENGHAZI"
    draw.text((x + 8, y + h - 17), cap, font=font(SANS_B, 9),
              fill=(240, 240, 240))


def draw_item(draw, x, y, width, head, body, head_size=15, body_size=13,
              body_leading=16, gap_after=7):
    """One dated news item: bold serif head + wrapped body. Returns next y."""
    hf = font(SERIF_B, head_size)
    bf = font(SERIF, body_size)
    lines = wrap(draw, head, hf, width)
    for ln in lines:
        draw.text((x, y), ln, font=hf, fill=INK)
        y += head_size + 4
    for ln in wrap(draw, body, bf, width):
        draw.text((x, y), ln, font=bf, fill=INK)
        y += body_leading
    return y + gap_after


def draw_section(draw, x, y, width, title, items):
    """A black section bar followed by its items. Returns next y."""
    bar_h = 26
    draw.rectangle([x, y, x + width, y + bar_h], fill=INK)
    draw.text((x + 10, y + 4), title, font=font(SANS_B, 14), fill=(246, 240, 221))
    y += bar_h + 8
    for head, body in items:
        y = draw_item(draw, x, y, width, head, body)
    return y


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # side margin
    L, R = M, W - M             # content left / right
    CW = R - L                  # 952

    # ---- top line -------------------------------------------------------
    draw_spaced(d, W / 2, 14, "THE WORLD IN ONE DAY", font(SANS_B, 14), FAINT, 4)

    # ---- masthead -------------------------------------------------------
    name = "THE DAILY GLOBE"
    nf = font(SERIF_B, 88)
    d.text((W / 2, 34), name, font=nf, fill=INK, anchor="ma")
    rule(d, L, R, 128, 4)
    rule(d, L, R, 136, 1)

    # ---- dateline -------------------------------------------------------
    d.text((L, 146), "MONDAY, 23 NOVEMBER 2026", font=font(SANS_B, 19), fill=INK)
    d.text((R, 148), "20 STORIES  ·  WORLD EDITION", font=font(SANS_B, 15),
           fill=INK, anchor="ra")
    rule(d, L, R, 172, 4)
    rule(d, L, R, 180, 1)

    # ---- lead story -----------------------------------------------------
    y = 194
    d.text((L, y), "UKRAINE WAR  —  LIBYA", font=font(SANS_B, 14), fill=RED)
    y += 22
    lead_head = "Ukraine sinks Russian warship off Libya"
    d.text((L, y), lead_head, font=font(SERIF_B, 38), fill=INK)
    y += 50
    lead_body = ("President Zelenskyy said on Monday that seven Ukrainian naval "
                 "drones sank the Russian corvette Merkury at Benghazi port on "
                 "Sunday. A second vessel was hit offshore; satellite images "
                 "and Libyan officials corroborated it.")
    ill_w, ill_h = 300, 140
    ill_x, ill_y = R - ill_w, y - 6
    text_w = ill_x - L - 24
    by = y
    for ln in wrap(d, lead_body, font(SERIF, 16), text_w):
        d.text((L, by), ln, font=font(SERIF, 16), fill=INK)
        by += 21
    # dateline tag under the lead text
    d.text((L, by + 6), "BENGHAZI, LIBYA — ", font=font(SANS_B, 12), fill=FAINT)
    d.text((L + d.textlength("BENGHAZI, LIBYA — ", font=font(SANS_B, 12)), by + 6),
           "Zelenskyy: seven drones, one corvette sunk",
           font=font(SERIF_I, 14), fill=FAINT)
    draw_lead_illustration(d, ill_x, ill_y, ill_w, ill_h)
    y = max(by + 32, ill_y + ill_h + 10)
    rule(d, L, R, y, 1)
    y += 12

    # ---- two half-width stories -----------------------------------------
    half_w = (CW - 24) // 2
    halves = [
        ("MARKETS",
         "Nvidia brings back Huang; shares jump a third",
         "Nvidia reinstated Jensen Huang as chief, 11 days after he resigned; "
         "shares jumped about 33%. The S&P 500 rose 4.82% after last week's "
         "sharp AI sell-off."),
        ("KYIV REGION",
         "Russian strike wrecks flats in Dymer; 11 killed",
         "A Russian drone and missile strike partly destroyed an apartment block "
         "in Dymer, north of Kyiv. At least 11 were killed and 14 missing; "
         "rescuers dug for survivors."),
    ]
    top = y
    max_y = y
    for i, (kick, head, body) in enumerate(halves):
        x = L + i * (half_w + 24)
        yy = top
        d.text((x, yy), kick, font=font(SANS_B, 13), fill=RED)
        yy += 20
        for ln in wrap(d, head, font(SERIF_B, 23), half_w):
            d.text((x, yy), ln, font=font(SERIF_B, 23), fill=INK)
            yy += 28
        yy += 2
        for ln in wrap(d, body, font(SERIF, 14), half_w):
            d.text((x, yy), ln, font=font(SERIF, 14), fill=INK)
            yy += 18
        max_y = max(max_y, yy)
    # vertical divider between the halves
    div_x = L + half_w + 12
    d.line([(div_x, top), (div_x, max_y)], fill=(180, 172, 150), width=1)
    y = max_y + 10
    rule(d, L, R, y, 4)
    y += 12

    # ---- three columns of dated sections --------------------------------
    col_w = (CW - 40) // 3
    cols = [
        ("WAR & DIPLOMACY", [
            ("Iran vows to defy US blockade",
             "Tehran will use all means against the US naval blockade; it says "
             "it downed a US drone."),
            ("Trump calls Putin \u2018my friend\u2019",
             "After a Shenzhen summit with Putin and Xi, Trump praised the "
             "Russian leader as a friend."),
            ("EU proposes 22nd sanctions package",
             "Brussels tabled a 22nd round of sanctions against Russia over "
             "the war in Ukraine."),
            ("NATO warns Russia in Berlin",
             "NATO warned Moscow and pledged space defence amid reports of a "
             "nuclear-armed satellite."),
            ("Poland revises missile account",
             "Debris at all three crash sites came from Russian Kh-101 "
             "missiles, prosecutors said."),
            ("Freighter Sparta II hit off Finland",
             "The Russian freighter caught fire in a drone strike; Finland "
             "blames Ukraine."),
        ]),
        ("AMERICAS", [
            ("Democrats\u2019 biggest House win since 1992",
             "At least 258 seats after Hubbard beat 11-term Rep. Virginia "
             "Foxx in North Carolina."),
            ("FBI probes police database hack",
             "Apparent breach of the national crime database of fugitives and "
             "missing persons."),
            ("\u2018El Chapo Isidro\u2019 captured",
             "Mexican forces seized the FBI most-wanted fugitive in Sinaloa, "
             "with US help."),
        ]),
        ("WORLD", [
            ("Indonesia factory-fire search goes on",
             "Rescuers searched a burned candy factory in Banten; deaths "
             "confirmed, workers missing."),
            ("Delta failure delays up to 2,000 flights",
             "A tech failure delayed 1,300\u20132,000 flights on Sunday; storms "
             "threaten holiday travel."),
            ("India pledges \u20ac1.4bn for Nepal rebuild",
             "India pledged about \u20ac1.4bn to rebuild after Nepal\u2019s deadly "
             "glacier flood."),
            ("Student protests sweep Europe",
             "Students marched across Europe for higher wages, lower rents, "
             "better schools."),
            ("Nigeria boat capsizes; 24 dead",
             "A boat carrying mourners to a funeral capsized in Bayelsa State."),
            ("Coalition talks fail in Israel",
             "Netanyahu\u2013Eisenkot talks ended with no deal; settlers torched "
             "homes in four villages."),
        ]),
    ]
    # second section in column 2, below AMERICAS
    col2_extra = ("CLIMATE & SCIENCE", [
        ("COP31 ends with no deal",
         "Antalya talks closed with no agreement, the first failure since "
         "2009; two days overrun."),
        ("BepiColombo checks before Mercury",
         "An orbit-entry problem on the ESA/JAXA mission needs checks before "
         "entry."),
    ])

    col_top = y
    ends = []
    for i, (title, items) in enumerate(cols):
        x = L + i * (col_w + 20)
        yy = draw_section(d, x, col_top, col_w, title, items)
        if i == 1:
            yy += 6  # ~14 px gap between sections sharing a column
            yy = draw_section(d, x, yy, col_w, col2_extra[0], col2_extra[1])
        ends.append(yy)
    # thin vertical dividers between columns, full column height
    for i in (0, 1):
        dvx = L + (i + 1) * col_w + i * 20 + 10
        d.line([(dvx, col_top), (dvx, max(ends))], fill=(180, 172, 150), width=1)
    print("column ends:", ends, "column top:", col_top)
    y = max(ends)

    # ---- footer ---------------------------------------------------------
    fy = 976
    rule(d, L, R, fy - 10, 1)
    d.text((W / 2, fy), "THE DAILY GLOBE  ·  MONDAY, 23 NOVEMBER 2026  ·  "
           "THE DAY\u2019S NEWS, AS REPORTED",
           font=font(SANS, 12), fill=FAINT, anchor="ma")
    img.save(path, format="PNG")
    print("saved", path, "content bottom:", y, "footer:", fy)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
