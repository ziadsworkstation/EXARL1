"""
Render 3D (raytracing ortogonal) de la cadira en projecció isomètrica.
Genera un PNG amb transparència: fusta, làmines, ombra al terra i arestes.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cad"))
import cadira_breuer as cb  # noqa: E402

WOOD = np.array([0.40, 0.21, 0.12])       # noguera / cirerer
LAMINA = np.array([0.80, 0.45, 0.24])     # làmina (to tèxtil original)
SUN = np.array([0.35, -0.75, 1.0]); SUN /= np.linalg.norm(SUN)


def intersect(solids, O, d):
    """O: (N,3) orígens, d: (3,) direcció. Retorna t, índex sòlid, normal."""
    N = O.shape[0]
    best_t = np.full(N, np.inf)
    best_s = np.full(N, -1)
    best_n = np.zeros((N, 3))
    for si, s in enumerate(solids):
        t0 = np.full(N, -np.inf)
        t1 = np.full(N, np.inf)
        n0 = np.zeros((N, 3))
        ok = np.ones(N, bool)
        for n, dd in s.planes:
            nv = n @ d
            dist = dd - O @ n
            if abs(nv) < 1e-12:
                ok &= dist > 0
                continue
            t = dist / nv
            if nv < 0:
                upd = t > t0
                t0 = np.where(upd, t, t0)
                n0[upd] = n
            else:
                t1 = np.minimum(t1, t)
        hit = ok & (t0 < t1) & (t0 > 1e-3) & (t0 < best_t)
        best_t[hit] = t0[hit]
        best_s[hit] = si
        best_n[hit] = n0[hit]
    return best_t, best_s, best_n


def render(path, px_per_mm=2.2, ss=2):
    solids = cb.build_chair()
    f = -cb.ISO_DIR / np.linalg.norm(cb.ISO_DIR)
    r, u = cb._r, cb._u
    V = np.vstack([s.v for s in solids])
    # incloure la projecció de l'ombra al terra en els límits
    sh = V - np.outer(V[:, 2] / SUN[2], SUN)
    P = np.vstack([V, sh])
    rr, uu = P @ r, P @ u
    m = 40
    r0, r1, u0, u1 = rr.min() - m, rr.max() + m, uu.min() - m, uu.max() + m
    k = px_per_mm * ss
    Wp, Hp = int((r1 - r0) * k), int((u1 - u0) * k)
    xs = r0 + (np.arange(Wp) + 0.5) / k
    ys = u1 - (np.arange(Hp) + 0.5) / k
    X, Y = np.meshgrid(xs, ys)
    c = V.mean(axis=0)
    base = c - (c @ r) * r - (c @ u) * u - 3000 * f
    O = base + X.reshape(-1, 1) * r + Y.reshape(-1, 1) * u

    rgba = np.zeros((O.shape[0], 4))
    shadow_a = np.zeros(O.shape[0])
    chunk = 400_000
    for a in range(0, O.shape[0], chunk):
        Oc = O[a:a + chunk]
        t, si, n = intersect(solids, Oc, f)
        hit = si >= 0
        # superfície dels sòlids
        Ph = Oc[hit] + t[hit, None] * f
        _, sb, _ = intersect(solids, Ph + n[hit] * 0.05, SUN)
        lit = (sb < 0).astype(float)
        lam = np.clip(n[hit] @ SUN, 0, 1)
        sky = 0.5 + 0.5 * n[hit][:, 2]
        kinds = np.array([solids[i].kind == "lamina" for i in si[hit]])
        col = np.where(kinds[:, None], LAMINA, WOOD)
        shade = 0.30 + 0.22 * sky[:, None] + 0.75 * (lam * lit)[:, None]
        rgb = np.clip(col * shade, 0, 1)
        blk = rgba[a:a + chunk]
        blk[hit, :3] = rgb
        blk[hit, 3] = 1
        # terra (z = 0): només ombra
        miss = ~hit & (np.abs(f[2]) > 1e-9)
        tf = -Oc[miss, 2] / f[2]
        Pf = Oc[miss] + tf[:, None] * f
        _, sf, _ = intersect(solids, Pf + np.array([0, 0, 0.05]), SUN)
        sa = shadow_a[a:a + chunk]
        idx = np.where(miss)[0]
        sa[idx[sf >= 0]] = 1
    img = (rgba.reshape(Hp, Wp, 4) * 255).astype(np.uint8)
    obj = Image.fromarray(img, "RGBA")

    # arestes visibles
    segs = cb.visible_segments(solids, cb.ISO_DIR, lambda p: (p @ r, p @ u), step=1.5)
    draw = ImageDraw.Draw(obj)
    for p, q, kind in segs:
        a_ = ((p[0] - r0) * k, (u1 - p[1]) * k)
        b_ = ((q[0] - r0) * k, (u1 - q[1]) * k)
        draw.line([a_, b_], fill=(40, 20, 12, 150), width=max(1, int(0.6 * ss)))

    sh_img = Image.fromarray((shadow_a.reshape(Hp, Wp) * 255).astype(np.uint8), "L")
    sh_img = sh_img.filter(ImageFilter.GaussianBlur(6 * ss))
    shadow = Image.new("RGBA", (Wp, Hp), (70, 60, 50, 0))
    shadow.putalpha(sh_img.point(lambda v: int(v * 0.22)))
    out = Image.alpha_composite(shadow, obj)
    out = out.resize((Wp // ss, Hp // ss), Image.LANCZOS)
    out.save(path)
    return out.size, (r0, r1, u0, u1)


if __name__ == "__main__":
    here = Path(__file__).parent
    print(render(here / "assets" / "render_iso.png"))
