"""Modelo Walfisch-Ikegami (PL = L₀ + Lᵣₜₛ + Lₘₛd)"""

from modelo_base import ModeloBase


class Walfisch(ModeloBase):

    variables = {
        "Pérdida (dB)": (0, 0, "Pérdida total (PL) en dB"),
        "Pérdida en espacio libre L₀ (dB)": (0, 0, "Pérdida en espacio libre (L₀)"),
        "Pérdida por techo a calle Lᵣₜₛ (dB)": (0, 0, "Pérdida de techo a calle (Lᵣₜₛ)"),
        "Pérdida por múltiples difracciones Lₘₛd (dB)": (0, 0, "Pérdida por múltiples difracciones (Lₘₛd)"),
    }

    def calcular(self, v):
        PL = v.get("Pérdida (dB)")
        L0 = v.get("Pérdida en espacio libre L₀ (dB)")
        Lrts = v.get("Pérdida por techo a calle Lᵣₜₛ (dB)")
        Lmsd = v.get("Pérdida por múltiples difracciones Lₘₛd (dB)")

        sel = self.seleccion_modelo

        if sel == "Pérdida (dB)":
            return L0 + Lrts + Lmsd

        if sel == "Pérdida en espacio libre L₀ (dB)":
            return PL - Lrts - Lmsd

        if sel == "Pérdida por techo a calle Lᵣₜₛ (dB)":
            return PL - L0 - Lmsd

        if sel == "Pérdida por múltiples difracciones Lₘₛd (dB)":
            return PL - L0 - Lrts
