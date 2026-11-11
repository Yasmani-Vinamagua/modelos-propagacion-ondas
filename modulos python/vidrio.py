"""Efecto "liquid glass": fondo líquido y paneles de vidrio esmerilado.

Tk no tiene transparencia ni desenfoque por widget, así que el efecto se dibuja
con imágenes (PIL + numpy) sobre un Canvas:

  - fondo(): Medianoche con manchas suaves de Azul marino y un resplandor Rosa.
  - tarjeta(): panel con el fondo desenfocado en el borde, reflejos de luz en
    el canto (más fuertes arriba a la izquierda), brillo interior y sombra.

El interior de cada panel es de un color uniforme (estilos.VIDRIO). Así los
widgets que se colocan encima, que son opacos, se funden con el panel sin que
se vean costuras. El efecto de vidrio vive en el borde (EDGE px).
"""

import numpy as np
from PIL import Image, ImageFilter

import estilos

EDGE = 22     # grosor (px lógicos) de la franja de vidrio; el interior es liso
MARGEN = 48   # margen transparente alrededor del panel para la sombra


def _rgb(hexa):
    return np.array([int(hexa[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32)


def _suavizar(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def fondo(ancho, alto, escala=1.0):
    """Fondo líquido. Devuelve una imagen PIL RGB de (ancho·escala) x (alto·escala)."""
    w, h = int(round(ancho * escala)), int(round(alto * escala))
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    x /= w
    y /= h

    img = np.empty((h, w, 3), dtype=np.float32)
    img[:] = _rgb(estilos.MEDIANOCHE)

    azul, rosa, bruma = _rgb(estilos.AZUL_MARINO), _rgb(estilos.ROSA), _rgb(estilos.BRUMA)

    # (cx, cy, radio_x, radio_y, giro, color, peso): manchas elípticas suaves
    manchas = [
        (0.08, 0.10, 0.40, 0.55, 0.5, azul, 0.95),
        (0.62, 0.50, 0.45, 0.28, -0.4, azul, 0.75),
        (0.95, 0.98, 0.22, 0.30, 0.3, rosa, 0.80),     # resplandor rosa (acento, esquina inferior)
        (0.40, 1.05, 0.30, 0.16, 0.0, azul, 0.60),
        (0.55, -0.02, 0.35, 0.12, 0.0, bruma, 0.10),   # luz tenue arriba
    ]
    for cx, cy, rx, ry, giro, color, peso in manchas:
        dx, dy = x - cx, (y - cy) * (h / w)
        c, s = np.cos(giro), np.sin(giro)
        u, v = dx * c + dy * s, -dx * s + dy * c
        g = np.exp(-((u / rx) ** 2 + (v / (ry * h / w)) ** 2)) * peso
        img += g[..., None] * (color - img)

    # Grano muy fino para evitar bandas en los degradados
    rng = np.random.default_rng(7)
    img += rng.normal(0, 1.1, (h, w, 1)).astype(np.float32)

    return Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8), "RGB")


def tarjeta(ancho, alto, radio, pos, imagen_fondo, escala=1.0):
    """Panel de vidrio con sombra.

    pos: (x, y) del panel en px lógicos sobre el fondo. imagen_fondo: lo que hay detrás.
    Devuelve una imagen RGBA de (ancho + 2·MARGEN) x (alto + 2·MARGEN) px lógicos (por escala),
    para colocarla en (x − MARGEN, y − MARGEN).
    """
    s = escala
    P = int(round(MARGEN * s))
    w, h = int(round(ancho * s)), int(round(alto * s))
    W, H = w + 2 * P, h + 2 * P
    r = radio * s

    # --- lo que hay detrás del panel, desenfocado (vidrio esmerilado)
    x0, y0 = int(round(pos[0] * s)) - P, int(round(pos[1] * s)) - P
    fondo_arr = np.asarray(imagen_fondo, dtype=np.float32)
    fondo_arr = np.pad(fondo_arr, ((P, P), (P, P), (0, 0)), mode="edge")
    recorte = fondo_arr[y0 + P:y0 + P + H, x0 + P:x0 + P + W]
    desenfocado = np.asarray(
        Image.fromarray(recorte.astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * s)),
        dtype=np.float32)

    # --- distancia al borde (negativa fuera, positiva dentro) con esquinas redondeadas
    py, px = np.mgrid[0:H, 0:W].astype(np.float32)
    qx = np.abs(px - W / 2) - (w / 2 - r)
    qy = np.abs(py - H / 2) - (h / 2 - r)
    fuera = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
    sdf = fuera + np.minimum(np.maximum(qx, qy), 0) - r
    dist = -sdf
    mascara = np.clip(0.5 + dist, 0, 1)  # borde suavizado de 1 px

    # --- orientación del canto respecto a la luz (arriba a la izquierda)
    gy, gx = np.gradient(sdf)
    norma = np.maximum(np.hypot(gx, gy), 1e-6)
    luz = np.clip((gx * -0.6 + gy * -0.8) / norma, 0, 1)      # canto que mira a la luz
    contraluz = np.clip((gx * 0.6 + gy * 0.8) / norma, 0, 1)  # canto opuesto: refracción tenue

    blanco = _rgb(estilos.BLANCO)
    interior = _rgb(estilos.VIDRIO)

    # --- color: fondo desenfocado con velo blanco en el borde, que se funde con el interior liso
    t = _suavizar(dist / (EDGE * s))
    esmerilado = desenfocado * 0.90 + blanco * 0.10
    color = esmerilado * (1 - t[..., None]) + interior * t[..., None]

    # --- reflejos de luz (todos se anulan hacia el interior)
    borde = 1 - t
    fino = np.exp(-(dist / (1.5 * s)) ** 2)                  # filo brillante del canto
    segundo = np.exp(-((dist - 4.5 * s) / (2.6 * s)) ** 2)   # segundo filo interior
    brillo = np.exp(-np.maximum(dist, 0) / (9 * s))          # resplandor que baja hacia dentro

    luz_total = (fino * (0.18 + 0.62 * luz + 0.16 * contraluz)
                 + segundo * 0.20 * (0.3 + luz)
                 + brillo * 0.10 * (0.35 + luz)) * borde
    # Mancha de luz suave en la esquina superior izquierda (reflejo curvo)
    mancha = np.exp(-(((px - W * 0.20) / (w * 0.30)) ** 2 + ((py - (P + 0.02 * h)) / (h * 0.05)) ** 2))
    luz_total += mancha * 0.11 * borde

    luz_total = np.clip(luz_total, 0, 1)[..., None]
    color = color + (blanco - color) * luz_total  # la luz aclara hacia el blanco sin quemar
    color = np.clip(color, 0, 255)

    rgba = np.dstack([color, mascara * 255]).astype(np.uint8)
    panel = Image.fromarray(rgba, "RGBA")

    # --- sombra suave debajo del panel
    sombra_mask = Image.fromarray((mascara * 255).astype(np.uint8), "L")
    sombra_mask = sombra_mask.transform(sombra_mask.size, Image.AFFINE, (1, 0, 0, 0, 1, -14 * s))
    sombra_mask = sombra_mask.filter(ImageFilter.GaussianBlur(20 * s))
    sombra_alfa = sombra_mask.point(lambda v: int(v * 0.50))
    sombra = Image.new("RGBA", (W, H), (3, 6, 16, 0))
    sombra.putalpha(sombra_alfa)

    return Image.alpha_composite(sombra, panel)
