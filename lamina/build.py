"""
Genera la làmina A3 (HTML + SVG vectorial) de la pràctica L1 i l'exporta a PDF.

    python3 render.py      # (un cop) render isomètric -> assets/render_iso.png
    python3 build.py       # lamina.html -> EXAR_L1_Addami_Ech_Chaouy_Ziad.pdf
"""
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
import cadira_breuer as cb  # noqa: E402
from cadira_breuer import M, t, W, D, H  # noqa: E402

# ---------------------------------------------------------------- paleta
BG0, BG1 = "#1d2742", "#2b3b63"
INK = "#ece8e1"        # línies i text principal
MUTED = "#9fabc2"      # cotes, text secundari
ACCENT = "#d98a55"     # làmines / accent
AX = {"z": INK, "y": "#e3c27a", "x": "#7fa6d6"}

ALUMNE = "Ziad Addami Ech Chaouy"
PROFESSOR = "De Castro Losada, Rubén"
GRUP = "D3012"
DATA = "05/10/2026"

SOLIDS = cb.build_chair()


# ---------------------------------------------------------------- figures SVG
class Fig:
    """Figura en coordenades de model (mm reals) -> SVG en mm de paper."""

    def __init__(self, scale, pad=2.0):
        self.s = scale
        self.pad = pad
        self.items = []          # (tipus, dades)
        self.pts = []

    def _add(self, kind, pts, **kw):
        self.items.append((kind, pts, kw))
        self.pts.extend(pts)

    def line(self, p, q, color=INK, w=0.3, dash=None, op=1):
        self._add("line", [tuple(p), tuple(q)], color=color, w=w, dash=dash, op=op)

    def poly(self, pts, fill, op=1, stroke=None, w=0.2):
        self._add("poly", [tuple(p) for p in pts], fill=fill, op=op, stroke=stroke, w=w)

    def text(self, p, s, size=2.2, color=MUTED, anchor="middle", rot=0, weight=400,
             family="Inter"):
        self._add("text", [tuple(p)], s=s, size=size, color=color, anchor=anchor,
                  rot=rot, weight=weight, family=family, track=False)

    def segs(self, segs, wood=INK, lam=ACCENT, w=0.3, colors=None):
        for p, q, k in segs:
            c = colors.get(k, wood) if colors else (lam if k == "lamina" else wood)
            self.line(p, q, color=c, w=w)

    # cota lineal; p1,p2 punts mesurats; off = distància (model) de la línia de cota
    def hdim(self, x0, x1, y, yb, txt=None):
        tick = 1.0 / self.s
        for x in (x0, x1):
            self.line((x, y + math.copysign(1.0 / self.s, yb - y)), (x, yb + math.copysign(1.2 / self.s, yb - y)),
                      color=MUTED, w=0.12)
            self.line((x - tick * .5, yb - tick * .5), (x + tick * .5, yb + tick * .5),
                      color=MUTED, w=0.25)
        self.line((x0 - 1 / self.s, yb), (x1 + 1 / self.s, yb), color=MUTED, w=0.12)
        self.text(((x0 + x1) / 2, yb + 0.8 / self.s), txt or f"{x1 - x0:g}", size=2.0)

    def vdim(self, y0, y1, x, xb, txt=None):
        tick = 1.0 / self.s
        for y in (y0, y1):
            self.line((x + math.copysign(1.0 / self.s, xb - x), y), (xb + math.copysign(1.2 / self.s, xb - x), y),
                      color=MUTED, w=0.12)
            self.line((xb - tick * .5, y - tick * .5), (xb + tick * .5, y + tick * .5),
                      color=MUTED, w=0.25)
        self.line((xb, y0 - 1 / self.s), (xb, y1 + 1 / self.s), color=MUTED, w=0.12)
        self.text((xb - 0.8 / self.s, (y0 + y1) / 2), txt or f"{y1 - y0:g}", size=2.0, rot=-90)

    def svg(self, extra_bbox=None):
        P = np.array(self.pts + (extra_bbox or []))
        x0, y0 = P.min(axis=0)
        x1, y1 = P.max(axis=0)
        s, pad = self.s, self.pad
        Wm = (x1 - x0) * s + 2 * pad
        Hm = (y1 - y0) * s + 2 * pad

        def tp(p):
            return ((p[0] - x0) * s + pad, (y1 - p[1]) * s + pad)

        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wm:.2f}mm" height="{Hm:.2f}mm" '
               f'viewBox="0 0 {Wm:.3f} {Hm:.3f}" overflow="visible">']
        for kind, pts, kw in self.items:
            if kind == "line":
                (a, b), (c, d) = tp(pts[0]), tp(pts[1])
                dash = f' stroke-dasharray="{kw["dash"]}"' if kw["dash"] else ""
                out.append(f'<line x1="{a:.3f}" y1="{b:.3f}" x2="{c:.3f}" y2="{d:.3f}" '
                           f'stroke="{kw["color"]}" stroke-width="{kw["w"]}" stroke-opacity="{kw["op"]}" '
                           f'stroke-linecap="round"{dash}/>')
            elif kind == "poly":
                pp = " ".join(f"{a:.3f},{b:.3f}" for a, b in map(tp, pts))
                st = f' stroke="{kw["stroke"]}" stroke-width="{kw["w"]}"' if kw["stroke"] else ""
                out.append(f'<polygon points="{pp}" fill="{kw["fill"]}" fill-opacity="{kw["op"]}"{st}/>')
            else:
                a, b = tp(pts[0])
                rot = f' transform="rotate({kw["rot"]} {a:.3f} {b:.3f})"' if kw["rot"] else ""
                out.append(f'<text x="{a:.3f}" y="{b:.3f}" font-family="{kw["family"]}" '
                           f'font-size="{kw["size"]}" font-weight="{kw["weight"]}" fill="{kw["color"]}" '
                           f'text-anchor="{kw["anchor"]}"{rot}>{kw["s"]}</text>')
        out.append("</svg>")
        return "\n".join(out), Wm, Hm


def vis(view_dir, proj, solids=SOLIDS):
    return cb.visible_segments(solids, view_dir, proj, step=1.5)


ALC = vis((0, -1, 0), cb.proj_alcat)
PER = vis((-1, 0, 0), cb.proj_perfil)
PLA = vis((0, 0, 1), cb.proj_planta)


def iso_proj(p):  # projecció isomètrica real (reduïda)
    return (p @ cb._r, p @ cb._u)


# ---------------------------------------------------------------- 04 vistes
def fig_vistes():
    s = 0.1
    f = Fig(s)
    gap = 170                        # separació alçat-perfil (model)
    ox_p = W + gap                   # origen perfil
    oy_pl = -(D + 230)               # origen planta
    sh = lambda segs, dx, dy: [((p[0] + dx, p[1] + dy), (q[0] + dx, q[1] + dy), k) for p, q, k in segs]
    f.segs(ALC); f.segs(sh(PER, ox_p, 0)); f.segs(sh(PLA, 0, oy_pl))
    # terra i eixos
    f.line((-40, 0), (W + 40, 0), w=0.35)
    f.line((ox_p - 40, 0), (ox_p + D + 40, 0), w=0.35)
    for y0, y1 in ((-30, H + 30), (oy_pl - 30, oy_pl + D + 30)):
        f.line((W / 2, y0), (W / 2, y1), color=MUTED, w=0.12, dash="3 1 0.6 1")
    # alçat
    f.hdim(0, W, 0, -105)
    for a, b in ((0, t), (t, t + M), (t + M, W - t - M), (W - t - M, W - t), (W - t, W)):
        f.hdim(a, b, 0, -50, txt="" if b - a < 30 else None)
    f.text((t / 2, -38), "24", size=1.6); f.text((W - t / 2, -38), "24", size=1.6)
    f.vdim(0, H, 0, -150)
    for a, b in ((0, cb.Z_FLEG), (cb.Z_FLEG, cb.Z_ARM), (cb.Z_ARM, cb.Z_ARM + t),
                 (cb.Z_ARM + t, cb.Z_HOLD), (cb.Z_HOLD, H)):
        f.vdim(a, b, 0, -75, txt="" if b - a < 30 else None)
    f.text((-60, cb.Z_ARM + t / 2), "24", size=1.6, rot=-90)
    # perfil (davant a la dreta)
    o = ox_p
    hy = [0, t, D - cb.Y_REAR - t, D - cb.Y_REAR, D - M, D]
    f.hdim(o, o + D, 0, -105)
    for a, b in zip(hy, hy[1:]):
        f.hdim(o + a, o + b, 0, -50, txt="" if b - a < 30 else None)
    f.text((o + t / 2, -38), "24", size=1.6); f.text((o + D - cb.Y_REAR - t / 2, -38), "24", size=1.6)
    f.hdim(o + t, o + D - cb.Y_ARM, cb.Z_ARM + t, cb.Z_ARM + t + 60)
    f.hdim(o + D - cb.Y_ARM, o + D, cb.Z_ARM + t, cb.Z_ARM + t + 60)
    f.vdim(0, cb.Z_RRAIL + M, o + D, o + D + 55)
    f.vdim(0, cb.Z_FRAIL + M, o + D, o + D + 105)
    f.vdim(0, cb.Z_ARM + t, o + D, o + D + 155)
    f.vdim(cb.Z_STRAP_U, cb.Z_STRAP_U + 2 * M, o, o - 70)
    f.vdim(cb.Z_STRAP_L, cb.Z_STRAP_L + 2 * M, o, o - 70)
    f.vdim(cb.Z_RAIL, cb.Z_RAIL + M, o, o - 70)
    # planta
    f.hdim(0, W, oy_pl + D, oy_pl + D + 70)
    f.vdim(oy_pl, oy_pl + D, 0, -90)
    vy = [0, M, cb.Y_ARM, cb.Y_REAR, cb.Y_REAR + t, D - 2 * t, D - t, D]
    for a, b in zip(vy, vy[1:]):
        f.vdim(oy_pl + a, oy_pl + b, W, W + 60, txt="" if b - a < 30 else None)
    # rètols
    lab = dict(size=2.4, color=INK, weight=600)
    f.text((W / 2, H + 70), "ALÇAT", **lab)
    f.text((o + D / 2, H + 70), "PERFIL ESQUERRE", **lab)
    f.text((W / 2, oy_pl - 75), "PLANTA", **lab)
    return f.svg()


# ---------------------------------------------------------------- 02 proporcions
def grid(f, x0, y0, nx, ny, step):
    for i in range(nx + 1):
        f.line((x0 + i * step, y0), (x0 + i * step, y0 + ny * step), color=ACCENT, w=0.08, op=0.35)
    for j in range(ny + 1):
        f.line((x0, y0 + j * step), (x0 + nx * step, y0 + j * step), color=ACCENT, w=0.08, op=0.35)


def fig_prop_alcat():
    f = Fig(0.045)
    grid(f, 0, 0, 12, 20, M)
    f.segs(ALC, w=0.22, lam=INK)
    # quadrat 12M + rectangle 12x8
    sq = [(0, 0), (W, 0), (W, W), (0, W)]
    f.poly(sq, ACCENT, op=0.10, stroke=ACCENT, w=0.35)
    f.poly([(0, W), (W, W), (W, H), (0, H)], "#7fa6d6", op=0.10, stroke="#7fa6d6", w=0.35)
    f.line((0, 0), (W, W), color=ACCENT, w=0.2, dash="1 0.8")
    f.line((W, 0), (0, W), color=ACCENT, w=0.2, dash="1 0.8")
    f.text((W + 25, W / 2), "12M", size=2.0, color=ACCENT, anchor="start", weight=600)
    f.text((W + 25, (W + H) / 2), "8M", size=2.0, color="#7fa6d6", anchor="start", weight=600)
    f.text((W / 2, -45), "12M", size=2.0, color=ACCENT, weight=600)
    f.text((-25, H / 2), "20M", size=2.0, color=INK, rot=-90, weight=600)
    return f.svg()


def fig_prop_perfil():
    f = Fig(0.045)
    grid(f, 0, 0, 12, 20, M)
    f.segs(PER, w=0.22, lam=INK)
    levels = [(cb.Z_RAIL, "7M"), (cb.Z_FRAIL + M, "8,5M"), (cb.Z_ARM + t, "13M"),
              (cb.Z_STRAP_U, "16M"), (H, "20M")]
    for z, lab in levels:
        f.line((-10, z), (D + 30, z), color=ACCENT, w=0.18)
        f.text((D + 40, z - 6), lab, size=1.8, color=ACCENT, anchor="start", weight=600)
    return f.svg()


def fig_prop_planta():
    f = Fig(0.045)
    grid(f, 0, 0, 12, 12, M)
    f.segs(PLA, w=0.22, lam=INK)
    f.line((0, 0), (W, D), color=ACCENT, w=0.2, dash="1 0.8")
    f.line((W, 0), (0, D), color=ACCENT, w=0.2, dash="1 0.8")
    f.poly([(0, 0), (W, 0), (W, D), (0, D)], ACCENT, op=0.08, stroke=ACCENT, w=0.35)
    f.text((W / 2, -45), "12M × 12M", size=2.0, color=ACCENT, weight=600)
    return f.svg()


# ---------------------------------------------------------------- 01 mòdul
def fig_llisto():
    """Secció del llistó tipus a 1:2 sobre retícula de ½M."""
    f = Fig(0.5)
    for i in range(3):
        f.line((i * t, 0), (i * t, M), color=ACCENT, w=0.1, op=0.5)
    for j in range(3):
        f.line((0, j * t), (2 * t, j * t), color=ACCENT, w=0.1, op=0.5)
    f.poly([(0, 0), (t, 0), (t, M), (0, M)], INK, op=0.9)
    f.hdim(0, t, 0, -9, txt="24")
    f.vdim(0, M, 0, -9, txt="48")
    f.text((t + 4, M - 4), "M", size=2.4, color=ACCENT, anchor="start", weight=600)
    f.text((t + 4, t / 2 - 2), "½M", size=2.4, color=ACCENT, anchor="start", weight=600)
    return f.svg()


def inventory():
    """Llargades dels llistons (múltiples de ½M)."""
    rows = {}
    for s in SOLIDS:
        if s.kind != "wood":
            continue
        name = s.name.rsplit(" ", 1)[0] if s.name[-2:] in (" E", " D") else s.name
        L = float((s.v.max(axis=0) - s.v.min(axis=0)).max())
        rows.setdefault(name, [L, 0])[1] += 1
    return sorted(((n, L, c) for n, (L, c) in rows.items()), key=lambda r: -r[1])


def fig_inventari():
    f = Fig(0.1)
    rows = inventory()
    y = 0
    for name, L, c in rows:
        f.poly([(0, y), (L, y), (L, y + 24), (0, y + 24)], INK, op=0.85)
        for k in range(1, int(L // t)):
            f.line((k * t, y), (k * t, y + 24), color=BG0, w=0.08, op=0.6)
        f.text((L + 12, y + 4), f"{c}× {name}", size=1.9, color=INK, anchor="start")
        f.text((-12, y + 4), f"{L / M:g}M", size=1.9, color=ACCENT, anchor="end", weight=600)
        y -= 46
    return f.svg(extra_bbox=[(1000, 0)]), sum(c for *_, c in rows)


# ---------------------------------------------------------------- 03 composició
def fig_volum():
    f = Fig(0.032)
    segs = vis(cb.ISO_DIR, iso_proj)
    f.segs(segs, wood=MUTED, lam=MUTED, w=0.15)
    def boxw(x0, x1, y0, y1, z0, z1, col, fill_op):
        V = np.array([(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)], float)
        E = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
        P = [iso_proj(v) for v in V]
        for a, b in E:
            f.line(P[a], P[b], color=col, w=0.3)
        # cares visibles (davant y0, dreta x1, dalt z1)
        for face in ((0, 1, 5, 4), (1, 3, 7, 5), (4, 5, 7, 6)):
            f.poly([P[i] for i in face], col, op=fill_op)
    boxw(0, W, 0, D, 0, W, ACCENT, 0.10)
    boxw(t, W - t, D - 2 * t, D, W, H, "#7fa6d6", 0.18)
    return f.svg()


def axis_of(s):
    ext = s.v.max(axis=0) - s.v.min(axis=0)
    return "xyz"[int(np.argmax(ext))]


def fig_direccions():
    f = Fig(0.032)
    wood = [s for s in SOLIDS if s.kind == "wood"]
    saved = [s.kind for s in wood]
    for s in wood:
        s.kind = axis_of(s)
    segs = vis(cb.ISO_DIR, iso_proj, wood)
    for s, k in zip(wood, saved):
        s.kind = k
    f.segs(segs, colors=AX, w=0.3)
    return f.svg()


def fig_plans():
    f = Fig(0.032)
    segs = vis(cb.ISO_DIR, iso_proj)
    f.segs(segs, wood=MUTED, lam=ACCENT, w=0.18)
    for s in SOLIDS:
        if s.kind != "lamina":
            continue
        # cara més gran visible: projecta tots els vèrtexs i n'agafa l'envolupant convexa
        P = np.array([iso_proj(v) for v in s.v])
        hull = convex_hull(P)
        f.poly(hull, ACCENT, op=0.75)
    return f.svg()


def convex_hull(P):
    pts = sorted(map(tuple, P))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


# ---------------------------------------------------------------- HTML
def build():
    vistes, vw, vh = fig_vistes()
    pa, paw, pah = fig_prop_alcat()
    pp, ppw, pph = fig_prop_perfil()
    pl, plw, plh = fig_prop_planta()
    ll, llw, llh = fig_llisto()
    (inv, invw, invh), n_llistons = fig_inventari()
    v1, *_ = fig_volum()
    v2, *_ = fig_direccions()
    v3, *_ = fig_plans()
    top02 = 62 + 50 + invh + 12

    html = f"""<!doctype html>
<html lang="ca"><head><meta charset="utf-8">
<title>EXAR L1 · Slatted Chair TI 1A</title>
<style>
@font-face {{ font-family: Anton; src: url(assets/anton-latin-400-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 300; src: url(assets/inter-latin-300-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 400; src: url(assets/inter-latin-400-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 500; src: url(assets/inter-latin-500-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url(assets/inter-latin-600-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url(assets/inter-latin-700-normal.woff2); }}
@page {{ size: 420mm 297mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 420mm; height: 297mm; }}
body {{
  position: relative; overflow: hidden;
  font-family: Inter; font-weight: 300; color: {INK};
  background: radial-gradient(120% 90% at 85% 25%, {BG1} 0%, {BG0} 70%);
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
.abs {{ position: absolute; }}
h1 {{ font-family: Anton; font-weight: 400; color: {ACCENT}; font-size: 30mm; line-height: .9;
      letter-spacing: .4mm; }}
.sub {{ font-family: Inter; font-weight: 500; font-size: 4.6mm; letter-spacing: .2mm; margin-top: 2.5mm; }}
.sub span {{ color: {MUTED}; font-weight: 300; }}
.kicker {{ font-weight: 600; font-size: 2.9mm; letter-spacing: 1.1mm; color: {MUTED}; margin-bottom: 3mm; }}
p {{ font-size: 3.05mm; line-height: 1.42; text-align: left; }}
p.small {{ font-size: 2.6mm; color: {MUTED}; }}
b {{ font-weight: 600; color: {INK}; }}
.acc {{ color: {ACCENT}; font-weight: 600; }}
.sec {{ display: flex; align-items: baseline; gap: 2.5mm; margin-bottom: 2mm; }}
.sec .n {{ font-family: Anton; color: {ACCENT}; font-size: 7mm; line-height: 1; }}
.sec .t {{ font-weight: 600; font-size: 4.2mm; }}
.sec .m {{ font-size: 2.5mm; color: {MUTED}; font-weight: 400; margin-left: auto; }}
.rule {{ height: .25mm; background: {INK}; opacity: .25; }}
.info {{ font-size: 2.9mm; line-height: 1.5; }}
.info b {{ font-weight: 600; }}
.cap {{ font-size: 2.3mm; color: {MUTED}; margin-top: 1mm; }}
.row {{ display: flex; align-items: flex-end; justify-content: space-between; }}
.legend span {{ display: inline-flex; align-items: center; gap: 1.2mm; margin-right: 3mm;
                font-size: 2.3mm; color: {MUTED}; }}
.legend i {{ width: 5mm; height: .7mm; display: inline-block; }}
</style></head><body>

<!-- ============ CAPÇALERA ============ -->
<div class="abs" style="left:16mm; top:13mm;">
  <div class="kicker">EXAR · L1 — APLICACIÓ A LA COMPOSICIÓ I PROPORCIÓ</div>
  <h1>SLATTED CHAIR</h1>
  <div class="sub">TI 1A &nbsp;·&nbsp; Marcel Breuer <span>&nbsp;·&nbsp; Bauhaus Weimar, 1922–24</span></div>
</div>
<div class="abs" style="left:194mm; top:21mm; width:112mm;">
  <p>Dissenyada per Marcel Breuer quan encara era estudiant al taller de fusteria del
  Bauhaus, la cadira trasllada a l'espai la gramàtica del <b>De Stijl</b>: una xarxa lleugera
  de <b>llistons ortogonals</b> que sostenen làmines suspeses. A la segona versió
  (1924) tota l'estructura es construeix amb un <b>únic llistó estandarditzat</b> —només en
  canvia la llargada—, una decisió que ordena la forma i n'abarateix la producció.</p>
</div>
<div class="abs" style="left:322mm; top:14mm; width:84mm;">
  <img src="assets/logo_upc_epsevg.png" style="width:62mm; display:block; margin-bottom:4mm;">
  <div class="info">
    <b>Alumne:</b> {ALUMNE}<br>
    <b>Professor:</b> {PROFESSOR}<br>
    <b>Grup:</b> {GRUP} &nbsp;·&nbsp; <b>Assignatura:</b> EXAR<br>
    <b>Data:</b> {DATA}
  </div>
</div>
<div class="abs rule" style="left:16mm; right:16mm; top:56mm;"></div>

<!-- ============ COL A: MÒDUL I PROPORCIONS ============ -->
<div class="abs" style="left:16mm; top:62mm; width:98mm;">
  <div class="sec"><span class="n">01</span><span class="t">Mòdul base</span></div>
  <div class="row" style="align-items:flex-start; gap:4mm;">
    <div style="flex:1">
      <p><span class="acc">M = 48 mm</span>, l'amplada del llistó tipus. La secció
      24 × 48 (<b>½M × M</b>, proporció 1:2) es repeteix a totes les peces: només
      canvia la llargada, sempre múltiple de ½M.</p>
    </div>
    <div style="text-align:center">{ll}<div class="cap">Secció · E 1:2</div></div>
  </div>
  <div class="cap" style="margin:3mm 0 1mm">Llargades dels llistons (en M)</div>
  <div>{inv}</div>
</div>

<div class="abs" style="left:16mm; top:{top02}mm; width:98mm;">
  <div class="sec"><span class="n">02</span><span class="t">Sistema de proporcions</span></div>
  <p>Planta <b>quadrada</b> (12M × 12M) i alçat <b>12M × 20M = 3:5</b>, termes de la sèrie de
  Fibonacci que tendeix a la secció àuria (5/3 = 1,67, prop de 1,618). L'alçada es divideix
  en un <span class="acc">quadrat de 12M</span> —cos del seient, fins a l'arrencada dels braços— i
  un rectangle 12M × 8M —el respatller—: <b>3:2</b>.</p>
  <div class="row" style="margin-top:3mm; align-items:flex-end;">
    <div style="text-align:center">{pa}<div class="cap">Alçat · 3:5</div></div>
    <div style="text-align:center">{pp}<div class="cap">Perfil · nivells</div></div>
    <div style="text-align:center">{pl}<div class="cap">Planta · quadrat</div></div>
  </div>
  <p class="small" style="margin-top:2.5mm;">Retícula de mòduls M = 48 mm (esquemes sense escala). Tots els
  nivells i llargades cauen sobre la retícula de ½M.</p>
</div>

<!-- ============ COL B: VISTES ============ -->
<div class="abs" style="left:124mm; top:62mm; width:178mm;">
  <div class="sec"><span class="n">04</span><span class="t">Vistes dièdriques acotades</span>
    <span class="m">E 1:10 · cotes en mm · sistema europeu</span></div>
  <div style="margin-top:3mm; display:flex; justify-content:center;">{vistes}</div>
</div>

<!-- ============ COL C: ISOMÈTRICA + COMPOSICIÓ ============ -->
<div class="abs" style="left:306mm; top:62mm; width:100mm; height:140mm;">
  <img src="assets/render_iso.png" style="position:absolute; right:-4mm; top:8mm; height:128mm;">
  <div class="sec" style="position:relative;"><span class="n">05</span><span class="t">Perspectiva isomètrica</span></div>
  <div class="cap" style="position:absolute; left:0; top:12mm; width:31mm; line-height:1.4;">Model 3D a partir de les
  vistes acotades. La làmina inferior del respatller s'ancora a les potes posteriors i la
  superior als pals: el respatller s'inclina sense inclinar cap llistó.</div>
</div>

<div class="abs" style="left:310mm; top:204mm; width:96mm;">
  <div class="sec"><span class="n">03</span><span class="t">Composició volumètrica</span></div>
  <p style="font-size:2.75mm">Un <span class="acc">cub de 12M</span> conté potes, seient i braços; en
  sobresurt el pla del respatller (8M). La forma s'articula amb <b>línies</b> —llistons en les
  tres direccions, que es superposen sense tallar-se— i <b>plans</b> —tres làmines suspeses.</p>
  <div class="row" style="margin-top:2mm">
    <div style="text-align:center">{v1}<div class="cap">Volum envolupant</div></div>
    <div style="text-align:center">{v2}<div class="cap">Línies X · Y · Z</div></div>
    <div style="text-align:center">{v3}<div class="cap">Plans suspesos</div></div>
  </div>
  <div class="legend" style="margin-top:1.5mm; text-align:center">
    <span><i style="background:{AX['z']}"></i>Z verticals</span>
    <span><i style="background:{AX['y']}"></i>Y longitudinals</span>
    <span><i style="background:{AX['x']}"></i>X transversals</span>
    <span><i style="background:{ACCENT}; height:1.6mm"></i>làmines</span>
  </div>
</div>

</body></html>"""
    out = HERE / "lamina.html"
    out.write_text(html, encoding="utf-8")
    return out


def export(html):
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1588, height: 1123 }} }});
  await p.goto('file://{html}');
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: '{HERE}/EXAR_L1_Addami_Ech_Chaouy_Ziad.pdf', width: '420mm', height: '297mm',
                printBackground: true }});
  await p.screenshot({{ path: '{HERE}/preview.png' }});
  await b.close();
}})();
"""
    subprocess.run(["node", "-e", js], check=True,
                   env={**__import__("os").environ,
                        "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True,
                                                    text=True).stdout.strip()})


if __name__ == "__main__":
    export(build())
