"""Modelo Log-Normal: PL = PL(d₀) + 10·n·log(d/d₀) + Xσ"""

import numpy as np

from modelo_base import ModeloBase


class Log(ModeloBase):

    variables = {
        "Pérdida a distancia d₀ (PL(d₀))": (0, 200, "Pérdida en d₀ (PL₀) en dB"),
        "Distancia d₀ (km)": (0.01, 1, "Distancia de referencia (d₀) entre 0.01-1 km"),
        "Distancia d (km)": (0.01, 20, "Distancia d entre 0.01-20 km"),
        "Exponente de pérdida (n)": (1, 6, "Exponente n entre 1-6"),
        "Variación Xσ (dB)": (-20, 20, "Variable aleatoria Xσ (normal, en dB)"),
        "Pérdida (dB)": (0, 0, "Ingrese la pérdida total PL"),
    }

    def calcular(self, v):
        pl_d0 = v.get("Pérdida a distancia d₀ (PL(d₀))")
        d0 = v.get("Distancia d₀ (km)")
        d = v.get("Distancia d (km)")
        n = v.get("Exponente de pérdida (n)")
        x_sigma = v.get("Variación Xσ (dB)")
        pl = v.get("Pérdida (dB)")

        sel = self.seleccion_modelo

        if sel == "Pérdida a distancia d₀ (PL(d₀))":
            return pl - 10 * n * np.log10(d / d0) - x_sigma

        if sel == "Distancia d₀ (km)":
            return d / (10 ** ((pl - pl_d0 - x_sigma) / (10 * n)))

        if sel == "Distancia d (km)":
            return d0 * (10 ** ((pl - pl_d0 - x_sigma) / (10 * n)))

        if sel == "Exponente de pérdida (n)":
            return (pl - pl_d0 - x_sigma) / (10 * np.log10(d / d0))

        if sel == "Variación Xσ (dB)":
            return pl - pl_d0 - 10 * n * np.log10(d / d0)

        if sel == "Pérdida (dB)":
            return pl_d0 + 10 * n * np.log10(d / d0) + x_sigma
