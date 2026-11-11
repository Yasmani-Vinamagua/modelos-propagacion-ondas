"""Modelo Egli (f en MHz, d en km, alturas en m)

    PL = K + 20·log f + 40·log d − 20·log ht − a·log hr
    hr <= 10 m -> K = 76.3, a = 10        hr > 10 m -> K = 85.9, a = 20
"""

import numpy as np

from modelo_base import ModeloBase


def constantes(hr):
    """Devuelve (K, a) según la altura de la antena receptora."""
    return (76.3, 10) if hr <= 10 else (85.9, 20)


class Egli(ModeloBase):

    variables = {
        "Frecuencia (MHz)": (30, 3000, "Frecuencia (f) entre 30-3000 MHz"),
        "Altura antena transmisora (m)": (3, 200, "Altura antena transmisora (ht) entre 3-200 m"),
        "Altura antena receptora (m)": (1, 50, "Altura antena receptora (hr) entre 1-50 m"),
        "Distancia (km)": (0.1, 20, "Distancia (d) entre 0.1-20 km"),
        "Pérdida (dB)": (0, 0, "Ingrese la pérdida (PL)"),
    }

    def calcular(self, v):
        f = v.get("Frecuencia (MHz)")
        ht = v.get("Altura antena transmisora (m)")
        hr = v.get("Altura antena receptora (m)")
        d = v.get("Distancia (km)")
        pl = v.get("Pérdida (dB)")

        sel = self.seleccion_modelo

        if sel == "Altura antena receptora (m)":
            # La constante depende de hr, que es la incógnita: se prueba primero hr <= 10 m
            base = 20 * np.log10(f) + 40 * np.log10(d) - 20 * np.log10(ht) - pl
            hr_bajo = 10 ** ((76.3 + base) / 10)
            return hr_bajo if hr_bajo <= 10 + 1e-9 else 10 ** ((85.9 + base) / 20)

        K, a = constantes(hr)

        if sel == "Frecuencia (MHz)":
            return 10 ** ((pl - K - 40 * np.log10(d) + 20 * np.log10(ht) + a * np.log10(hr)) / 20)

        if sel == "Altura antena transmisora (m)":
            return 10 ** ((K + 20 * np.log10(f) + 40 * np.log10(d) - a * np.log10(hr) - pl) / 20)

        if sel == "Distancia (km)":
            return 10 ** ((pl - K - 20 * np.log10(f) + 20 * np.log10(ht) + a * np.log10(hr)) / 40)

        if sel == "Pérdida (dB)":
            return K + 20 * np.log10(f) + 40 * np.log10(d) - 20 * np.log10(ht) - a * np.log10(hr)
