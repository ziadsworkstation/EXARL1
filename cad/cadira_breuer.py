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
# Segona versió (1924): tota l'estructura amb un únic llistó estandarditzat,
# només canvia la llargada.  Llistó real ~25 x 54 mm  ->  proposta 24 x 48.
M = 48                    # mòdul base = amplada del llistó
t = M // 2                # gruix del llistó (24) = ½ M
W = 12 * M                # amplada total      576  (real 570)
D = 12 * M                # profunditat total  576  (real 575)
H = 20 * M                # alçada total       960  (real 960)

Z_RAIL = 7 * M            # travesser lateral (cantell)  336-384
Z_FLEG = 9 * M            # pota davantera               432
Z_FRAIL = 7.5 * M         # travesser seient davant      360-408
Z_RRAIL = 6.5 * M         # travesser seient darrere     312-360
Z_ARM = 12.5 * M          # pota posterior / sota braç   600  (braç 600-624)
Z_BRAIL = 10 * M          # travesser respatller         480-528
Z_STRAP_L = 10 * M        # làmina respatller inferior   480-576
Z_STRAP_U = 16 * M        # làmina respatller superior   768-864
Z_HOLD = 19 * M           # suport làmina superior       624-912
Y_ARM = 2 * M             # voladís del braç (davant)     96
Y_REAR = 9 * M            # cara davantera pota posterior 432
T = 6                     # gruix de les làmines (seient i respatller)


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


def prism_x(name, x0, x1, quad_yz, kind="lamina"):
    """Prisma extruït en X a partir d'un quadrilàter convex al pla YZ."""
    v = [(x0, y, z) for y, z in quad_yz] + [(x1, y, z) for y, z in quad_yz]
    return Solid(name, v, BOX_FACES, kind)


def build_chair():
    """18 llistons + 3 làmines.  Pla exterior (x 0-24): potes davanteres i
    travessers laterals.  Pla interior (x 24-72): potes posteriors, pals del
    respatller, braços i suports de la làmina superior."""
    s = []
    for side, mir in (("E", False), ("D", True)):
        def bx(name, x0, x1, *rest, kind="wood"):
            if mir:
                x0, x1 = W - x1, W - x0
            s.append(box(f"{name} {side}", x0, x1, *rest, kind=kind))
        bx("pota davantera", 0, t, 0, M, 0, Z_FLEG)
        bx("travesser lateral", 0, t, M, D, Z_RAIL, Z_RAIL + M)
        bx("pota posterior", t, t + M, Y_REAR, Y_REAR + t, 0, Z_ARM)
        bx("pal respatller", t, t + M, D - t, D, Z_RAIL, H)
        bx("braç", t, t + M, Y_ARM, D - t, Z_ARM, Z_ARM + t)
        bx("suport làmina", t, t + M, D - 2 * t, D - t, Z_ARM + t, Z_HOLD)
    # travessers transversals
    s.append(box("travesser seient davant", t, W - t, 0, t, Z_FRAIL, Z_FRAIL + M))
    s.append(box("travesser seient darrere", t + M, W - t - M, Y_REAR, Y_REAR + t,
                 Z_RRAIL, Z_RRAIL + M))
    s.append(box("travesser respatller", t + M, W - t - M, D - t, D,
                 Z_BRAIL, Z_BRAIL + M))
    # làmina del seient (inclinada, del travesser davanter al posterior)
    zf, zr = Z_FRAIL + M, Z_RRAIL + M
    s.append(prism_x("làmina seient", t, W - t,
                     [(0, zf), (Y_REAR + t, zr), (Y_REAR + t, zr + T), (0, zf + T)],
                     kind="lamina"))
    # làmines del respatller
    s.append(box("làmina respatller inferior", t, W - t, Y_REAR - T, Y_REAR,
                 Z_STRAP_L, Z_STRAP_L + 2 * M, kind="lamina"))
    s.append(box("làmina respatller superior", t, W - t, D - 2 * t - T, D - 2 * t,
                 Z_STRAP_U, Z_STRAP_U + 2 * M, kind="lamina"))
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
    doc.layers.add("LAMINA", color=7, lineweight=50)
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
                     dxfattribs={"layer": "FUSTA" if kind == "wood" else "LAMINA"})


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
    info = ["Alumne: Ziad Addami Ech Chaouy", "Professor: De Castro Losada, Rubén",
            "Grup: D3012 · Assignatura: EXAR", "Data: 05/10/2026"]
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
    hdim(msp, 0, t, 0, -60, o)
    hdim(msp, t, t + M, 0, -60, o)
    hdim(msp, t + M, W - t - M, 0, -60, o)
    hdim(msp, W - t - M, W - t, 0, -60, o)
    hdim(msp, W - t, W, 0, -60, o)
    vdim(msp, 0, H, 0, -260, o)
    for a, b in ((0, Z_FLEG), (Z_FLEG, Z_ARM), (Z_ARM, Z_ARM + t),
                 (Z_ARM + t, Z_HOLD), (Z_HOLD, H)):
        vdim(msp, a, b, 0, -130, o)
    for a, b in ((0, Z_FRAIL), (Z_FRAIL, Z_FRAIL + M),
                 (Z_STRAP_U, Z_STRAP_U + 2 * M)):
        vdim(msp, a, b, W, W + 110, o)
    label(msp, "ALÇAT", o[0] + W / 2, o[1] + H + 120)

    # ---- cotes: perfil (davant a la dreta) ----
    o = O_PER
    hdim(msp, 0, D, 0, -130, o)
    hy = [0, t, D - Y_REAR - t, D - Y_REAR, D - M, D]
    for a, b in zip(hy, hy[1:]):
        hdim(msp, a, b, 0, -60, o)
    hdim(msp, t, D - Y_ARM, Z_ARM + t, Z_ARM + t + 80, o)       # braç
    hdim(msp, D - Y_ARM, D, Z_ARM + t, Z_ARM + t + 80, o)       # voladís
    vdim(msp, 0, Z_RRAIL + M, D, D + 110, o)
    vdim(msp, 0, Z_FRAIL + M, D, D + 200, o)
    vdim(msp, 0, Z_ARM + t, D, D + 290, o)
    vdim(msp, Z_RAIL, Z_RAIL + M, 0, -110, o)
    vdim(msp, Z_STRAP_L, Z_STRAP_L + 2 * M, 0, -110, o)
    vdim(msp, Z_STRAP_U, Z_STRAP_U + 2 * M, 0, -110, o)
    label(msp, "PERFIL ESQUERRE", o[0] + D / 2, o[1] + H + 120)

    # ---- cotes: planta ----
    o = O_PLA
    hdim(msp, 0, W, D, D + 110, o)
    vdim(msp, 0, D, 0, -130, o)
    vy = [0, M, Y_ARM, Y_REAR, Y_REAR + t, D - 2 * t, D - t, D]
    for a, b in zip(vy, vy[1:]):
        vdim(msp, a, b, W, W + 90, o)
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
    text(msp, f"Mòdul base  M = {M} mm  ·  llistó estandarditzat {t}x{M} (½M x M)",
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
        fig.savefig(str(here / "preview.png"), dpi=300)
