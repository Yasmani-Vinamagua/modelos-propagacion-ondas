"""Aqui se describen los estilos de la app"""

import customtkinter as ctk


def cargar_fuentes():
    """Función para cargar las fuentes (solo se debe llamar después de crear la app CTk)"""

    # Tipografía y pesos
    return {
        "h1":ctk.CTkFont(family="Montserrat", size=24, weight="bold"),
        "h2": ctk.CTkFont(family="Montserrat", size=20, weight="bold"),
        "h3": ctk.CTkFont(family="Montserrat", size=18, weight="bold"),
        "text_resalt": ctk.CTkFont(family="Montserrat", size=16, weight="bold"),
        "text": ctk.CTkFont(family="Montserrat", size=16, weight="normal")
    }



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
