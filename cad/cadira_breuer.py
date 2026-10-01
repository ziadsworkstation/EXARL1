"""
EXAR - L1 Composició i proporció
Cadira Slatted Chair "TI 1A" (Marcel Breuer, 1922-24)

Genera el model 3D (sòlids convexos) i, a partir d'ell, les vistes dièdriques
(sistema europeu) acotades i la perspectiva isomètrica en un fitxer DXF.

Unitats: mm.  Làmina A3 dibuixada a escala 1:10 a l'espai model
(marc de 4200 x 2970 unitats = 420 x 297 mm en imprimir a 1:10).

Eixos del model:  X = amplada (esquerra -> dreta)
                  Y = profunditat (0 = davant, creix cap enrere)
                  Z = alçada (0 = terra)
"""

import math
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment

# --------------------------------------------------------------------------
# Mòdul i proporcions
# --------------------------------------------------------------------------
M = 40                    # mòdul base = secció dels llistons (40 x 40 mm)
W = 14 * M                # amplada total      560
D = 14 * M                # profunditat total  560
H = 24 * M                # alçada total       960

Z_RAIL = 6 * M            # alçada inferior del travesser lateral  240
Z_SEAT_F = 11 * M         # alçada seient davant (pota davantera)  440
Z_SEAT_R = 9 * M          # alçada seient darrere                  360
Z_ARM = 16 * M            # alçada pota posterior / base del braç  640
Y_REAR = 10 * M           # posició pota posterior                 400
Y_ARM = 2 * M             # inici del braç (voladís)                80
T = 4                     # gruix de les teles / cinghes


# --------------------------------------------------------------------------
# Geometria: sòlids convexos
# --------------------------------------------------------------------------
class Solid:
    """Poliedre convex definit per vèrtexs i cares (llistes d'índexs)."""

    def __init__(self, name, verts, faces, kind="wood"):
        self.name = name
        self.kind = kind
        self.v = np.array(verts, dtype=float)
        self.faces = faces
        self.planes = []          # (normal exterior, d) amb n·p <= d a l'interior
        c = self.v.mean(axis=0)
        for f in faces:
            p0, p1, p2 = self.v[f[0]], self.v[f[1]], self.v[f[2]]
            n = np.cross(p1 - p0, p2 - p0)
            n /= np.linalg.norm(n)
            d = n @ p0
            if n @ c > d:
                n, d = -n, -d
            self.planes.append((n, d))
        edges = set()
        for f in faces:
            for i in range(len(f)):
                a, b = f[i], f[(i + 1) % len(f)]
                edges.add((min(a, b), max(a, b)))
        self.edges = sorted(edges)

    def ray_hits(self, p, v, eps=1e-6):
        """True si el raig p + t·v (t>0) travessa l'interior del sòlid."""
        t0, t1 = -math.inf, math.inf
        for n, d in self.planes:
            nv = n @ v
            dist = d - n @ p
            if abs(nv) < 1e-12:
                if dist <= eps:      # fora (o sobre) del semiespai
                    return False
                continue
            t = dist / nv
            if nv > 0:
                t1 = min(t1, t)
            else:
                t0 = max(t0, t)
            if t0 >= t1 - eps:
                return False
        return t1 > eps and (t1 - max(t0, 0.0)) > eps


BOX_FACES = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
             [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]


def box(name, x0, x1, y0, y1, z0, z1, kind="wood"):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return Solid(name, v, BOX_FACES, kind)


def prism_x(name, x0, x1, quad_yz, kind="fabric"):
    """Prisma extruït en X a partir d'un quadrilàter convex al pla YZ."""
    v = [(x0, y, z) for y, z in quad_yz] + [(x1, y, z) for y, z in quad_yz]
    return Solid(name, v, BOX_FACES, kind)


def build_chair():
    s = []
    for side, (xa, xb) in (("E", (0, M)), ("D", (W - M, W))):
        s.append(box(f"pota davantera {side}", xa, xb, 0, M, 0, Z_SEAT_F))
        s.append(box(f"pota posterior {side}", xa, xb, Y_REAR, Y_REAR + M, 0, Z_ARM))
        s.append(box(f"travesser lateral {side}", xa, xb, 0, D, Z_RAIL, Z_RAIL + M))
        s.append(box(f"pal respatller {side}", xa, xb, D - M, D, Z_RAIL, H))
        s.append(box(f"braç {side}", xa, xb, Y_ARM, D, Z_ARM, Z_ARM + M))
    # travessers transversals
    s.append(box("travesser seient davant", M, W - M, 0, M, Z_SEAT_F - M, Z_SEAT_F))
    s.append(box("travesser seient darrere", M, W - M, Y_REAR, Y_REAR + M,
                 Z_SEAT_R - M, Z_SEAT_R))
    s.append(box("travesser posterior inferior", M, W - M, D - M, D,
                 Z_RAIL, Z_RAIL + M))
    # tela del seient (inclinada del travesser davanter al posterior)
    s.append(prism_x("tela seient", M, W - M,
                     [(0, Z_SEAT_F), (Y_REAR + M, Z_SEAT_R),
                      (Y_REAR + M, Z_SEAT_R + T), (0, Z_SEAT_F + T)]))
    # cinghes del respatller
    s.append(box("cinga respatller inferior", M, W - M, Y_REAR - T, Y_REAR,
                 12 * M, 15 * M, "fabric"))
    s.append(box("cinga respatller superior", M, W - M, D - M - T, D - M,
                 21 * M, 23 * M + M // 2, "fabric"))
    return s


# --------------------------------------------------------------------------
# Eliminació de línies ocultes per mostreig
# --------------------------------------------------------------------------
def visible_segments(solids, view_dir, project, step=2.0):
    """Retorna segments 2D visibles. view_dir: vector cap a l'observador."""
    v = np.array(view_dir, dtype=float)
    v /= np.linalg.norm(v)
    out = []
    for s in solids:
        for a, b in s.edges:
            pa, pb = s.v[a], s.v[b]
            e = pb - pa
            L = np.linalg.norm(e)
            if L < 1e-9 or np.linalg.norm(np.cross(e / L, v)) < 1e-6:
                continue                     # aresta paral·lela a la visual
            n = max(2, int(L / step) + 1)
            ts = np.linspace(0, 1, n)
            vis = []
            for t in ts:
                p = pa + t * e
                hidden = any(o.ray_hits(p, v) for o in solids)
                vis.append(not hidden)
            # agrupar trams visibles
            i = 0
            while i < n:
                if vis[i]:
                    j = i
                    while j + 1 < n and vis[j + 1]:
                        j += 1
                    if j > i:
                        q0, q1 = pa + ts[i] * e, pa + ts[j] * e
                        out.append((project(q0), project(q1), s.kind))
                    i = j + 1
                else:
                    i += 1
    return dedupe(out)


def dedupe(segs, tol=0.05):
    seen, res = set(), []
    for p, q, k in segs:
        key = tuple(np.round(sorted([tuple(p), tuple(q)]), 1).ravel())
        if key in seen:
            continue
        seen.add(key)
        if math.dist(p, q) > tol:
            res.append((p, q, k))
    return res


# Projeccions (sistema europeu)
def proj_alcat(p):        # vista frontal, observador a -Y
    return (p[0], p[2])


def proj_perfil(p):       # perfil esquerre, observador a -X, situat a la dreta
    return (D - p[1], p[2])


def proj_planta(p):       # planta, observador a +Z, situada sota l'alçat
    return (p[0], p[1])


ISO_DIR = np.array([1.0, -1.0, 1.0])     # observador davant-dreta-dalt
_f = -ISO_DIR / np.linalg.norm(ISO_DIR)
_r = np.cross(_f, [0, 0, 1.0]); _r /= np.linalg.norm(_r)
_u = np.cross(_r, _f)
ISO_K = 1 / math.sqrt(2 / 3)                # dibuix isomètric (coef. 1)


def proj_iso(p):
    return (ISO_K * (p @ _r), ISO_K * (p @ _u))


# --------------------------------------------------------------------------
# DXF
# --------------------------------------------------------------------------
SCALE = 10                 # 1:10  ->  1 mm de paper = 10 unitats
TXT = 2.5 * SCALE


def setup_doc():
    doc = ezdxf.new("R2010", setup=True, units=4)   # 4 = mm
    doc.layers.add("MARC", color=7, lineweight=70)
    doc.layers.add("CAIXETI", color=7, lineweight=35)
    doc.layers.add("FUSTA", color=7, lineweight=50)
    doc.layers.add("TELA", color=8, lineweight=25)
    doc.layers.add("COTES", color=1, lineweight=18)
    doc.layers.add("EIXOS", color=3, lineweight=13, linetype="CENTER")
    doc.layers.add("TEXT", color=7, lineweight=25)
    doc.styles.add("EXAR", font="DejaVuSans.ttf")
    ds = doc.dimstyles.new("EXAR_1-10")
    ds.dxf.dimtxsty = "EXAR"
    ds.dxf.dimscale = SCALE
    ds.dxf.dimtxt = 2.0
    ds.dxf.dimasz = 1.8
    ds.dxf.dimexe = 1.2
    ds.dxf.dimexo = 1.0
    ds.dxf.dimgap = 0.8
    ds.dxf.dimdec = 0
    ds.dxf.dimtad = 1
    ds.dxf.dimtih = 0
    ds.dxf.dimtoh = 0
    ds.dxf.dimclrd = 1
    ds.dxf.dimclre = 1
    ds.dxf.dimclrt = 7
    ds.dxf.dimblk = "ARCHTICK"
    ds.dxf.dimtsz = 0
    return doc


def draw_segments(msp, segs, origin):
    ox, oy = origin
    for p, q, kind in segs:
        msp.add_line((p[0] + ox, p[1] + oy), (q[0] + ox, q[1] + oy),
                     dxfattribs={"layer": "FUSTA" if kind == "wood" else "TELA"})


def text(msp, s, x, y, h=TXT, align=TextEntityAlignment.BOTTOM_LEFT, layer="TEXT"):
    t = msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "EXAR"})
    t.set_placement((x, y), align=align)
    return t


def hdim(msp, x0, x1, y, base, origin):
    ox, oy = origin
    msp.add_linear_dim(base=(ox + x0, oy + base), p1=(ox + x0, oy + y),
                       p2=(ox + x1, oy + y), dimstyle="EXAR_1-10",
                       dxfattribs={"layer": "COTES"}).render()


def vdim(msp, y0, y1, x, base, origin):
    ox, oy = origin
    msp.add_linear_dim(base=(ox + base, oy + y0), p1=(ox + x, oy + y0),
                       p2=(ox + x, oy + y1), angle=90, dimstyle="EXAR_1-10",
                       dxfattribs={"layer": "COTES"}).render()


def label(msp, s, x, y):
    text(msp, s, x, y, h=3.0 * SCALE, align=TextEntityAlignment.BOTTOM_CENTER)


def main(path_dxf):
    solids = build_chair()
    doc = setup_doc()
    msp = doc.modelspace()

    # ---- marc A3 (420 x 297 mm a 1:10) ----
    FW, FH = 420 * SCALE, 297 * SCALE
    mg = 10 * SCALE
    msp.add_lwpolyline([(0, 0), (FW, 0), (FW, FH), (0, FH)], close=True,
                       dxfattribs={"layer": "CAIXETI", "lineweight": 13})
    msp.add_lwpolyline([(mg, mg), (FW - mg, mg), (FW - mg, FH - mg), (mg, FH - mg)],
                       close=True, dxfattribs={"layer": "MARC"})

    # ---- capçalera (caixetí de disseny lliure) ----
    hb = 28 * SCALE
    y_h = FH - mg - hb
    msp.add_line((mg, y_h), (FW - mg, y_h), dxfattribs={"layer": "CAIXETI"})
    text(msp, "L1 - APLICACIÓ A LA COMPOSICIÓ I PROPORCIÓ", mg + 60, y_h + 170,
         h=4 * SCALE)
    text(msp, "SLATTED CHAIR  \"TI 1A\"  ·  Marcel Breuer, 1922-24", mg + 60,
         y_h + 70, h=6 * SCALE)
    info = ["Alumne: COGNOMS, NOM", "Professor: ______________",
            "Assignatura: EXAR", "Data: 05/10/2026"]
    for i, s in enumerate(info):
        text(msp, s, FW - mg - 1100, y_h + 200 - i * 50, h=3 * SCALE)
    text(msp, "Escala 1:10  ·  Cotes en mm  ·  Sistema europeu", FW - mg - 1260,
         y_h - 60, h=2.5 * SCALE)
    msp.add_lwpolyline([(FW - mg - 1260, y_h + 30), (FW - mg - 1160, y_h + 30),
                        (FW - mg - 1160, y_h + 230), (FW - mg - 1260, y_h + 230)],
                       close=True, dxfattribs={"layer": "CAIXETI"})
    text(msp, "LOGO", FW - mg - 1210, y_h + 130, h=2 * SCALE,
         align=TextEntityAlignment.MIDDLE_CENTER)

    # ---- vistes dièdriques ----
    O_ALC = (600, 1420)                    # alçat
    O_PER = (O_ALC[0] + W + 500, O_ALC[1])  # perfil esquerre (a la dreta)
    O_PLA = (O_ALC[0], O_ALC[1] - D - 480)  # planta (a sota)

    views = [
        ("ALÇAT", O_ALC, proj_alcat, (0, -1, 0)),
        ("PERFIL ESQUERRE", O_PER, proj_perfil, (-1, 0, 0)),
        ("PLANTA", O_PLA, proj_planta, (0, 0, 1)),
    ]
    for name, org, prj, vd in views:
        draw_segments(msp, visible_segments(solids, vd, prj), org)

    # línies de terra
    for org, w in ((O_ALC, W), (O_PER, D)):
        msp.add_line((org[0] - 60, org[1]), (org[0] + w + 60, org[1]),
                     dxfattribs={"layer": "FUSTA"})
    # eixos de simetria
    msp.add_line((O_ALC[0] + W / 2, O_ALC[1] - 40), (O_ALC[0] + W / 2, O_ALC[1] + H + 40),
                 dxfattribs={"layer": "EIXOS"})
    msp.add_line((O_PLA[0] + W / 2, O_PLA[1] - 40), (O_PLA[0] + W / 2, O_PLA[1] + D + 40),
                 dxfattribs={"layer": "EIXOS"})

    # ---- cotes: alçat ----
    o = O_ALC
    hdim(msp, 0, W, 0, -130, o)
    hdim(msp, 0, M, 0, -60, o)
    hdim(msp, M, W - M, 0, -60, o)
    vdim(msp, 0, H, 0, -260, o)
    vdim(msp, 0, Z_RAIL, 0, -130, o)
    vdim(msp, Z_RAIL, Z_SEAT_F, 0, -130, o)
    vdim(msp, Z_SEAT_F, Z_ARM, 0, -130, o)
    vdim(msp, Z_ARM, Z_ARM + M, 0, -130, o)
    vdim(msp, Z_ARM + M, H, 0, -130, o)
    label(msp, "ALÇAT", o[0] + W / 2, o[1] + H + 120)

    # ---- cotes: perfil ----
    o = O_PER
    hdim(msp, 0, D, 0, -130, o)
    hdim(msp, 0, M, 0, -60, o)                       # pal respatller
    hdim(msp, M, D - Y_REAR - M, 0, -60, o)
    hdim(msp, D - Y_REAR - M, D - Y_REAR, 0, -60, o)  # pota posterior
    hdim(msp, D - Y_REAR, D - M, 0, -60, o)
    hdim(msp, D - M, D, 0, -60, o)                    # pota davantera
    hdim(msp, 0, D - Y_ARM, Z_ARM + M, Z_ARM + M + 90, o)   # braç
    vdim(msp, 0, Z_SEAT_R, D, D + 120, o)
    vdim(msp, 0, Z_SEAT_F, D, D + 220, o)
    vdim(msp, 0, Z_ARM + M, D, D + 320, o)
    vdim(msp, 12 * M, 15 * M, 0, -120, o)
    vdim(msp, 21 * M, 23 * M + M // 2, 0, -120, o)
    label(msp, "PERFIL ESQUERRE", o[0] + D / 2, o[1] + H + 120)

    # ---- cotes: planta ----
    o = O_PLA
    hdim(msp, 0, W, D, D + 110, o)
    vdim(msp, 0, D, 0, -130, o)
    vdim(msp, 0, Y_ARM, W, W + 90, o)
    vdim(msp, Y_REAR, Y_REAR + M, W, W + 90, o)
    vdim(msp, Y_ARM, Y_REAR, W, W + 90, o)
    vdim(msp, Y_REAR + M, D - M, W, W + 90, o)
    vdim(msp, D - M, D, W, W + 90, o)
    label(msp, "PLANTA", o[0] + W / 2, o[1] - 230)

    # ---- perspectiva isomètrica ----
    segs = visible_segments(solids, ISO_DIR, proj_iso)
    xs = [c for p, q, _ in segs for c in (p[0], q[0])]
    ys = [c for p, q, _ in segs for c in (p[1], q[1])]
    cx, cy = (min(xs) + max(xs)) / 2, min(ys)
    O_ISO = (3300 - cx, 380 - cy)
    draw_segments(msp, segs, O_ISO)
    label(msp, "PERSPECTIVA ISOMÈTRICA", 3300, 380 + (max(ys) - min(ys)) + 120)

    # ---- llegenda del mòdul ----
    text(msp, f"Mòdul base  M = {M} mm  (secció dels llistons {M}x{M})",
         1550, mg + 60, h=2.5 * SCALE)
    text(msp, f"Amplada {W // M}M · Profunditat {D // M}M · Alçada {H // M}M",
         1550, mg + 120, h=2.5 * SCALE)

    doc.saveas(path_dxf)
    return doc, solids


def export_stl(solids, path):
    """Model 3D en STL (per a visualització / render)."""
    with open(path, "w") as f:
        f.write("solid cadira_breuer\n")
        for s in solids:
            for face in s.faces:
                pts = s.v[face]
                c = s.v.mean(axis=0)
                for i in range(1, len(pts) - 1):
                    a, b, cc = pts[0], pts[i], pts[i + 1]
                    n = np.cross(b - a, cc - a)
                    n /= np.linalg.norm(n)
                    if n @ (a - c) < 0:
                        b, cc, n = cc, b, -n
                    f.write(f" facet normal {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}\n"
                            "  outer loop\n")
                    for p in (a, b, cc):
                        f.write(f"   vertex {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}\n")
                    f.write("  endloop\n endfacet\n")
        f.write("endsolid cadira_breuer\n")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    here = Path(__file__).parent
    doc, solids = main(str(here / "EXAR_L1_cadira_breuer.dxf"))
    export_stl(solids, str(here / "EXAR_L1_cadira_breuer_3D.stl"))
    if "--pdf" in sys.argv:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
        ax = fig.add_axes([0, 0, 1, 1])
        from ezdxf.addons.drawing.config import (Configuration, BackgroundPolicy,
                                                 ColorPolicy)
        cfg = Configuration(background_policy=BackgroundPolicy.WHITE,
                            color_policy=ColorPolicy.COLOR)
        ctx = RenderContext(doc)
        ctx.set_current_layout(doc.modelspace())
        Frontend(ctx, MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace(), finalize=True)
        fig.savefig(str(here / "EXAR_L1_cadira_breuer_CAD.pdf"))
        fig.savefig(str(here / "preview.png"), dpi=150)
