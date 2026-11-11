"""Aqui se describen los estilos de la app.

La paleta es la del manual de identidad (paleta/paleta.md, v1.1). Los tonos de
"vidrio" no son colores nuevos: son el blanco con transparencia sobre el fondo,
mezclados aquí con anticipación porque los widgets de Tk no admiten alfa.
"""

import os

import customtkinter as ctk

# ---------- Paleta de marca ----------
AZUL_MARINO = "#223367"  # principal
ROSA = "#FF1563"         # acento firma (10 % o menos)
MEDIANOCHE = "#0D1530"   # fondos oscuros
PIZARRA = "#5B6478"      # texto secundario (sobre claro)
NIEBLA = "#F2F4F8"       # fondos claros
BLANCO = "#FFFFFF"
LINEA = "#E3E7F0"        # solo decorativo
BRUMA = "#C9D0E6"        # solo decorativo


def mezclar(color_a, color_b, t):
    """Mezcla dos colores HEX: t = 0 da color_a y t = 1 da color_b."""
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * (1 - t) + y * t):02X}" for x, y in zip(a, b))


# ---------- Vidrio (blanco con transparencia sobre el fondo) ----------
VIDRIO = mezclar(mezclar(MEDIANOCHE, AZUL_MARINO, 0.55), BLANCO, 0.07)  # interior de los paneles
VIDRIO_BOTON = mezclar(VIDRIO, BLANCO, 0.10)    # botones en reposo
VIDRIO_HOVER = mezclar(VIDRIO, BLANCO, 0.20)    # botones con el cursor encima
VIDRIO_BORDE = mezclar(VIDRIO, BLANCO, 0.28)    # borde fino de los botones
ROSA_HOVER = mezclar(ROSA, BLANCO, 0.12)

# ---------- Roles ----------
color_texto = BLANCO               # texto principal sobre vidrio (contraste > 10:1)
color_ayuda = NIEBLA               # texto de apoyo sobre vidrio
color_error = ROSA                 # el manual aún no define un color de error: se usa el acento
color_campo = NIEBLA               # relleno de las cajas de texto
color_campo_texto = MEDIANOCHE
color_campo_placeholder = PIZARRA  # 5,39:1 sobre Niebla
color_foco = ROSA

# Medidas (px lógicos; customtkinter los escala con el DPI)
ancho_etiquetas = 270  # Ancho de la columna de etiquetas del formulario
ancho_inputs = 360     # Ancho de las cajas de entry

RUTA_FUENTES = os.path.join(os.path.dirname(__file__), "fuentes")
_fuentes_cargadas = False


def registrar_fuentes():
    """Registra Montserrat desde la carpeta del proyecto, para que no dependa de que esté instalada.

    En sistemas donde customtkinter no puede cargar fuentes (macOS) se usa la instalada o una de reemplazo.
    """
    global _fuentes_cargadas
    if _fuentes_cargadas:
        return
    _fuentes_cargadas = True
    for archivo in ("Montserrat-Regular.ttf", "Montserrat-Bold.ttf"):
        ruta = os.path.join(RUTA_FUENTES, archivo)
        if os.path.exists(ruta):
            ctk.FontManager.load_font(ruta)


def cargar_fuentes():
    """Función para cargar las fuentes (solo se debe llamar después de crear la app CTk)"""

    registrar_fuentes()

    # Tipografía y pesos
    return {
        "h1": ctk.CTkFont(family="Montserrat", size=26, weight="bold"),
        "h2": ctk.CTkFont(family="Montserrat", size=22, weight="bold"),
        "h3": ctk.CTkFont(family="Montserrat", size=18, weight="bold"),
        "resultado": ctk.CTkFont(family="Montserrat", size=38, weight="bold"),
        "text_resalt": ctk.CTkFont(family="Montserrat", size=15, weight="bold"),
        "text": ctk.CTkFont(family="Montserrat", size=15, weight="normal"),
        "small": ctk.CTkFont(family="Montserrat", size=13, weight="normal"),
        "small_negrita": ctk.CTkFont(family="Montserrat", size=13, weight="bold"),
    }


estilo_boton_modelo = {
    "width": 276,
    "height": 40,
    "corner_radius": 20,
    "border_width": 1,
    "border_color": VIDRIO_BORDE,
    "text_color": BLANCO,
    "fg_color": VIDRIO_BOTON,
    "hover_color": VIDRIO_HOVER,
    "font": ("Montserrat", 15, "bold"),
}

# Modelo activo: Niebla con texto Medianoche (16,3:1) y borde rosa
estilo_boton_modelo_activo = {
    "fg_color": NIEBLA,
    "hover_color": NIEBLA,
    "text_color": MEDIANOCHE,
    "border_color": ROSA,
    "border_width": 2,
}

# Blanco sobre rosa: 3,79:1, válido solo para texto grande (aquí 20 px en negrita)
estilo_boton_calcular = {
    "width": 220,
    "height": 46,
    "corner_radius": 23,
    "border_width": 0,
    "text_color": BLANCO,
    "fg_color": ROSA,
    "hover_color": ROSA_HOVER,
    "font": ("Montserrat", 20, "bold"),
}
