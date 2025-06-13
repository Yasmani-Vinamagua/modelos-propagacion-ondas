import customtkinter as ctk
import numpy as np
import estilos
from error import VentanaError

app = ctk.CTk()

fuentes = estilos.cargar_fuentes() #Se llama a la funcion q tiene el diccionario de fuentes

class Egli:

    def __init__(self, frame_inputs, frame_OptionMenu):
        self.frame_OptionMenu = frame_OptionMenu
        self.frame_inputs = frame_inputs

        self.operacion = 0.00

        self.valores = {} # Creamos una lista para almacenar los datos del input

        self.var_egli = {
            "Frecuencia (MHz)": (30, 3000, "Frecuencia (f) entre 30-3000 MHz"),
            "Altura antena base (m)": (3, 200, "Altura antena base (hb) entre 3-200 m"),
            "Altura antena móvil (m)": (1, 10, "Altura antena móvil (hm) entre 1-10 m"),
            "Distancia (Km)": (0.1, 20, "Distancia (d) entre 0.1-20 Km"),
            "Perdida (dB)": (0, 0, "Ingrese la pérdida (PL)")
        }

        self.list_menu = list(self.var_egli.keys())  # Opciones de cálculo modelo egli

        self.entradas_egli = []  # Lista para guardar los imputs del modelo egli


    def menu(self):

        # Menú de opciones para modelo okomura
        self.optionmenu = ctk.StringVar(value=self.list_menu[0])
        self.optionegli = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=self.optionmenu,
                                             width=250, height=30,
                                             command= self.inputs) #cada vez que el usuario cambia la selección,
        # se llama automáticamente a la función inputs pasando el valor seleccionado como argumento.
        self.optionegli.grid(padx=32, pady=5)

        self.inputs(self.list_menu[0]) #Llama a la funcion inputs por primera vez para mostrar los inputs de la primera opción al cargar la interfaz por defecto.


    #Entradas del modelo egli
    def inputs(self, seleccion):

        self.seleccion_modelo = seleccion #Guarda el valor seleccionado del menú

        # Limpiar todos los inputs
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        self.entradas_egli.clear()

        fila = 0

        # Genera los labels e Imputs del modelo
        for self.variable in self.list_menu:
            if self.seleccion_modelo != self.variable: #Si el valor del menu seleccionado es diferente a la lista de opciones imprime

                self.label_egli = ctk.CTkLabel(self.frame_inputs, text=self.variable, text_color="black", font=fuentes["text_resalt"])
                self.label_egli.grid(row=fila, column=0,**estilos.pad_labels)

                self.in_egli = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                               placeholder_text=self.var_egli[self.variable][2], #Imprimer de la lista de var_egli[key][item]
                                          font=fuentes["text"])
                self.in_egli.grid(row=fila, column=1,**estilos.pad_inputs)

                self.entradas_egli.append(self.in_egli)  # Almacenamos los imputs en una lista

            fila += 1

    #Calculo de variables
    def calculo(self):

        #Refrescamos los valores
        self.valores.clear()
        self.operacion = 0

        variables = [v for v in self.list_menu if v != self.seleccion_modelo] #Generamos una lista con todas las variables menos la seleccionada

        for nombre_variable, entrada in zip(variables, self.entradas_egli): #Asosiamos cada nombre de variable con su valor ingresado

            try:
                self.valor = float(entrada.get()) #Covertimos cada valor ingresado en un float

                min_val, max_val, _ = self.var_egli[nombre_variable]

                if min_val !=0 or max_val!=0: #Evitar validar aquellas variables q no tienen rango como a(hm) o pl
                    if not (min_val <= self.valor <= max_val):
                        VentanaError(app) #Valor fuera del rango lanza pantalla error

                self.valores[nombre_variable] = self.valor #Creamos un diccionario con cada nombre variable y float ingresado

            except ValueError:
                self.valores[nombre_variable] = None #Si se ingresa otro valor q no sea numerico se llena con un None

        if None in self.valores.values():
            return VentanaError(app) #Si existe un valor none en valores{} lanza la ventana de error

        f = self.valores.get("Frecuencia (MHz)")
        hb = self.valores.get("Altura antena base (m)")
        hm = self.valores.get("Altura antena móvil (m)")
        d = self.valores.get("Distancia (Km)")
        pl = self.valores.get("Perdida (dB)")


        # Evalúa cada opción de cálculo del modelo egli
        if self.seleccion_modelo == "Frecuencia (MHz)":
            self.operacion = 10 ** ((pl - 117 - 40 * np.log10(d) + 20 * np.log10(hb * hm)) / 20)

        elif self.seleccion_modelo == "Altura antena base (m)":
            producto = 10 ** ((pl - 117 - 40 * np.log10(d) - 20 * np.log10(f)) / -20)
            self.operacion = producto / hm

        elif self.seleccion_modelo == "Altura antena móvil (m)":
            producto = 10 ** ((pl - 117 - 40 * np.log10(d) - 20 * np.log10(f)) / -20)
            self.operacion = producto / hb

        elif self.seleccion_modelo == "Distancia (Km)":
            self.operacion = 10 ** ((pl - 117 + 20 * np.log10(hb * hm) - 20 * np.log10(f)) / 40)

        elif self.seleccion_modelo == "Perdida (dB)":
            self.operacion = 117 + 40 * np.log10(d) - 20 * np.log10(hb * hm) + 20 * np.log10(f)