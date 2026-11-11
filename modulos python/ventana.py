"""Aquí se configura la ventana: un fondo líquido con paneles de vidrio encima.

El fondo y los paneles son imágenes dibujadas sobre un Canvas (ver vidrio.py).
Los widgets de siempre (etiquetas, cajas, botones) viven dentro de marcos
ancla (`anfitriones`) que se colocan sobre cada panel.
"""

import os
import tkinter as tk

import customtkinter as ctk
from PIL import ImageTk

import estilos
import vidrio

ANCHO, ALTO = 1200, 744

# Paneles de vidrio: (x, y, ancho, alto) en px lógicos
PANEL_LATERAL = (24, 24, 320, 696)
PANEL_FORMULARIO = (368, 24, 808, 550)
PANEL_RESULTADO = (368, 598, 808, 122)
RADIO = 30


class VentanaApp:
    """Crea y maneja la ventana principal de la app"""

    def __init__(self):
        """Dibuja el fondo y los paneles y crea los marcos donde va cada parte de la interfaz"""

        self.app = ctk.CTk(fg_color=estilos.MEDIANOCHE)  # Inicializa la ventana
        self.app.geometry(f"{ANCHO}x{ALTO}")  # Tamaño de la ventana ancho x alto
        self.app.resizable(False, False)  # Fija el tamaño de la ventana
        self.app.title("MODELTEC")  # Titulo de la ventana
        # Definicmos q el icono esta en la misma ruta que el proyecto
        self.ruta_icono = os.path.join(os.path.dirname(__file__), "Marca_PersonalCirculo.ico")
        self.app.iconbitmap(self.ruta_icono)  # Modifica el icono de la ventana

        # Con pantallas de alta densidad (125 %, 150 %...) las imágenes se dibujan a ese tamaño
        try:
            self.escala = float(self.app._get_window_scaling())
        except Exception:
            self.escala = 1.0

        self._imagenes = []  # Referencias: Tk descarta las imágenes que no se guardan
        self.canvas = tk.Canvas(self.app, highlightthickness=0, bd=0, bg=estilos.MEDIANOCHE)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        fondo = vidrio.fondo(ANCHO, ALTO, self.escala)
        self._poner_imagen(fondo, 0, 0)

        for panel in (PANEL_LATERAL, PANEL_FORMULARIO, PANEL_RESULTADO):
            x, y, w, h = panel
            tarjeta = vidrio.tarjeta(w, h, RADIO, (x, y), fondo, self.escala)
            self._poner_imagen(tarjeta, x - vidrio.MARGEN, y - vidrio.MARGEN)

        # ---- Panel lateral: nombre de la app y modelos
        self.columna_izquierda = self._anfitrion(PANEL_LATERAL)
        self.frame_nombre = ctk.CTkFrame(self.columna_izquierda, fg_color="transparent", corner_radius=0)
        self.frame_nombre.pack(fill="x")
        self.frame_opciones = ctk.CTkFrame(self.columna_izquierda, fg_color="transparent", corner_radius=0)
        self.frame_opciones.pack(fill="both", expand=True)

        # ---- Panel del formulario: título, fórmula, menú, entradas y botón
        self.columna_derecha = self._anfitrion(PANEL_FORMULARIO)
        self.columna_derecha.grid_columnconfigure(0, weight=1)
        self.columna_derecha.grid_rowconfigure(3, weight=1)  # Las entradas ocupan el espacio sobrante

        def fila(numero):
            marco = ctk.CTkFrame(self.columna_derecha, fg_color="transparent", corner_radius=0)
            marco.grid(row=numero, column=0, sticky="nsew")
            return marco

        self.frame_titulo = fila(0)
        self.frame_formula = fila(1)
        self.frame_OptionMenu = fila(2)
        self.frame_inputs = fila(3)
        self.frame_boton = fila(4)

        # ---- Panel del resultado
        self.columna_resultado = self._anfitrion(PANEL_RESULTADO)
        self.frame_resultados = ctk.CTkFrame(self.columna_resultado, fg_color="transparent", corner_radius=0)
        self.frame_resultados.pack(fill="both", expand=True)

    def _poner_imagen(self, imagen_pil, x, y):
        """Coloca una imagen en el Canvas (x, y en px lógicos)."""
        foto = ImageTk.PhotoImage(imagen_pil)
        self._imagenes.append(foto)
        self.canvas.create_image(round(x * self.escala), round(y * self.escala), image=foto, anchor="nw")

    def _anfitrion(self, panel):
        """Marco de color liso colocado sobre un panel, dentro de su franja de vidrio."""
        x, y, w, h = panel
        borde = vidrio.EDGE
        marco = ctk.CTkFrame(self.canvas, width=w - 2 * borde, height=h - 2 * borde,
                             fg_color=estilos.VIDRIO, corner_radius=0)
        marco.pack_propagate(False)
        marco.grid_propagate(False)
        self.canvas.create_window(round((x + borde) * self.escala), round((y + borde) * self.escala),
                                  window=marco, anchor="nw")
        return marco

    def iniciar(self):
        """Permite ejecutar la ventana"""
        self.app.mainloop()
