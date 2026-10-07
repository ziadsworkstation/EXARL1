"""Genera las imágenes del portfolio, cada una en versión horizontal (φ:1) y vertical (1:φ).

- modulo-*: planta y alzado de la Slatted Chair dibujados a escala exacta desde el
  modelo paramétrico (cad/cadira_breuer.py) y colocados sobre la construcción áurea.
- render-*, lamina-*: recortes del render isométrico y de la lámina A3.
- r11-*: captura de la web de R11 (web/index.html) en n = 0.

  python3 ziadaddami/tools/make_images.py      (desde la raíz del repo)
Necesita: ezdxf, numpy, Pillow, pdftoppm y Playwright de Node (para la captura).
"""
import math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'web', 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'cad'))
from golden_crop import frame, padded_crop, PHI          # noqa: E402
import cadira_breuer as cb                                  # noqa: E402

OUT = os.path.join(ROOT, 'ziadaddami', 'img')
PAPER = (242, 241, 238)
INK = (30, 30, 30)
ORANGE = (194, 116, 69)          # el acento de la lámina
LW, LH = 1400, round(1400 / PHI) # 1400 × 865
MONO = None
for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',):
    if os.path.exists(f):
        MONO = f

def font(px):
    return ImageFont.truetype(MONO, px) if MONO else ImageFont.load_default()

def save(img, name):
    img.convert('RGB').save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=82, method=6)
    print('ok', name, img.size)

# ---------------------------------------------------------------- vistas CAD
def segments():
    solids = cb.build_chair()
    al = cb.visible_segments(solids, (0, -1, 0), cb.proj_alcat)
    pl = cb.visible_segments(solids, (0, 0, 1), cb.proj_planta)
    return al, pl

def draw_view(d, segs, ox, oy, sc, flip_y=True, h=None, lw=2):
    """Dibuja segmentos en mm con origen (ox, oy) en píxeles; y hacia arriba si flip_y."""
    for (p, q, kind) in segs:
        P = (ox + p[0] * sc, oy - p[1] * sc if flip_y else oy + p[1] * sc)
        Q = (ox + q[0] * sc, oy - q[1] * sc if flip_y else oy + q[1] * sc)
        d.line([P, Q], fill=ORANGE if kind == 'lamina' else INK, width=lw)

def modulo():
    al, pl = segments()
    W, D, H, M = cb.W, cb.D, cb.H, cb.M
    # Horizontal: alzado llena la altura del rectángulo restante R1 (1:φ ≈ 3:5);
    # la planta (cuadrada) se centra en el cuadrado 1. Misma escala para las dos vistas.
    s = LH
    img = Image.new('RGB', (LW, LH), PAPER); d = ImageDraw.Draw(img)
    sc = s / H                                   # 960 mm = altura total
    r1x, r1w = s, LW - s
    draw_view(d, al, r1x + (r1w - W * sc) / 2, s, sc)
    side = D * sc
    draw_view(d, pl, (s - side) / 2, (s - side) / 2, sc, flip_y=False)
    f = font(15)
    d.text(((s - side) / 2, (s - side) / 2 + side + 14), 'PLANTA  12M × 12M  (576 × 576)', fill=INK, font=f)
    d.text((r1x + (r1w - W * sc) / 2, 14), 'ALZADO  12M × 20M', fill=INK, font=f)
    save(img, 'modulo-l')
    # Vertical (móvil): en pantallas 9:19,5 solo se ve el 75 % central del ancho, así que
    # la planta se inscribe en el cuadrado 1 (abajo) dentro de esa franja.
    pw, ph = LH, LW
    img = Image.new('RGB', (pw, ph), PAPER); d = ImageDraw.Draw(img)
    side = 0.66 * pw; sc = side / D
    draw_view(d, pl, (pw - side) / 2, ph - pw + (pw - side) / 2, sc, flip_y=False, lw=3)
    d.text(((pw - side) / 2, ph - pw + (pw - side) / 2 + side + 16), 'PLANTA  12M × 12M', fill=INK, font=font(20))
    save(img, 'modulo-p')

# ---------------------------------------------------------------- recortes
def crop(src_img, name, cfg, mode='edge'):
    for o, out_w in (('L', 1400), ('P', 865)):
        c = cfg[o]
        (bx, by, _, _), _ = frame(o, (0, 0), c['s'])
        E = (c['tl'][0] - bx, c['tl'][1] - by)
        box, _ = frame(o, E, c['s'])
        img, pad = padded_crop(src_img, box, mode, out_w)
        save(img, f'{name}-{o.lower()}')

def render():
    im = Image.open(os.path.join(ROOT, 'lamina', 'assets', 'render_iso.png')).convert('RGBA')
    bg = Image.new('RGB', im.size, PAPER); bg.paste(im, mask=im.split()[3])
    # silla: x 91–1876, y 80–2823 (alto 2743). Horizontal: inscrita en el cuadrado 1.
    s_l = 2743 / 0.9
    s_p = 2743 / 0.9                              # vertical: inscrita en el cuadrado 1 (abajo)
    crop(bg, 'render', {'L': {'tl': (983 - s_l / 2, 80 - (s_l - 2743) / 2), 's': s_l},
                        'P': {'tl': (983 - s_p / 2, 80 - (s_l - 2743) / 2 - (PHI - 1) * s_p), 's': s_p}})

def lamina():
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-r', '200', '-png', os.path.join(ROOT, 'lamina', 'EXAR_L1_Addami_Ech_Chaouy_Ziad.pdf'),
                        os.path.join(tmp, 'l')], check=True)
        im = Image.open(os.path.join(tmp, 'l-1.png')).convert('RGB')
    w = im.size[0]
    # Horizontal: ancho completo, φ:1 → el A3 (1:√2) pierde la franja inferior.
    # Vertical: la columna de las vistas diédricas.
    k = w / 1489
    crop(im, 'lamina', {'L': {'tl': (0, 0), 's': w / PHI},
                        'P': {'tl': (445 * k, 263 * k), 's': 426 * k}})     # alzado + planta, centrados

def r11():
    js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w, h, n] of [[1456, 900, 'l'], [390, 844, 'p']]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + process.argv[2]);
    await p.addStyleTag({ content: '.hud,.cap,.veil{display:none!important}' });
    await p.waitForTimeout(1800);
    await p.screenshot({ path: process.argv[3] + '/r11-' + n + '.png' });
  }
  await b.close();
})();"""
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, 's.js'), 'w').write(js)
        npm_root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
        subprocess.run(['node', os.path.join(tmp, 's.js'), os.path.join(ROOT, 'web', 'index.html'), tmp],
                       check=True, env={**os.environ, 'NODE_PATH': npm_root})
        save(Image.open(os.path.join(tmp, 'r11-l.png')).resize((LW, LH), Image.LANCZOS), 'r11-l')
        # 390 × 844 es la parte visible de un rectángulo 1:φ de 521,6 × 844: se centra sobre papel
        shot = Image.open(os.path.join(tmp, 'r11-p.png'))
        rw = round(shot.size[1] / PHI)
        canvas = Image.new('RGB', (rw, shot.size[1]), PAPER); canvas.paste(shot, ((rw - shot.size[0]) // 2, 0))
        save(canvas.resize((LH, LW), Image.LANCZOS), 'r11-p')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    modulo(); render(); lamina(); r11()
