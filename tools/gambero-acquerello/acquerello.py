# densità (nero con opacità) + luci → acquerello cobalto: bordi mossi, granulazione, bordo che asciuga, fioriture
from PIL import Image
import numpy as np, sys
from scipy import ndimage as nd
def fbm(shape, seed, scales):
    rng = np.random.default_rng(seed); out = np.zeros(shape)
    for i, s in enumerate(scales):
        n = nd.gaussian_filter(rng.standard_normal(shape), s); out += n / (n.std() + 1e-9) * 0.55 ** i
    return out / out.std()
def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def run(pig_png, luce_png, dst, seed=5, k=2.0):
    d = np.array(Image.open(pig_png).convert('RGBA')).astype(float)[..., 3] / 255
    l = np.array(Image.open(luce_png).convert('RGBA')).astype(float)[..., 3] / 255
    H, W = d.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dx = fbm((H, W), seed, (36*k, 12*k)) * 2.6*k; dy = fbm((H, W), seed+1, (36*k, 12*k)) * 2.6*k
    warp = lambda img: nd.map_coordinates(img, [yy+dy, xx+dx], order=1)
    d = warp(d); l = nd.gaussian_filter(warp(l), 1.6*k)
    d = nd.gaussian_filter(d, 0.6*k)
    d = d * (1 - l * 0.85)                                         # luci: carta che torna fuori
    wash = fbm((H, W), seed+3, (50*k, 18*k)); grain = fbm((H, W), seed+2, (2*k, 1*k))
    d = d * (0.84 + 0.13*wash + 0.08*grain)
    rim = np.clip(d - nd.gaussian_filter(d, 2.5*k), 0, 1); d = d + rim * 0.6
    bloom = smooth(fbm((H, W), seed+4, (22*k, 8*k)), 1.0, 1.9)
    d = d * (1 - bloom * 0.4 * smooth(d, 0.08, 0.3) * (1 - smooth(d, 0.6, 0.85)))
    d = np.clip(d, 0, 1)
    light = np.array([96, 126, 214]); deep = np.array([4, 12, 98])
    t = smooth(d, 0.12, 0.92)[..., None]
    rgb = light*(1-t) + deep*t
    alpha = smooth(d, 0.02, 0.36)
    img = Image.fromarray(np.dstack([rgb, alpha*255]).astype(np.uint8))
    x0, y0, x1, y1 = img.getbbox()
    img.crop((max(0, x0-6), max(0, y0-6), min(W, x1+6), min(H, y1+6))).save(dst, quality=90, method=6)
if __name__ == '__main__':
    run(*sys.argv[1:4], int(sys.argv[4]) if len(sys.argv) > 4 else 5)
