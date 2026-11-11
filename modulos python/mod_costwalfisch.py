"""Modelo COST-231 Walfisch-Ikegami (caso con línea de vista)"""

import numpy as np

from modelo_base import ModeloBase


class COSTWalfisch(ModeloBase):

    variables = {
        "Frecuencia (MHz)": (800, 2000, "Frecuencia (f) entre 800-2000 MHz"),
        "Distancia (km)": (0.02, 5, "Distancia (d) entre 0.02-5 km"),
        "Pérdida (dB)": (0, 0, "Ingrese la pérdida (PL)"),
    }

    def calcular(self, v):
        f = v.get("Frecuencia (MHz)")
        d = v.get("Distancia (km)")
        pl = v.get("Pérdida (dB)")

        sel = self.seleccion_modelo

        if sel == "Frecuencia (MHz)":
            return 10 ** ((pl - 42.6 - 26 * np.log10(d)) / 20)

        if sel == "Distancia (km)":
            return 10 ** ((pl - 42.6 - 20 * np.log10(f)) / 26)

        if sel == "Pérdida (dB)":
            return 42.6 + 26 * np.log10(d) + 20 * np.log10(f)
