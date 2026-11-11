"""Pruebas de los 6 modelos de propagación."""

import math

import pytest

from mod_okumura import Okumura
from mod_costhata import COSTHata
from mod_walfisch import Walfisch
from mod_costwalfisch import COSTWalfisch
from mod_egli import Egli
from mod_log import Log
from modelo_base import unidad_de

log = math.log10

CASOS = {
    "okumura": (Okumura, "Pérdida (dB)", {
        "Frecuencia (MHz)": 900, "Altura antena base (m)": 50, "Distancia (km)": 5,
        "Corrección por altura del receptor": 1.2}),
    "costhata": (COSTHata, "Pérdida (dB)", {
        "Frecuencia (MHz)": 1800, "Altura antena base (m)": 50,
        "Corrección por altura del receptor": 1.2, "Distancia (km)": 5,
        "Constante C (dB)": 3}),
    "walfisch": (Walfisch, "Pérdida (dB)", {
        "Pérdida en espacio libre L₀ (dB)": 80,
        "Pérdida por techo a calle Lᵣₜₛ (dB)": 20,
        "Pérdida por múltiples difracciones Lₘₛd (dB)": 15}),
    "costwalfisch": (COSTWalfisch, "Pérdida (dB)", {
        "Frecuencia (MHz)": 900, "Distancia (km)": 1}),
    "egli_hr_bajo": (Egli, "Pérdida (dB)", {
        "Frecuencia (MHz)": 900, "Altura antena transmisora (m)": 50,
        "Altura antena receptora (m)": 2, "Distancia (km)": 5}),
    "egli_hr_10": (Egli, "Pérdida (dB)", {
        "Frecuencia (MHz)": 900, "Altura antena transmisora (m)": 50,
        "Altura antena receptora (m)": 10, "Distancia (km)": 5}),
    "egli_hr_alto": (Egli, "Pérdida (dB)", {
        "Frecuencia (MHz)": 900, "Altura antena transmisora (m)": 50,
        "Altura antena receptora (m)": 30, "Distancia (km)": 5}),
    "log": (Log, "Pérdida (dB)", {
        "Pérdida a distancia d₀ (PL(d₀))": 40, "Distancia d₀ (km)": 0.1,
        "Distancia d (km)": 2, "Exponente de pérdida (n)": 3,
        "Variación Xσ (dB)": 4}),
}


@pytest.mark.parametrize("nombre", CASOS)
def test_despejar_recupera_cada_variable(nombre, ejecutar):
    """Calcula la pérdida y despeja cada variable: debe volver al valor original."""
    clase, clave_pl, entradas = CASOS[nombre]
    _, pl = ejecutar(clase, clave_pl, entradas)

    for variable, esperado in entradas.items():
        valores = {**entradas, clave_pl: pl}
        retorno, obtenido = ejecutar(clase, variable, valores)
        assert retorno is not False, variable
        assert obtenido == pytest.approx(esperado, rel=1e-9), variable


# Valores de referencia calculados a mano, con las fórmulas escritas aparte del código.

def test_okumura_hata_valor_de_referencia(ejecutar):
    _, pl = ejecutar(*CASOS["okumura"])
    esperado = 69.55 + 26.16 * log(900) - 13.82 * log(50) - 1.2 + (44.9 - 6.55 * log(50)) * log(5)
    assert pl == pytest.approx(esperado)


def test_cost_hata_valor_de_referencia(ejecutar):
    _, pl = ejecutar(*CASOS["costhata"])
    esperado = 46.3 + 33.9 * log(1800) - 13.82 * log(50) - 1.2 + (44.9 - 6.55 * log(50)) * log(5) + 3
    assert pl == pytest.approx(esperado)


def test_cost_walfisch_los_valor_de_referencia(ejecutar):
    _, pl = ejecutar(*CASOS["costwalfisch"])
    assert pl == pytest.approx(42.6 + 26 * log(1) + 20 * log(900))


def test_walfisch_suma_de_terminos(ejecutar):
    _, pl = ejecutar(*CASOS["walfisch"])
    assert pl == 115


def test_log_normal_valor_de_referencia(ejecutar):
    _, pl = ejecutar(*CASOS["log"])
    assert pl == pytest.approx(40 + 10 * 3 * log(2 / 0.1) + 4)


@pytest.mark.parametrize("hr, k, a", [(2, 76.3, 10), (10, 76.3, 10), (30, 85.9, 20)])
def test_egli_constante_segun_altura_receptora(hr, k, a, ejecutar):
    entradas = {**CASOS["egli_hr_bajo"][2], "Altura antena receptora (m)": hr}
    _, pl = ejecutar(Egli, "Pérdida (dB)", entradas)
    esperado = k + 20 * log(900) + 40 * log(5) - 20 * log(50) - a * log(hr)
    assert pl == pytest.approx(esperado)


# Validación: un dato malo marca el campo, explica el motivo y aborta el cálculo.

def test_valor_fuera_de_rango_marca_el_campo(ejecutar):
    clase, clave_pl, entradas = CASOS["okumura"]
    retorno, _ = ejecutar(clase, clave_pl, {**entradas, "Frecuencia (MHz)": 5000})
    modelo = ejecutar.ultimo
    assert retorno is False
    assert list(modelo.errores) == ["Frecuencia (MHz)"]
    assert modelo.errores["Frecuencia (MHz)"] == "Fuera de rango. Entre 150 y 1500 MHz"
    assert modelo.mensajes[0].configure.call_args.kwargs["text"] == modelo.errores["Frecuencia (MHz)"]


@pytest.mark.parametrize("nombre", ["okumura", "costhata", "walfisch", "costwalfisch", "egli_hr_bajo", "log"])
def test_texto_no_numerico_marca_el_campo(nombre, ejecutar):
    clase, clave_pl, entradas = CASOS[nombre]
    primera = next(iter(entradas))
    retorno, _ = ejecutar(clase, clave_pl, {**entradas, primera: "abc"})
    assert retorno is False
    assert list(ejecutar.ultimo.errores) == [primera]
    assert ejecutar.ultimo.errores[primera].startswith("Escribe un número")


def test_campo_vacio_pide_el_dato(ejecutar):
    clase, clave_pl, entradas = CASOS["okumura"]
    retorno, _ = ejecutar(clase, clave_pl, {**entradas, "Distancia (km)": "  "})
    assert retorno is False
    assert ejecutar.ultimo.errores["Distancia (km)"] == "Falta este dato. Entre 1 y 20 km"


def test_se_marcan_todos_los_campos_con_error_a_la_vez(ejecutar):
    clase, clave_pl, entradas = CASOS["okumura"]
    retorno, _ = ejecutar(clase, clave_pl, {**entradas, "Frecuencia (MHz)": 5000, "Distancia (km)": "x"})
    assert retorno is False
    assert set(ejecutar.ultimo.errores) == {"Frecuencia (MHz)", "Distancia (km)"}


def test_los_errores_se_limpian_al_corregir(ejecutar):
    clase, clave_pl, entradas = CASOS["okumura"]
    ejecutar(clase, clave_pl, {**entradas, "Frecuencia (MHz)": 5000})
    modelo = ejecutar.ultimo
    modelo.entradas[0].valor = 900
    assert modelo.calculo() is True
    assert modelo.errores == {}


def test_campo_sin_rango_no_muestra_ayuda():
    from unittest.mock import MagicMock
    assert Walfisch(MagicMock(), MagicMock()).rango_texto("Pérdida (dB)") == ""


def test_division_entre_cero_va_al_error_general(ejecutar):
    """Log-Normal con d = d₀ no permite despejar n (log 1 = 0): debe avisar, no mostrar inf."""
    entradas = {**CASOS["log"][2], "Distancia d (km)": 0.1, "Pérdida (dB)": 50}
    retorno, _ = ejecutar(Log, "Exponente de pérdida (n)", entradas)
    assert retorno is False
    assert ejecutar.ultimo.errores == {}
    assert "división entre cero" in ejecutar.ultimo.error_general


def test_coma_decimal_se_acepta(ejecutar):
    clase, clave_pl, entradas = CASOS["okumura"]
    con_coma = {**entradas, "Corrección por altura del receptor": "1,2"}
    retorno, pl = ejecutar(clase, clave_pl, con_coma)
    assert retorno is True
    assert pl == pytest.approx(ejecutar(clase, clave_pl, entradas)[1])


@pytest.mark.parametrize("clase", [Okumura, COSTHata, Walfisch, COSTWalfisch, Egli, Log])
def test_opcion_por_defecto_es_la_pérdida(clase):
    from unittest.mock import MagicMock
    modelo = clase(MagicMock(), MagicMock())
    assert modelo.defecto == "Pérdida (dB)"


@pytest.mark.parametrize("nombre, unidad", [
    ("Frecuencia (MHz)", "MHz"),
    ("Altura antena receptora (m)", "m"),
    ("Distancia (km)", "km"),
    ("Pérdida (dB)", "dB"),
    ("Pérdida (dB)", "dB"),
    ("Pérdida a distancia d₀ (PL(d₀))", "dB"),
    ("Corrección por altura del receptor", "dB"),
    ("Variación Xσ (dB)", "dB"),
    ("Exponente de pérdida (n)", ""),
])
def test_unidad_del_resultado(nombre, unidad):
    assert unidad_de(nombre) == unidad
