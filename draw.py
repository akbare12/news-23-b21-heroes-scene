#!/usr/bin/env python3
"""Draw news-23 b21 heroes-scene entry: THE WORLD TODAY, Monday 23 Nov 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (16, 32, 64)
DARK = (24, 24, 28)
GREY = (110, 108, 100)
LINE = (200, 192, 172)
MAP_BG = (223, 233, 238)
LAND = (232, 220, 192)
AMBER = (176, 120, 0)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill, lh=None):
    lh = lh or int(font.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = F(SANS_B, 8)
    w_ = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w_, y + 13], radius=3, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return w_


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- top rule + masthead ----------
    d.rectangle([0, 0, W, 4], fill=RED)
    d.text((16, 10), "THE WORLD TODAY", font=F(SERIF_B, 56), fill=INK)
    d.text((W - 16 - d.textlength("31 STORIES", font=F(SANS_B, 16)), 16),
           "31 STORIES", font=F(SANS_B, 16), fill=INK)
    d.text((W - 16 - d.textlength("6 REGIONS", font=F(SANS_B, 16)), 36),
           "6 REGIONS", font=F(SANS_B, 16), fill=INK)
    d.line([16, 72, W - 16, 72], fill=INK, width=2)
    d.text((16, 76), "MONDAY 23 NOVEMBER 2026", font=F(SANS_B, 17), fill=RED)
    kr = "AI ROUT  ·  AI RULES  ·  POWER SHIFT"
    d.text((W - 16 - d.textlength(kr, font=F(SANS_B, 12)), 80), kr,
           font=F(SANS_B, 12), fill=GREY)

    # ---------- number strip ----------
    nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"),
            ("11,762", "EBOLA CASES"), ("10T WON", "SEOUL FUND"),
            ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
    y0, y1 = 100, 142
    cw = (W - 32) / 6
    for i, (n, lab) in enumerate(nums):
        x = 16 + i * cw
        d.line([x, y0 + 4, x, y1 - 4], fill=LINE, width=1)
        f = F(SANS_B, 24 if len(n) < 7 else 20)
        d.text((x + cw / 2 - d.textlength(n, font=f) / 2, y0 + 4), n, font=f, fill=RED)
        fl = F(SANS_B, 9)
        d.text((x + cw / 2 - d.textlength(lab, font=fl) / 2, y0 + 32), lab, font=fl, fill=INK)
    d.line([16, y1, W - 16, y1], fill=INK, width=1)

    # ---------- region bar ----------
    regions = [("NORTH AMERICA 8", (31, 90, 160)), ("EUROPE 6", (198, 110, 20)),
               ("MIDDLE EAST 6", (122, 60, 160)), ("ASIA-PACIFIC 6", (16, 130, 120)),
               ("AFRICA 3", (150, 100, 40)), ("WORLD 2", (100, 100, 100))]
    y0, y1 = 146, 168
    x = 16
    total = W - 32
    widths = [0.24, 0.18, 0.19, 0.19, 0.11, 0.09]
    for (lab, col), wf in zip(regions, widths):
        w_ = total * wf
        d.rectangle([x, y0, x + w_, y1], fill=col)
        f = F(SANS_B, 10)
        d.text((x + w_ / 2 - d.textlength(lab, font=f) / 2, y0 + 5), lab, font=f, fill=(255, 255, 255))
        x += w_

    # ---------- UTC strip ----------
    d.rectangle([16, 172, W - 16, 192], fill=NAVY)
    f = F(SANS_B, 10)
    utc = "THE DAY IN UTC    ~00:00 ASIA OPENS  ·  06:30 KOSPI -3.3%  ·  ~09:00 SEOUL FUND  ·  14:30 WALL ST +3%  ·  ~16:00 GUTERRES  ·  ~21:00 FBI HACK   (~ = APPROX.)"
    d.text((22, 177), utc, font=f, fill=(255, 255, 255))

    # ---------- hero scenes ----------
    hy, hh = 198, 118  # scene area
    hw = 320
    hx = [16, 352, 688]
    # --- scene 1: Kospi chart over Seoul skyline ---
    d.rectangle([hx[0], hy, hx[0] + hw, hy + hh], fill=(10, 18, 38))
    # skyline
    import random
    random.seed(7)
    bx = hx[0] + 8
    while bx < hx[0] + hw - 14:
        bw_ = random.randint(14, 26)
        bh_ = random.randint(28, 78)
        d.rectangle([bx, hy + hh - bh_, bx + bw_, hy + hh], fill=(30, 42, 66))
        for wy in range(hy + hh - bh_ + 6, hy + hh - 6, 9):
            for wx in range(bx + 3, bx + bw_ - 3, 7):
                if random.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 90))
        bx += bw_ + 4
    pts = [(hx[0] + 10, hy + 22), (hx[0] + 70, hy + 38), (hx[0] + 130, hy + 30),
           (hx[0] + 190, hy + 62), (hx[0] + 250, hy + 78), (hx[0] + 310, hy + 108)]
    d.line(pts, fill=(255, 80, 80), width=3)
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 255, 255),
                  outline=(255, 80, 80))
    d.text((hx[0] + 10, hy + 2), "intraday -5.8%", font=F(SANS_B, 11), fill=(255, 255, 255))
    d.text((hx[0] + hw - 88, hy + 8), "-3.3%", font=F(SANS_B, 30), fill=(255, 80, 80))
    # --- scene 2: globe + network + podium ---
    d.rectangle([hx[1], hy, hx[1] + hw, hy + hh], fill=(14, 40, 74))
    cx, cy, r = hx[1] + 62, hy + 64, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 210))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 225, 245), width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(200, 225, 245))
    d.line([cx - r, cy, cx + r, cy], fill=(200, 225, 245), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(200, 225, 245))
    nodes = [(hx[1] + 170, hy + 22), (hx[1] + 215, hy + 48), (hx[1] + 185, hy + 80),
             (hx[1] + 240, hy + 92), (hx[1] + 265, hy + 40), (hx[1] + 290, hy + 78),
             (hx[1] + 205, hy + 108), (hx[1] + 260, hy + 112)]
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            d.line([a, b], fill=(140, 180, 230), width=1)
    for a in nodes:
        d.ellipse([a[0] - 4, a[1] - 4, a[0] + 4, a[1] + 4], fill=(255, 205, 90))
    # podium silhouette
    px = hx[1] + 148
    d.ellipse([px + 6, hy + 84, px + 18, hy + 96], fill=(10, 10, 14))
    d.polygon([(px, hy + 96), (px + 24, hy + 96), (px + 20, hy + 118), (px + 4, hy + 118)],
              fill=(10, 10, 14))
    d.rectangle([hx[1] + 8, hy + 6, hx[1] + 118, hy + 22], fill=(255, 205, 90))
    d.text((hx[1] + 13, hy + 8), "150 DELEGATES", font=F(SANS_B, 10), fill=(17, 17, 17))
    # --- scene 3: power index bars ---
    d.rectangle([hx[2], hy, hx[2] + hw, hy + hh], fill=(245, 240, 228))
    d.text((hx[2] + 10, hy + 6), "ASIA POWER INDEX 2026", font=F(SANS_B, 12), fill=INK)
    by = hy + 32
    d.text((hx[2] + 10, by), "US", font=F(SANS_B, 12), fill=INK)
    d.rectangle([hx[2] + 62, by, hx[2] + 62 + 190, by + 16], fill=(31, 90, 160))
    d.text((hx[2] + 258, by), "78.9", font=F(SANS_B, 12), fill=INK)
    by += 24
    d.text((hx[2] + 10, by), "CHINA", font=F(SANS_B, 12), fill=INK)
    d.rectangle([hx[2] + 62, by, hx[2] + 62 + 177, by + 16], fill=RED)
    d.text((hx[2] + 245, by), "73.6", font=F(SANS_B, 12), fill=INK)
    by += 24
    d.text((hx[2] + 10, by), "INDIA 3rd", font=F(SANS_B, 10), fill=INK)
    d.rectangle([hx[2] + 74, by, hx[2] + 74 + 98, by + 14], fill=(150, 150, 150))
    d.text((hx[2] + 178, by), "40.5", font=F(SANS_B, 10), fill=INK)
    d.text((hx[2] + 10, hy + 100), "GAP 5.3", font=F(SANS_B, 15), fill=RED)
    d.text((hx[2] + 92, hy + 102), "narrowest since 2018", font=F(SANS_B, 11), fill=INK)

    # ---------- hero text blocks ----------
    heroes = [
        ("#1 ASIA · MARKETS", "AI ROUT HITS ASIA",
         "Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%.",
         "Source: Yonhap · Korea JoongAng", "REPORTED", (34, 139, 34)),
        ("#2 WORLD · UNITED NATIONS", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "Source: UN News · Reuters", "REPORTED", (34, 139, 34)),
        ("#3 ASIA-PACIFIC · POWER", "US LEAD OVER CHINA AT RECORD LOW",
         "Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
         "Source: Lowy Institute", "REPORTED", (34, 139, 34)),
    ]
    ty = hy + hh + 6
    for (kick, head, body, src, ch, chcol), x in zip(heroes, hx):
        d.text((x, ty), kick, font=F(SANS_B, 9), fill=RED)
        lines = wrap(d, head, F(SANS_B, 14), hw)
        y = text_block(d, x, ty + 12, lines[:2], F(SANS_B, 14), INK, lh=16)
        bl = wrap(d, body, F(SANS, 10), hw)
        y = text_block(d, x, y + 2, bl[:2], F(SANS, 10), INK, lh=12)
        d.text((x, ty + 72), src, font=F(SANS, 8), fill=GREY)
        chip(d, x + hw - 62, ty + 70, ch, chcol)
    d.line([16, 404, W - 16, 404], fill=INK, width=1)

    # ---------- 10 small cards ----------
    cards = [
        ("#4", "SPORT · US", (31, 90, 160), "Skubal signs $450M Mets deal",
         "Two-time Cy Young winner, nine years — the largest ever for a pitcher.", "ESPN", "REPORTED", (34, 139, 34)),
        ("#5", "TECH · US", (31, 90, 160), "Anthropic IPO: $107.3B, largest ever",
         "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.", "Bloomberg", "REPORTED", (34, 139, 34)),
        ("#6", "EUROPE · WAR", (198, 110, 20), "Poland: 3 Russian missiles crossed airspace",
         "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.", "AP", "CLAIM", AMBER),
        ("#7", "EUROPE · SECURITY", (198, 110, 20), "Intel warns of Russian nuclear satellite",
         "Moscow built a satellite to carry a nuclear warhead; launch possible next month.", "Bloomberg", "CLAIM", AMBER),
        ("#8", "EUROPE · ECONOMY", (198, 110, 20), "Paris: 100+ back 2% billionaire tax",
         "Economists, politicians and unions rally behind France's 2% minimum wealth tax.", "AFP", "REPORTED", (34, 139, 34)),
        ("#9", "EUROPE · UK", (198, 110, 20), "Manchester: 12,000 cleared after scare",
         "Substance scare empties arena district; no casualties reported.", "AP", "REPORTED", (34, 139, 34)),
        ("#10", "EUROPE · WAR", (198, 110, 20), "Zelenskyy: 165 Russian missiles in a week",
         "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.", "Kyiv", "CLAIM", AMBER),
        ("#11", "WORLD · CLIMATE", (100, 100, 100), "COP31: the day after",
         "Sunday's collapse — 194 nations reject the Antalya pact — draws fury; Guterres 'profoundly frustrated'.", "CNN", "REPORTED", (34, 139, 34)),
        ("#12", "AFRICA · LIBYA", (150, 100, 40), "Benghazi: UN demands probe of port attacks",
         "Drones hit two Russian ships; UN calls for an investigation.", "UN News", "CLAIM", AMBER),
        ("#13", "MIDDLE EAST · ISRAEL", (122, 60, 160), "Israel unity talks resume",
         "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.", "Reuters", "ONGOING", (16, 90, 160)),
    ]
    cw = 192
    gap = 8
    cx0, cy0 = 16, 412
    for i, (num, kick, col, title, body, src, ch, chcol) in enumerate(cards):
        x = cx0 + (i % 5) * (cw + gap)
        y = cy0 + (i // 5) * 104
        d.rectangle([x, y, x + cw, y + 100], outline=LINE, width=1)
        d.rectangle([x, y, x + cw, y + 16], fill=col)
        d.text((x + 5, y + 3), num, font=F(SANS_B, 9), fill=(255, 255, 255))
        d.text((x + 30, y + 3), kick, font=F(SANS_B, 8), fill=(255, 255, 255))
        tl = wrap(d, title, F(SANS_B, 11), cw - 10)
        yy = text_block(d, x + 5, y + 20, tl[:2], F(SANS_B, 11), INK, lh=13)
        bl = wrap(d, body, F(SANS, 9), cw - 10)
        yy = text_block(d, x + 5, yy + 2, bl[:3], F(SANS, 9), INK, lh=11)
        d.text((x + 5, y + 86), src, font=F(SANS, 8), fill=GREY)
        chip(d, x + cw - 62, y + 84, ch, chcol)

    # ---------- map + ALSO ----------
    my0, my1 = 624, 890
    d.text((16, my0), "THE WORLD — WHERE IT HAPPENED", font=F(SANS_B, 12), fill=RED)
    d.text((16, my0 + 16), "PIN = STORY NUMBER", font=F(SANS_B, 8), fill=GREY)
    mx0, mx1, myy0, myy1 = 16, 592, my0 + 32, my1
    d.rectangle([mx0, myy0, mx1, myy1], fill=MAP_BG, outline=LINE)
    for gx in range(mx0, mx1, 48):
        d.line([gx, myy0, gx, myy1], fill=(210, 222, 228), width=1)
    for gy in range(myy0, myy1, 36):
        d.line([mx0, gy, mx1, gy], fill=(210, 222, 228), width=1)
    # simplified continents (lon/lat polygons, rough)
    def ll(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                myy0 + (90 - lat) / 180 * (myy1 - myy0))
    continents = [
        # North America
        [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
         (-70, 62), (-55, 47), (-60, 44), (-75, 35), (-80, 26), (-90, 21),
         (-97, 16), (-105, 20), (-117, 33), (-125, 49), (-150, 60), (-168, 66)],
        # South America
        [(-80, 9), (-72, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
         (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -37), (-70, -18),
         (-80, -3), (-80, 9)],
        # Europe
        [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55),
         (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (45, 60),
         (40, 47), (30, 46), (28, 41), (23, 36), (19, 40), (12, 44), (8, 44),
         (3, 42), (-10, 36)],
        # Africa
        [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11),
         (48, 0), (40, -10), (35, -18), (32, -26), (26, -34), (19, -35), (15, -27),
         (12, -18), (9, -1), (9, 4), (-8, 5), (-17, 15), (-17, 25), (-6, 35)],
        # Asia
        [(40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (100, 77), (120, 73),
         (140, 72), (160, 70), (178, 65), (170, 60), (162, 56), (158, 52),
         (142, 50), (140, 40), (130, 33), (127, 35), (122, 30), (120, 22),
         (110, 20), (105, 9), (100, 7), (97, 16), (92, 21), (89, 22), (80, 13),
         (77, 8), (73, 20), (66, 25), (61, 25), (57, 26), (52, 28), (48, 30),
         (44, 29), (40, 36), (36, 36), (30, 36), (35, 42), (40, 47), (40, 60), (40, 68)],
        # Oceania
        [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
         (150, -37), (153, -27), (146, -19), (142, -11), (135, -12), (130, -13),
         (122, -17), (113, -22)],
    ]
    for poly in continents:
        d.polygon([ll(lon, lat) for lon, lat in poly], fill=LAND)
    pins = [
        (1, 126.9, 37.5, "R"), (2, -59.6, 13.1, "R"), (3, -150, -28, "R"),
        (4, -74.0, 40.7, "R"), (5, -122.4, 37.8, "R"), (6, 21.0, 52.2, "A"),
        (7, 37.6, 55.7, "A"), (8, 2.35, 48.85, "R"), (9, -2.24, 53.48, "R"),
        (10, 30.5, 50.45, "A"), (11, 30.7, 36.9, "R"), (12, 20.07, 32.1, "A"),
        (13, 35.2, 31.8, "R"), (14, 34.45, 31.5, "R"), (15, 35.6, 32.1, "R"),
        (16, 51.4, 35.7, "R"), (17, 35.5, 33.9, "R"), (18, 50.6, 26.2, "R"),
        (19, 32.5, 15.6, "R"), (20, 29.5, 1.5, "R"), (21, 90.4, 23.8, "R"),
        (22, 128.5, 36.0, "R"), (23, 129.5, 38.5, "R"), (24, 116.4, 39.9, "R"),
        (25, 124.5, 35.0, "R"), (26, -77.0, 38.9, "R"), (27, -74.5, 40.2, "R"),
        (28, -79.5, 37.5, "R"), (29, -73.0, 42.5, "R"), (30, -105.0, 39.7, "R"),
        (31, -97.7, 30.3, "R"),
    ]
    for num, lon, lat, kind in pins:
        x, y = ll(lon, lat)
        col = RED if kind == "R" else AMBER
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col, outline=(255, 255, 255))
        f = F(SANS_B, 7)
        t = str(num)
        d.text((x - d.textlength(t, font=f) / 2, y - 5), t, font=f, fill=(255, 255, 255))
    d.text((mx0 + 6, myy1 - 14), "N ↑", font=F(SANS_B, 9), fill=INK)

    # ALSO list
    ax = 608
    d.text((ax, my0), "ALSO ON MONDAY — 18 MORE STORIES", font=F(SANS_B, 12), fill=RED)
    also = [
        ("MIDDLE EAST", [
            "14  Gaza: two killed in Israeli strike",
            "15  West Bank: settler attacks hit villages",
            "16  Iran war: no deal in sight",
            "17  Lebanon seizes 264 kg of explosives",
            "18  Bahrain: Iran strike hits plant, 2 hurt"]),
        ("AFRICA", [
            "19  Sudan: air defences down drones over Khartoum",
            "20  DRC: fighting traps Ebola teams"]),
        ("ASIA-PACIFIC", [
            "21  Bangladesh: Hasina jailed if she returns",
            "22  Seoul minister quits over AI exam chaos",
            "23  SK Telecom -7.3% as Anthropic hype cools",
            "24  China eases margin rules to calm rout",
            "25  Seoul readies 10T-won stabilisation fund"]),
        ("NORTH AMERICA", [
            "26  Bessent demands Nvidia answers",
            "27  FBI probes hack of police database",
            "28  Trump: Iran strikes may resume in New Year",
            "29  US futures jump 3% holiday week",
            "30  Tom Jackson dies at 75"]),
        ("WORLD", [
            "31  States sue SpaceX over AI safety claims"]),
    ]
    y = my0 + 18
    for head, items in also:
        d.text((ax, y), head, font=F(SANS_B, 9), fill=RED)
        y += 11
        for it in items:
            d.text((ax, y), it, font=F(SANS, 9), fill=INK)
            y += 10
        y += 2

    # ---------- DATE CHECK ----------
    d.rectangle([16, 898, W - 16, 966], outline=RED, width=2)
    d.text((24, 904), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
    d.text((24 + d.textlength("DATE CHECK  ", font=F(SANS_B, 12)), 905),
           "Every story above happened or was first reported on Monday 23 November 2026.",
           font=F(SANS_B, 10), fill=INK)
    d.text((W - 16 - d.textlength("WIRES READ UP TO 23:00 UTC", font=F(SANS_B, 9)), 906),
           "WIRES READ UP TO 23:00 UTC", font=F(SANS_B, 9), fill=RED)
    d.text((24, 922), "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
           font=F(SANS, 10), fill=INK)
    d.text((24, 936), "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).",
           font=F(SANS, 10), fill=INK)
    d.text((24, 950), "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
           font=F(SANS, 10), fill=INK)

    # ---------- footer ----------
    d.text((16, 972), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
           font=F(SANS, 8), fill=GREY)
    d.text((16, 984), "CONFIRMED = 2+ outlets · REPORTED = carried by a wire · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified).",
           font=F(SANS, 8), fill=GREY)
    d.text((16, 998), "THE WORLD TODAY · 23 NOV 2026", font=F(SANS_B, 8), fill=INK)
    d.text((W - 16 - d.textlength("Scenes are drawn illustrations, not photographs.", font=F(SANS, 8)), 998),
           "Scenes are drawn illustrations, not photographs.", font=F(SANS, 8), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
