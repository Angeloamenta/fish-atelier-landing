# Gambero stilizzato "da maiolica": pennellate rastremate (larghe al centro, sottili alle punte),
# velature chiare, ombre sul ventre, luci lasciate in bianco. Disegnato come densità di pigmento
# (nero con opacità): acquerello_vett2.py la trasforma nel cobalto del polpo del cliente.
import numpy as np, sys

def bez(p, t):
    p = np.array(p, float); t = np.asarray(t)[..., None]
    return (1-t)**3*p[0] + 3*(1-t)**2*t*p[1] + 3*(1-t)*t**2*p[2] + t**3*p[3]

def catmull(pts, n=24):
    pts = [np.array(p, float) for p in pts]
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[i-1] if i > 0 else pts[i]; p1 = pts[i]; p2 = pts[i+1]; p3 = pts[i+2] if i+2 < len(pts) else pts[i+1]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t*t, t*t*t
            out.append(0.5*((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t2 + (-p0+3*p1-3*p2+p3)*t3))
    out.append(pts[-1])
    return np.array(out)

def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'

def brush(pts, width, taper=(0.15, 0.25), d=0.95, smooth=True):
    """pennellata: poligono con larghezza che cresce e cala lungo il tratto"""
    P = catmull(pts) if smooth else np.array(pts, float)
    seg = np.diff(P, axis=0); L = np.concatenate([[0], np.cumsum(np.linalg.norm(seg, axis=1))]); u = L / L[-1]
    Tg = np.gradient(P, axis=0); Tg /= np.linalg.norm(Tg, axis=1)[:, None] + 1e-9
    Nn = np.stack([-Tg[:, 1], Tg[:, 0]], 1)
    w = width * np.minimum(1, np.minimum(u / taper[0], (1 - u) / taper[1])) ** 0.6
    w = np.maximum(w, 0.6)
    left = P + Nn * (w / 2)[:, None]; right = P - Nn * (w / 2)[:, None]
    return f'<path d="{poly(list(left) + list(right[::-1]))}" fill="#000" fill-opacity="{d}"/>'

def area(pts, d, smooth=True):
    P = catmull(list(pts) + [pts[0]]) if smooth else np.array(pts)
    return f'<path d="{poly(P)}" fill="#000" fill-opacity="{d}"/>'

def thickness(s):
    return np.interp(s, [0, 0.04, 0.12, 0.26, 0.37, 0.48, 0.66, 0.84, 1.0], [56, 132, 176, 178, 152, 126, 96, 66, 46])

def gambero(spine, W=1100, H=860, flip=False):
    pig, luce = [], []
    S = np.linspace(0, 1, 260)
    C = bez(spine, S)
    T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    N = np.stack([T[:, 1], -T[:, 0]], 1)
    if N[len(N)//2, 1] > 0: N = -N
    th = thickness(S)
    dorso = C + N * (th * 0.55)[:, None]; ventre = C - N * (th * 0.45)[:, None]
    at = lambda s: int(np.clip(round(s * (len(S) - 1)), 0, len(S) - 1))
    rng = np.random.default_rng(4)

    # --- antenne: due lunghe pennellate a S sopra il dorso
    base = C[at(0.025)] + N[at(0.025)] * th[at(0.025)] * 0.05
    f0, u0 = -T[0], N[0]
    for k in range(2):
        # salgono appena sopra la testa e ricadono all'indietro lungo il dorso
        pts = [base, base + f0*(60+20*k) + u0*(40+15*k), base + f0*(10-20*k) + u0*(120+25*k),
               base - f0*(180+50*k) + u0*(150+15*k), base - f0*(430+60*k) + u0*(120-10*k), base - f0*(620+50*k) + u0*(40-30*k)]
        pig.append(brush(pts, 6.5 - k*1.8, (0.05, 0.6)))
    # antennule e scaglie antennali (la "foglia" davanti alla testa)
    for k in range(2):
        p0 = C[at(0.02)] - N[0] * th[0] * 0.05
        pig.append(brush([p0, p0 + f0*(80+10*k) + u0*(10+16*k), p0 + f0*(160+20*k) + u0*(-10+40*k)], 4.5, (0.1, 0.5)))
    sc0 = C[at(0.03)] - N[at(0.03)] * th[at(0.03)] * 0.15
    scale_leaf = [sc0, sc0 + f0*70 - u0*12, sc0 + f0*120 - u0*4, sc0 + f0*70 + u0*14]
    pig.append(area(scale_leaf, 0.35)); pig.append(brush(scale_leaf + [sc0], 3.5, (0.05, 0.05)))

    # --- zampe: cinque paia sottili, piegate in avanti
    for k, s in enumerate(np.linspace(0.07, 0.33, 5)):
        p0 = ventre[at(s)] + N[at(s)] * 16
        dn, fw = -N[at(s)], -T[at(s)]
        lean = [34, 22, 10, -2, -14][k]            # le prime puntano avanti, le ultime indietro
        a1 = p0 + dn*(30+4*k) + fw*(lean*0.6)
        a2 = a1 + dn*(30) + fw*(lean + 14)
        a3 = a2 + dn*(10) + fw*(lean*0.8 + 18)
        pig.append(brush([p0, a1, a2, a3], 5.5 - k*0.4, (0.05, 0.5), d=0.8))
    # massillipedi
    for k in range(2):
        p0 = ventre[at(0.025)] + N[at(0.025)] * 16
        pig.append(brush([p0, p0 - N[0]*28 + f0*(40+12*k), p0 - N[0]*(30+14*k) + f0*(90+18*k)], 4.5, (0.05, 0.5), d=0.85))
    # pleopodi: pinnette sotto l'addome
    for s in np.linspace(0.43, 0.85, 5):
        p0 = ventre[at(s)] + N[at(s)] * 8
        leaf = [p0, p0 - N[at(s)]*30 + T[at(s)]*12, p0 - N[at(s)]*44 + T[at(s)]*28, p0 - N[at(s)]*20 + T[at(s)]*26]
        pig.append(area(leaf, 0.45)); pig.append(brush([p0, p0 - N[at(s)]*44 + T[at(s)]*28], 3, (0.1, 0.3)))

    # --- ventaglio della coda: cinque lobi a raggiera con la nervatura
    end, te = C[-1], T[-1]
    for ang, ln, wd, dd in [(0.85, 125, 74, 0.36), (-0.85, 125, 74, 0.36), (0.42, 150, 76, 0.46), (-0.42, 150, 76, 0.46), (0.0, 165, 44, 0.6)]:
        c, s_ = np.cos(ang), np.sin(ang)
        dvec = np.array([te[0]*c - te[1]*s_, te[0]*s_ + te[1]*c]); nv = np.array([dvec[1], -dvec[0]])
        lobe = [end + nv*wd*0.15, end + dvec*ln*0.45 + nv*wd*0.55, end + dvec*ln*0.95 + nv*wd*0.12, end + dvec*ln,
                end + dvec*ln*0.6 - nv*wd*0.45, end - nv*wd*0.15]
        pig.append(area(lobe, dd))
        pig.append(brush(lobe + [lobe[0]], 4.2, (0.02, 0.02), d=0.9))
        pig.append(brush([end + dvec*12, end + dvec*ln*0.85], 2.6, (0.1, 0.4), d=0.7))
        luce.append(brush([end + dvec*ln*0.3 + nv*wd*0.2, end + dvec*ln*0.7 + nv*wd*0.15], 5, (0.3, 0.3)))

    # --- addome: sei segmenti dal fondo verso la testa (quello davanti copre il successivo)
    edges = [0.36, 0.47, 0.57, 0.665, 0.755, 0.845, 0.995]
    for i in range(len(edges) - 1, 0, -1):
        a, b = edges[i-1], min(1.0, edges[i] + 0.025)
        idx = list(range(at(a), at(b) + 1))
        top = [dorso[j] for j in idx]
        bottom = [ventre[j] - N[j] * np.sin(np.pi * (S[j]-a)/(b-a)) * 18 for j in reversed(idx)]
        pig.append(area(top + bottom, 0.36, smooth=False))
        # ombra sul ventre: mezza piastra più carica
        mid = [C[j] - N[j]*th[j]*0.05 for j in idx]
        pig.append(area(mid + bottom, 0.52, smooth=False))
        # contorno del segmento a pennello
        pig.append(brush(top, 6.5, (0.08, 0.08), d=0.95))
        pig.append(brush(bottom, 5.5, (0.1, 0.1), d=0.9))
        joint = [dorso[idx[-1]], C[idx[-1]] + N[idx[-1]]*th[idx[-1]]*0.1, ventre[idx[-1]] - N[idx[-1]]*10]
        pig.append(brush(joint, 6, (0.15, 0.3), d=0.95))
        # luce: tratto bianco lungo il dorso
        hl = [dorso[j] - N[j]*th[j]*0.15 for j in idx[3:-4]]
        if len(hl) > 2: luce.append(brush(hl, 9, (0.3, 0.3)))
        # decorazione maiolica: due archetti sul fianco
        for f in (0.35, 0.65):
            j = idx[int(len(idx)*f)]
            q = C[j] + N[j]*th[j]*0.12
            pig.append(brush([q - T[j]*10 + N[j]*6, q, q + T[j]*10 + N[j]*6], 3, (0.3, 0.3), d=0.7))

    # --- carapace
    idx = list(range(0, at(0.385) + 1))
    top = [dorso[j] for j in idx]; bottom = [ventre[j] for j in reversed(idx)]
    pig.append(area(top + bottom, 0.38, smooth=False))
    pig.append(area([C[j] - N[j]*th[j]*0.1 for j in idx] + bottom, 0.46, smooth=False))
    pig.append(brush(top, 7.5, (0.05, 0.05)))
    pig.append(brush(bottom, 6.5, (0.05, 0.1), d=0.9))
    # solco a voluta, tipico della maiolica
    gr = [C[j] + N[j]*th[j]*np.interp(S[j], [0.08, 0.2, 0.34], [0.22, 0.08, 0.18]) for j in range(at(0.08), at(0.34))]
    pig.append(brush(gr, 5, (0.2, 0.4), d=0.85))
    luce.append(brush([dorso[j] - N[j]*th[j]*0.14 for j in range(at(0.07), at(0.33))], 12, (0.25, 0.3)))
    # rostro seghettato, all'insù
    r0 = dorso[at(0.03)]; tip = r0 + f0*150 + u0*48
    teeth = []
    for k in range(6):
        q = r0 + (tip - r0)*(k/6); teeth += [q + u0*1, q + (tip-r0)*0.08 + u0*10]
    rostro = [C[at(0.02)] + N[at(0.02)]*th[at(0.02)]*0.2] + teeth + [tip, r0 + f0*70 - u0*6]
    pig.append(f'<path d="{poly(rostro)}" fill="#000" fill-opacity="0.85"/>')
    # occhio sul peduncolo
    e = C[at(0.05)] + N[at(0.05)]*th[at(0.05)]*0.1 + f0*6
    pig.append(f'<circle cx="{e[0]:.1f}" cy="{e[1]:.1f}" r="17" fill="#000" fill-opacity="0.97"/>')
    luce.append(f'<circle cx="{e[0]+5:.1f}" cy="{e[1]-6:.1f}" r="5" fill="#000"/>')

    def svg(items):
        g = ''.join(items)
        if flip: g = f'<g transform="translate({W} 0) scale(-1 1)">{g}</g>'
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{g}</svg>'
    return svg(pig), svg(luce)

POSE = {
    'curvo':  [(900, 330), (650, 200), (330, 230), (330, 600)],
    'teso':   [(960, 360), (700, 300), (420, 320), (210, 420)],
    'arco':   [(920, 450), (680, 280), (360, 260), (230, 610)],
}
if __name__ == '__main__':
    n = sys.argv[1]
    pig, luce = gambero(POSE[n])
    open(f'./{n}-pig.svg', 'w').write(pig); open(f'./{n}-luce.svg', 'w').write(luce)
