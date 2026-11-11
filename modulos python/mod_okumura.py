"""Modelo Okumura-Hata"""

import numpy as np

from modelo_base import ModeloBase


class Okumura(ModeloBase):

    variables = {
        "Frecuencia (MHz)": (150, 1500, "Frecuencia (f) entre 150-1500 MHz"),
        "Altura antena base (m)": (30, 200, "Altura antena base (hb) entre 30-200 m"),
        "Distancia (km)": (1, 20, "Distancia (d) entre 1-20 km"),
        "Corrección por altura del receptor": (0, 0, "a(hm)"),
        "Pérdida (dB)": (0, 0, "Ingrese la pérdida en un entorno urbano"),
    }

    def calcular(self, v):
        f = v.get("Frecuencia (MHz)")
        hb = v.get("Altura antena base (m)")
        d = v.get("Distancia (km)")
        ahm = v.get("Corrección por altura del receptor")
        pl = v.get("Pérdida (dB)")

        sel = self.seleccion_modelo

        if sel == "Frecuencia (MHz)":
            return 10 ** ((pl - 69.55 + 13.82 * np.log10(hb) + ahm - (44.9 - 6.55 * np.log10(hb)) * np.log10(d)) / 26.16)

        if sel == "Altura antena base (m)":
            return 10 ** ((69.55 + 26.16 * np.log10(f) - pl + 44.9 * np.log10(d) - ahm) / (13.82 + 6.55 * np.log10(d)))

        if sel == "Distancia (km)":
            return 10 ** ((pl - 69.55 - 26.16 * np.log10(f) + 13.82 * np.log10(hb) + ahm) / (44.9 - 6.55 * np.log10(hb)))

        if sel == "Corrección por altura del receptor":
            return 69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(hb) + (44.9 - 6.55 * np.log10(hb)) * np.log10(d) - pl

        if sel == "Pérdida (dB)":
            return 69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(hb) - ahm + (44.9 - 6.55 * np.log10(hb)) * np.log10(d)
