"""Modelo COST-231 Hata"""

import numpy as np

from modelo_base import ModeloBase


class COSTHata(ModeloBase):

    variables = {
        "Frecuencia (MHz)": (1500, 2000, "Frecuencia (f) entre 1500-2000 MHz"),
        "Altura antena base (m)": (30, 200, "Altura antena base (hb) entre 30-200 m"),
        "Corrección por altura del receptor": (0, 0, "a(hm)"),
        "Distancia (km)": (1, 20, "Distancia (d) entre 1-20 km"),
        "Constante C (dB)": (0, 3, "Constante C: 0 para rural, 3 para urbano"),
        "Pérdida (dB)": (0, 0, "Pérdida calculada (PL)"),
    }

    def calcular(self, v):
        f = v.get("Frecuencia (MHz)")
        hb = v.get("Altura antena base (m)")
        d = v.get("Distancia (km)")
        a_hm = v.get("Corrección por altura del receptor")
        pl = v.get("Pérdida (dB)")
        C = v.get("Constante C (dB)")

        sel = self.seleccion_modelo

        if sel == "Frecuencia (MHz)":
            return 10 ** ((pl - 46.3 + 13.82 * np.log10(hb) + a_hm -
                           (44.9 - 6.55 * np.log10(hb)) * np.log10(d) - C) / 33.9)

        if sel == "Altura antena base (m)":
            # Despejando log hb: (46.3 + 33.9·log f − a(hm) + 44.9·log d + C − PL) / (13.82 + 6.55·log d)
            return 10 ** ((46.3 + 33.9 * np.log10(f) - a_hm + 44.9 * np.log10(d) + C - pl)
                          / (13.82 + 6.55 * np.log10(d)))

        if sel == "Corrección por altura del receptor":
            return (46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) +
                    (44.9 - 6.55 * np.log10(hb)) * np.log10(d) + C - pl)

        if sel == "Distancia (km)":
            return 10 ** ((pl - 46.3 - 33.9 * np.log10(f) + 13.82 * np.log10(hb) + a_hm - C)
                          / (44.9 - 6.55 * np.log10(hb)))

        if sel == "Constante C (dB)":
            return pl - (46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) - a_hm +
                         (44.9 - 6.55 * np.log10(hb)) * np.log10(d))

        if sel == "Pérdida (dB)":
            return (46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) - a_hm +
                    (44.9 - 6.55 * np.log10(hb)) * np.log10(d) + C)
