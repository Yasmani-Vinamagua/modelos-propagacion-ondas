"""Cálculo del modelo costhata"""

import customtkinter as ctk
import numpy as np
import estilos
from error import VentanaError

app = ctk.CTk()

#Se llama a la funcion q tiene el diccionario de fuentes
fuentes = estilos.cargar_fuentes()

class COSTHata:
    """Maneja todo el cáclulo del modelo"""

    def __init__(self, frame_inputs, frame_OptionMenu):
        """Recibe los frames y almacena variables para el cálculo"""

        # Importamos el frame del menu
        self.frame_OptionMenu = frame_OptionMenu
        # Importamos el frame del input
        self.frame_inputs = frame_inputs

        # Variable para almacenar la opcion escogida
        self.seleccion_modelo = None

        self.operacion = 0.00

        # Creamos una lista para almacenar los datos del input
        self.valores = {}

        self.var_COSTHata = {
            "Frecuencia (MHz)": (1500, 2000, "Frecuencia (f) entre 1500-2000 MHz"),
            "Altura antena base (m)": (30, 200, "Altura antena base (hb) entre 30-200 m"),
            "Corrección por altura del receptor": (0,0,"a(hm)"),
            "Distancia (Km)": (1, 20, "Distancia (d) entre 1-20 Km"),
            "Constante C (dB)": (0, 3, "Constante C: 0 para rural, 3 para urbano"),
            "Perdida (dB)": (0, 0, "Perdida calculada (PL)")
        }

        # Opciones de cálculo modelo COSTHata
        self.list_menu = list(self.var_COSTHata.keys())

        # Lista para guardar los imputs del modelo COSTHata
        self.entradas_COSTHata = []


    def menu(self):
        """Maneja el menú de opciones del modelo"""

        # Menú de opciones para modelo okomura
        optionmenu = ctk.StringVar(value=self.list_menu[0])
        optionCOSTHata = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=optionmenu,
                                             width=250, height=30,
                                           # cada vez que el usuario cambia la selección,
                                           # se llama automáticamente a la función inputs pasando el
                                           # valor seleccionado como argumento.
                                             command= self.inputs)
        optionCOSTHata.grid(padx=32, pady=5)

        # Llama a la funcion inputs por primera vez para mostrar los
        # inputs de la primera opción al cargar la interfaz por defecto.
        self.inputs(self.list_menu[0])


    def inputs(self, seleccion):
        """Genera y almacena todas las entradas del modelo"""

        self.seleccion_modelo = seleccion #Guarda el valor seleccionado del menú

        # Limpiar todos los inputs
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        self.entradas_COSTHata.clear()

        fila = 0

        # Genera los labels e Imputs del modelo
        for variable in self.list_menu:
            # Si el valor del menu seleccionado es diferente a la lista de opciones imprime
            if self.seleccion_modelo != variable:

                label_COSTHata = ctk.CTkLabel(self.frame_inputs,
                                                   text=variable,
                                                   text_color="black",
                                                   font=fuentes["text_resalt"])
                label_COSTHata.grid(row=fila, column=0,**estilos.pad_labels)

                in_COSTHata = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                           # Imprime de la lista de var_COSTHata[key][item]
                                            placeholder_text=self.var_COSTHata[variable][2],
                                          font=fuentes["text"])
                in_COSTHata.grid(row=fila, column=1,**estilos.pad_inputs)

                # Almacenamos los imputs en una lista
                self.entradas_COSTHata.append(in_COSTHata)

            fila += 1


    def calculo(self):
        """Realiza el cálculo del modelo y sus derivadas"""

        #Refrescamos los valores
        self.valores.clear()
        self.operacion = 0

        # Generamos una lista con todas las variables menos la seleccionada
        variables = [v for v in self.list_menu if v != self.seleccion_modelo]

        # Asosiamos cada nombre de variable con su valor ingresado
        for nombre_variable, entrada in zip(variables, self.entradas_COSTHata):

            try:
                # Covertimos cada valor ingresado en un float
                valor = float(entrada.get())

                #Definimos los min y max de cada input
                min_val, max_val, _ = self.var_COSTHata[nombre_variable]

                # Evitar validar aquellas variables q no tienen rango como a(hm) o pl
                if min_val !=0 or max_val!=0:
                    if not min_val <= valor <= max_val:
                        # Valor fuera del rango lanza pantalla error
                        VentanaError(app)

                # Creamos un diccionario con cada nombre variable y float ingresado
                self.valores[nombre_variable] = valor

            except ValueError:
                # Si se ingresa otro valor q no sea numerico se llena con un None
                self.valores[nombre_variable] = None

        if None in self.valores.values():
            # Si existe un valor none en valores{} lanza la ventana de error
            VentanaError(app)

        # Ingresa el valor de la variable "Frecuencia# se usa un get()
        # para que asigne automaticamente un None al Key, caso contrario salta error.
        f = self.valores.get("Frecuencia (MHz)")
        hb = self.valores.get("Altura antena base (m)")
        d = self.valores.get("Distancia (Km)")
        a_hm = self.valores.get("Corrección por altura del receptor")
        pl = self.valores.get("Perdida (dB)")
        C = self.valores.get("Constante C (dB)")


        # Evalúa cada opción de cálculo del modelo COST-231 Hata
        if self.seleccion_modelo == "Frecuencia (MHz)":

            self.operacion = 10 ** ((pl - 46.3 + 13.82 * np.log10(hb) + a_hm -
                                     (44.9 - 6.55 * np.log10(hb)) * np.log10(d) - C) / 33.9)

        elif self.seleccion_modelo == "Altura antena base (m)":

            self.operacion = 10 ** ((pl - 46.3 - 33.9 * np.log10(f) + a_hm -
                                     (44.9 * np.log10(d)) + C)
                                    / (-13.82 + 6.55 * np.log10(d)))

        elif self.seleccion_modelo == "Altura antena móvil (m)":

            # Inversión de fórmula de a(hm)
            self.operacion = (a_hm + (1.56 * np.log10(f) - 0.8)) / (1.1 * np.log10(f) - 0.7)

        elif self.seleccion_modelo == "Distancia (Km)":

            self.operacion = 10 ** ((pl - 46.3 - 33.9 * np.log10(f) + 13.82 * np.log10(hb) +
                                     a_hm - C) / (44.9 - 6.55 * np.log10(hb)))

        elif self.seleccion_modelo == "Constante C (dB)":

            self.operacion = pl - (46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) - a_hm + (
                        44.9 - 6.55 * np.log10(hb)) * np.log10(d))

        elif self.seleccion_modelo == "Perdida (dB)":

            self.operacion = 46.3 + 33.9 * np.log10(f) - 13.82 * np.log10(hb) - a_hm + (
                        44.9 - 6.55 * np.log10(hb)) * np.log10(d) + C
