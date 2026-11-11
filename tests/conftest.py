"""Prepara el entorno para probar los modelos sin abrir ventanas.

Se sustituye customtkinter por un simulado y las cajas de texto por objetos que
solo guardan su texto. Los errores de validación se leen de modelo.errores.
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

RUTA = os.path.join(os.path.dirname(__file__), "..", "modulos python")
sys.path.insert(0, os.path.abspath(RUTA))

sys.modules["customtkinter"] = MagicMock()

class Entrada:
    """Imita un CTkEntry: solo expone get()."""

    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return str(self.valor)

    def configure(self, **opciones):
        self.opciones = opciones


@pytest.fixture
def ejecutar():
    """ejecutar(Clase, opcion_a_despejar, {variable: valor}) -> (retorno, resultado)"""

    def _ejecutar(clase, seleccion, valores):
        modelo = clase(MagicMock(), MagicMock())
        modelo.seleccion_modelo = seleccion
        entradas = [Entrada(valores[n]) for n in modelo.list_menu if n != seleccion]
        modelo.entradas = entradas
        modelo.mensajes = [MagicMock() for _ in entradas]
        _ejecutar.ultimo = modelo  # Para que las pruebas lean modelo.errores
        retorno = modelo.calculo()
        return retorno, modelo.operacion

    return _ejecutar
