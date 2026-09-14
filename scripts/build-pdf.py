#!/usr/bin/env python3
"""
Build assets/talisha-grobler-media-kit.pdf, the downloadable one page
analytics sheet.

    python3 scripts/build-pdf.py

Writes a real vector PDF: text stays selectable and sharp at any zoom, and
the file lands around 10KB. It uses the PDF base-14 fonts (Helvetica), so
nothing is embedded and there are no dependencies to install.

All the figures live in the DATA block below. Change them there and re-run;
remember to change the matching numbers in index.html too.
"""
import os, zlib

# ── The figures ────────────────────────────────────────────────
UPDATED   = "September 2026"
IG_WINDOW = "90 days to 12 Sep"
TT_WINDOW = "31 May to 11 Sep"

HEADLINE = [
    ("79.1K",  "Instagram followers", "@talisha.grobler"),
    ("323.6K", "TikTok followers",    "@talishagrobler"),
    ("12M",    "Views",               "last 3 months"),
    ("654K",   "Interactions",        "last 3 months"),
    ("80%",    "Aged 18 to 34",       "across both"),
    ("75%",    "South African",       "on Instagram"),
]

GENDER = [("Instagram", 61.8, 38.2), ("TikTok", 55.0, 45.0)]

AGE = [  # band, instagram %, tiktok % (None = platform doesn't report it)
    ("13-17", 11.1, None),
    ("18-24", 50.2, 50.6),
    ("25-34", 27.2, 32.8),
    ("35-44",  7.4,  9.6),
    ("45-54",  2.9,  4.3),
    ("55+",    1.2,  2.7),
]

IG_LOC = [("South Africa", 75.1), ("United States", 7.7), ("United Kingdom", 3.1),
          ("Australia", 2.0), ("Namibia", 1.2)]
TT_LOC = [("South Africa", 44.5), ("United States", 5.0), ("United Kingdom", 4.6),
          ("Australia", 3.9), ("Canada", 2.1)]

IG_MIX = [("Stories", 3.4, "3.4M"), ("Posts", 1.4, "1.4M"), ("Reels", 0.593, "593K")]
TT_SRC = [("For You", 72.2, "72.2%"), ("My profile", 17.6, "17.6%"),
          ("Search", 7.6, "7.6%"), ("Following", 2.3, "2.3%"), ("Sound", 0.3, "0.3%")]

# ── Colours, matching the site ─────────────────────────────────
IG    = (1.00, 0.176, 0.435)   # #FF2D6F
IG_S  = (1.00, 0.760, 0.839)   # #FFC2D6
TT    = (0.165, 0.471, 0.839)  # #2A78D6
TT_S  = (0.725, 0.831, 0.961)  # #B9D4F5
INK   = (0.075, 0.071, 0.082)
SOFT  = (0.361, 0.353, 0.380)
MUTE  = (0.557, 0.545, 0.576)
LINE  = (0.918, 0.906, 0.894)
TRACK = (0.937, 0.925, 0.910)
TINT  = (0.973, 0.965, 0.957)

W, H = 595.28, 841.89
M = 44.0
CW = W - 2 * M


class Page:
    """Draws in top-down coordinates and converts to PDF's bottom-up space."""

    def __init__(self):
        self.ops = []

    def _y(self, y):
        return H - y

    def rect(self, x, y, w, h, color):
        r, g, b = color
        self.ops.append(f"{r:.4f} {g:.4f} {b:.4f} rg "
                        f"{x:.2f} {self._y(y + h):.2f} {w:.2f} {h:.2f} re f")

    def rrect(self, x, y, w, h, rad, color):
        """Rounded rectangle, four bezier corners."""
        rad = min(rad, w / 2, h / 2)
        if rad <= 0.2:
            return self.rect(x, y, w, h, color)
        r, g, b = color
        k = rad * 0.5523
        y0, y1 = self._y(y + h), self._y(y)   # bottom, top
        x1 = x + w
        o = [f"{r:.4f} {g:.4f} {b:.4f} rg", f"{x + rad:.2f} {y0:.2f} m"]
        o.append(f"{x1 - rad:.2f} {y0:.2f} l")
        o.append(f"{x1 - rad + k:.2f} {y0:.2f} {x1:.2f} {y0 + rad - k:.2f} {x1:.2f} {y0 + rad:.2f} c")
        o.append(f"{x1:.2f} {y1 - rad:.2f} l")
        o.append(f"{x1:.2f} {y1 - rad + k:.2f} {x1 - rad + k:.2f} {y1:.2f} {x1 - rad:.2f} {y1:.2f} c")
        o.append(f"{x + rad:.2f} {y1:.2f} l")
        o.append(f"{x + rad - k:.2f} {y1:.2f} {x:.2f} {y1 - rad + k:.2f} {x:.2f} {y1 - rad:.2f} c")
        o.append(f"{x:.2f} {y0 + rad:.2f} l")
        o.append(f"{x:.2f} {y0 + rad - k:.2f} {x + rad - k:.2f} {y0:.2f} {x + rad:.2f} {y0:.2f} c")
        o.append("f")
        self.ops.append(" ".join(o))

    def line(self, x, y, w, color=LINE, weight=0.7):
        r, g, b = color
        self.ops.append(f"{r:.4f} {g:.4f} {b:.4f} RG {weight} w "
                        f"{x:.2f} {self._y(y):.2f} m {x + w:.2f} {self._y(y):.2f} l S")

    def text(self, x, y, s, size=9.5, bold=False, color=INK, align="left", track=0.0):
        font = "F2" if bold else "F1"
        s = str(s)
        if align != "left":
            wid = width_of(s, size, bold) + track * max(len(s) - 1, 0)
            x = x - wid if align == "right" else x - wid / 2
        esc = s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        r, g, b = color
        tc = f" {track:.2f} Tc" if track else ""
        self.ops.append(f"BT /{font} {size} Tf{tc} {r:.4f} {g:.4f} {b:.4f} rg "
                        f"{x:.2f} {self._y(y):.2f} Td ({esc}) Tj ET")

    def arc(self, cx, cy, r, a0, a1, width, color):
        """Stroked circular arc, angles in degrees measured counter-clockwise
        from east. Split into <=90 degree bezier spans so the curve stays
        accurate (a single bezier can't hold a half circle)."""
        import math
        r_, g_, b_ = color
        cy = self._y(cy)
        span = a1 - a0
        n = max(1, int(math.ceil(abs(span) / 90.0)))
        step = span / n
        o = [f"{r_:.4f} {g_:.4f} {b_:.4f} RG {width:.2f} w 1 J"]
        t0 = math.radians(a0)
        o.append(f"{cx + r * math.cos(t0):.2f} {cy + r * math.sin(t0):.2f} m")
        for i in range(n):
            s0 = math.radians(a0 + step * i)
            s1 = math.radians(a0 + step * (i + 1))
            k = 4.0 / 3.0 * math.tan((s1 - s0) / 4.0)
            x0, y0 = cx + r * math.cos(s0), cy + r * math.sin(s0)
            x3, y3 = cx + r * math.cos(s1), cy + r * math.sin(s1)
            x1, y1 = x0 - k * r * math.sin(s0), y0 + k * r * math.cos(s0)
            x2, y2 = x3 + k * r * math.sin(s1), y3 - k * r * math.cos(s1)
            o.append(f"{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f} {x3:.2f} {y3:.2f} c")
        o.append("S")
        self.ops.append(" ".join(o))

    def stream(self):
        return "\n".join(self.ops).encode("latin-1", "replace")


# Helvetica advance widths (units/1000) for the ASCII range, so text can be
# right-aligned and centred without measuring at render time.
_W = {}
for c in range(32, 127):
    _W[chr(c)] = 556
for c, w in {' ':278,'!':278,'"':355,'#':556,'$':556,'%':889,'&':667,"'":191,'(':333,')':333,
             '*':389,'+':584,',':278,'-':333,'.':278,'/':278,':':278,';':278,'<':584,'=':584,
             '>':584,'?':556,'@':1015,'[':278,'\\':278,']':278,'^':469,'_':556,'`':333,
             '{':334,'|':260,'}':334,'~':584}.items():
    _W[c] = w
for c, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,
                 667,778,722,667,611,722,667,944,667,667,611]):
    _W[c] = w
for c, w in zip("abcdefghijklmnopqrstuvwxyz",
                [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,
                 556,556,333,500,278,556,500,722,500,500,500]):
    _W[c] = w
_WB = dict(_W)
for c, w in zip("abcdefghijklmnopqrstuvwxyz",
                [556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,
                 611,611,389,556,333,611,556,778,556,556,500]):
    _WB[c] = w
for c, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                [722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,
                 667,778,722,667,611,722,667,944,667,667,611]):
    _WB[c] = w


def width_of(s, size, bold=False):
    table = _WB if bold else _W
    return sum(table.get(ch, 556) for ch in str(s)) * size / 1000.0


# ── Layout ─────────────────────────────────────────────────────
def bar_list(p, x, y, width, rows, colour, maxv, label_w=88, val_w=44):
    """One bar per row: label, track, value. The same shape as the bar
    lists on the site."""
    tx = x + label_w + 10
    tw = width - label_w - val_w - 20
    for label, val, shown in rows:
        p.text(x, y + 6.6, label, 8.2, color=SOFT)
        p.rrect(tx, y + 1.5, tw, 7, 3.5, TRACK)
        if val is None:
            p.text(x + width, y + 6.6, "n/a", 8.2, color=MUTE, align="right")
        else:
            p.rrect(tx, y + 1.5, max(tw * val / maxv, 3), 7, 3.5, colour)
            p.text(x + width, y + 6.6, shown, 8.2, bold=True, align="right")
        y += 15.5
    return y


def gauge(p, cx, y, women, colour, soft, label):
    """Half-donut, the same mark as the gender gauges on the site: a full
    light arc with the women's share drawn over it, and the figure sitting
    in the arc's opening."""
    r, wdt = 34, 11
    cy = y + r
    p.arc(cx, cy, r, 0, 180, wdt, soft)
    sweep = 180.0 * women / 100.0
    if sweep > 2:
        p.arc(cx, cy, r, 180 - sweep + 1.5, 180, wdt, colour)
    p.text(cx, cy - 2, f"{women:g}%", 14.5, bold=True, align="center")
    p.text(cx, cy + 8, "WOMEN", 6.4, color=MUTE, align="center", track=0.7)
    p.text(cx, cy + 24, label, 8, color=SOFT, align="center")
    return cy + 32


def build():
    p = Page()
    y = M

    # Header
    p.text(M, y + 24, "Talisha Grobler", 27, bold=True)
    p.text(M, y + 42, "Content creator, South Africa.", 9.6, color=SOFT)
    p.text(W - M, y + 24, "Audience &", 9.6, bold=True, color=MUTE, align="right")
    p.text(W - M, y + 36, "analytics", 9.6, bold=True, color=MUTE, align="right")
    p.text(W - M, y + 50, UPDATED, 8.6, color=MUTE, align="right")
    y += 58
    p.line(M, y, CW)
    y += 26

    # Headline figures
    col = CW / 3
    for i, (val, label, note) in enumerate(HEADLINE):
        cx = M + (i % 3) * col
        cy = y + (i // 3) * 52
        p.text(cx, cy + 15, val, 19, bold=True)
        p.text(cx, cy + 28, label, 8.6, color=SOFT)
        p.text(cx, cy + 39, note, 8.0, color=MUTE)
    y += 104
    p.line(M, y, CW)
    y += 24

    half = CW / 2 - 14
    right = M + CW / 2 + 14

    # Gender gauges
    p.text(M, y, "Gender", 12, bold=True)
    y += 14
    b1 = gauge(p, M + half / 2, y, GENDER[0][1], IG, IG_S, "Instagram")
    b2 = gauge(p, right + half / 2, y, GENDER[1][1], TT, TT_S, "TikTok")
    y = max(b1, b2) + 22

    # Age, one panel per platform
    p.text(M, y, "Age range", 12, bold=True)
    y += 16
    ig_age = [(b, i, f"{i:g}%" if i is not None else None) for b, i, _ in AGE]
    tt_age = [(b, t, f"{t:g}%" if t is not None else None) for b, _, t in AGE]
    for cx, name in ((M, "INSTAGRAM"), (right, "TIKTOK")):
        p.text(cx, y, name, 7.4, bold=True, color=MUTE, track=0.7)
    y += 12
    e1 = bar_list(p, M, y, half, ig_age, IG, 55)
    e2 = bar_list(p, right, y, half, tt_age, TT, 55)
    y = max(e1, e2) + 18

    # Locations
    p.text(M, y, "Top locations", 12, bold=True)
    y += 16
    for cx, name in ((M, "INSTAGRAM"), (right, "TIKTOK")):
        p.text(cx, y, name, 7.4, bold=True, color=MUTE, track=0.7)
    y += 12
    e1 = bar_list(p, M, y, half, [(l, v, f"{v:.1f}%") for l, v in IG_LOC], IG, 80)
    e2 = bar_list(p, right, y, half, [(l, v, f"{v:.1f}%") for l, v in TT_LOC], TT, 80)
    y = max(e1, e2) + 18

    # Views by format and traffic source
    p.text(M, y, "Views by format", 12, bold=True)
    p.text(right, y, "Traffic source", 12, bold=True)
    y += 16
    for cx, name in ((M, "INSTAGRAM"), (right, "TIKTOK")):
        p.text(cx, y, name, 7.4, bold=True, color=MUTE, track=0.7)
    y += 12
    e1 = bar_list(p, M, y, half, [(l, v, sh) for l, v, sh in IG_MIX], IG, 3.4)
    e2 = bar_list(p, right, y, half, [(l, v, sh) for l, v, sh in TT_SRC], TT, 80)
    y = max(e1, e2) + 18

    # Footer
    p.line(M, y, CW)
    y += 15
    line1 = f"Instagram Insights, {IG_WINDOW}.  TikTok Analytics, {TT_WINDOW}."
    line2 = ("TikTok does not report 13-17.  Instagram's 55-64 and 65+ are "
             "combined as 55+ to match TikTok's bracket.")
    email = "management@talishagrobler.com"
    gap = CW - width_of(line1, 7.6) - width_of(email, 9, bold=True)
    assert gap > 10, f"footer line 1 collides with the email ({gap:.0f}pt clearance)"
    p.text(M, y, line1, 7.6, color=MUTE)
    p.text(M, y + 10, line2, 7.6, color=MUTE)
    p.text(W - M, y, email, 9, bold=True, align="right")
    p.text(W - M, y + 11, "talishagrobler.com", 8.4, color=MUTE, align="right")

    assert y + 20 < H - 20, f"content overflows the page (bottom at {y + 20:.0f}pt of {H:.0f})"
    return p


def write_pdf(page, path):
    content = zlib.compress(page.stream())
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W:.2f} {H:.2f}] "
         f"/Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>").encode(),
        b"<< /Length " + str(len(content)).encode() + b" /Filter /FlateDecode >>\nstream\n"
        + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        b"<< /Title (Talisha Grobler, audience and analytics) "
        b"/Author (Talisha Grobler) /Creator (talishagrobler.com) >>",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R /Info 7 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    with open(path, "wb") as fh:
        fh.write(out)
    return len(out)


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(here, "assets", "talisha-grobler-media-kit.pdf")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    size = write_pdf(build(), dest)
    print(f"wrote {dest}  ({size:,} bytes)")
