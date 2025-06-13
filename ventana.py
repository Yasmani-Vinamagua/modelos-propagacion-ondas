"""Aquí se configura la ventana y grillas de la ventana"""

import customtkinter as ctk
import estilos

class VentanaApp:
    """Crea y maneja la ventana principal de la app"""

    def __init__(self):
        """Manjea toda la distribución de la ventana con grids"""

        self.app = ctk.CTk()  # Inicializa la ventana
        self.app.geometry("1200x744")  # Tamaño de la ventana ancho x alto
        self.app.resizable(False, False)  # Fija el tamaño de la ventana
        self.app.title("MODELTEC")  # Titulo de la ventana
        self.app.iconbitmap("Marca_PersonalCirculo.ico")  # Modifica el icono de la ventana

        # Estructura de la ventana
        self.app.grid_columnconfigure(0, weight=1)  # La columna 0 ocupa 1 parte de la ventana
        self.app.grid_columnconfigure(1, weight=3)  # La columna 1 ocupa 3 partes de la ventana
        self.app.grid_rowconfigure(0, weight=1)  # Las filas coupan toda la ventana

        # Configuramos la Columna izquierda
        self.columna_izquierda = ctk.CTkFrame(master=self.app,  # La columna pertenece a la ventana principal
                                              fg_color="#3C4E99",
                                              corner_radius=0)  # Por defecto el frame tiene un borde redondeado
        self.columna_izquierda.grid(row=0,
                                    column=0,
                                    sticky="nsew")  # La columna se alinea al norte, sur, este y oeste

        # Configuramos las filas de la columna izquierda
        self.columna_izquierda.grid_rowconfigure(0, weight=1)
        self.columna_izquierda.grid_rowconfigure(1, weight=9)
        #Configuración para que filas ocupen todo el ancho de la columna
        self.columna_izquierda.grid_columnconfigure(0, weight=1)

        # Fila 0: Nombre de la App
        self.frame_nombre = ctk.CTkFrame(master=self.columna_izquierda,
                                         fg_color="transparent", corner_radius=0)
        self.frame_nombre.grid(row=0, **estilos.der_grid)

        # Fila 1: Opciones de modelos de propagacion
        self.frame_opciones = ctk.CTkFrame(master=self.columna_izquierda,
                                           fg_color="transparent", corner_radius=0)
        self.frame_opciones.grid(row=1, **estilos.der_grid)

        # Configuramos la Columna derecha
        self.columna_derecha = ctk.CTkFrame(master=self.app,
                                            fg_color="#D9D9D9", corner_radius=0)
        self.columna_derecha.grid(row=0, column=1, sticky="nsew")
        #Configuración para que filas ocupen todo el ancho de la columna
        self.columna_derecha.grid_columnconfigure(0, weight=1)

        # Configurar filas en columna derecha
        for i, tam in enumerate([1, 1, 1, 4, 1, 2]):
            self.columna_derecha.grid_rowconfigure(i, weight=tam)

        # Fila 0: Título
        self.frame_titulo = ctk.CTkFrame(master=self.columna_derecha,
                                         fg_color="transparent", corner_radius=0)
        self.frame_titulo.grid(row=0, **estilos.der_grid)

        # Fila 1: Fórmula
        self.frame_formula = ctk.CTkFrame(master=self.columna_derecha,
                                          fg_color="transparent", corner_radius=0)
        self.frame_formula.grid(row=1, **estilos.der_grid)

        # Fila 2: Menú opciones
        self.frame_OptionMenu = ctk.CTkFrame(master=self.columna_derecha,
                                             fg_color="transparent", corner_radius=0)
        self.frame_OptionMenu.grid(row=2, **estilos.der_grid)

        # Fila 3: Inputs
        self.frame_inputs = ctk.CTkFrame(master=self.columna_derecha,
                                         fg_color="transparent", corner_radius=0)
        self.frame_inputs.grid(row=3, **estilos.der_grid)

        # Fila 4: Boton Calcular
        self.frame_boton = ctk.CTkFrame(master=self.columna_derecha,
                                        fg_color="transparent", corner_radius=0)
        self.frame_boton.grid(row=4, **estilos.der_grid)

        # Fila 5: Resultados
        self.frame_resultados = ctk.CTkFrame(master=self.columna_derecha,
                                             fg_color="transparent", corner_radius=0)
        self.frame_resultados.grid(row=5, **estilos.der_grid)

    def iniciar(self):
        """Permite ejecutar la ventana"""
        self.app.mainloop()
