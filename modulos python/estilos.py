"""Aqui se describen los estilos de la app"""

import os

import customtkinter as ctk

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
        "h1":ctk.CTkFont(family="Montserrat", size=24, weight="bold"),
        "h2": ctk.CTkFont(family="Montserrat", size=20, weight="bold"),
        "h3": ctk.CTkFont(family="Montserrat", size=18, weight="bold"),
        "text_resalt": ctk.CTkFont(family="Montserrat", size=16, weight="bold"),
        "text": ctk.CTkFont(family="Montserrat", size=16, weight="normal"),
        "small": ctk.CTkFont(family="Montserrat", size=13, weight="normal")
    }


# Colores de la validación (contraste mínimo 4.5:1 sobre el gris #D9D9D9 del panel)
color_primario = "#3C4E99"  # Azul de la barra lateral
color_primario_oscuro = "#2F3E7A"
ancho_etiquetas = 290  # Ancho de la columna de etiquetas del formulario
color_error = "#B00020"
color_ayuda = "#555555"



estilo_boton_modelo = {
    "width": 302,
    "height": 33,
    "corner_radius": 8,
    "border_width": 1,
    "border_color": "black",
    "text_color": "black",
    "text_color_disabled": "white",
    "fg_color": "#E1F7FA",
    "hover_color":"#C3E1EB",
    "font": ('Montserrat', 18, 'bold')
}

estilo_boton_calcular = {
    "width": 302,
    "height": 33,
    "corner_radius": 8,
    "border_width": 1,
    "border_color": "black",
    "text_color": "black",
    "text_color_disabled": "white",
    "fg_color": "#E88C0C",
    "hover_color":"#FF9605",
    "font": ('Montserrat', 18, 'bold')
}

#Diccionario con configuraciones de las filas
der_grid = {"column":0,
            "columnspan":2,
            "padx":0,
            "pady":0,
            "sticky":"nsew"}

#Propiedades basicas de los entry
pad_inputs = {"padx":(2, 32),
             "pady":10,
              "sticky":"w"} #Se alinea a la derecha

#Propiedades basicas de los labels
pad_labels = {"padx":(32, 2),
             "pady":(10,15),
              "sticky":"w"} #Se alinea a la derecha

#Propiedades basicas del resultado
pad_result = {"padx":(32, 32),
             "pady":(5,5),
              "sticky":"w"} #Se alinea a la derecha


ancho_inputs = 400 #Ancho de las cajas de entry
