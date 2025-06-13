import customtkinter as ctk
import numpy as np
import estilos
from error import VentanaError

app = ctk.CTk()

fuentes = estilos.cargar_fuentes() #Se llama a la funcion q tiene el diccionario de fuentes

class COSTWalfisch:

    def __init__(self, frame_inputs, frame_OptionMenu):
        self.frame_OptionMenu = frame_OptionMenu
        self.frame_inputs = frame_inputs

        self.operacion = 0.00

        self.valores = {} # Creamos una lista para almacenar los datos del input

        self.var_costwalfisch = {
            "Frecuencia (MHz)": (800, 2000, "Frecuencia (f) entre 800-2000 MHz"),
            "Distancia (Km)": (0.02, 5, "Distancia (d) entre 0.02-5 Km"),
            "Perdida (dB)": (0, 0, "Ingrese la pérdida (PL)")
        }

        self.list_menu = list(self.var_costwalfisch.keys())  # Opciones de cálculo modelo costwalfisch

        self.entradas_costwalfisch = []  # Lista para guardar los imputs del modelo costwalfisch


    def menu(self):

        # Menú de opciones para modelo okomura
        self.optionmenu = ctk.StringVar(value=self.list_menu[0])
        self.optioncostwalfisch = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=self.optionmenu,
                                             width=250, height=30,
                                             command= self.inputs) #cada vez que el usuario cambia la selección,
        # se llama automáticamente a la función inputs pasando el valor seleccionado como argumento.
        self.optioncostwalfisch.grid(padx=32, pady=5)

        self.inputs(self.list_menu[0]) #Llama a la funcion inputs por primera vez para mostrar los inputs de la primera opción al cargar la interfaz por defecto.


    #Entradas del modelo costwalfisch
    def inputs(self, seleccion):

        self.seleccion_modelo = seleccion #Guarda el valor seleccionado del menú

        # Limpiar todos los inputs
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        self.entradas_costwalfisch.clear()

        fila = 0

        # Genera los labels e Imputs del modelo
        for self.variable in self.list_menu:
            if self.seleccion_modelo != self.variable: #Si el valor del menu seleccionado es diferente a la lista de opciones imprime

                self.label_costwalfisch = ctk.CTkLabel(self.frame_inputs, text=self.variable, text_color="black", font=fuentes["text_resalt"])
                self.label_costwalfisch.grid(row=fila, column=0,**estilos.pad_labels)

                self.in_costwalfisch = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                               placeholder_text=self.var_costwalfisch[self.variable][2], #Imprimer de la lista de var_costwalfisch[key][item]
                                          font=fuentes["text"])
                self.in_costwalfisch.grid(row=fila, column=1,**estilos.pad_inputs)

                self.entradas_costwalfisch.append(self.in_costwalfisch)  # Almacenamos los imputs en una lista

            fila += 1

    #Calculo de variables
    def calculo(self):

        #Refrescamos los valores
        self.valores.clear()
        self.operacion = 0

        variables = [v for v in self.list_menu if v != self.seleccion_modelo] #Generamos una lista con todas las variables menos la seleccionada

        for nombre_variable, entrada in zip(variables, self.entradas_costwalfisch): #Asosiamos cada nombre de variable con su valor ingresado

            try:
                self.valor = float(entrada.get()) #Covertimos cada valor ingresado en un float

                min_val, max_val, _ = self.var_costwalfisch[nombre_variable]

                if min_val !=0 or max_val!=0: #Evitar validar aquellas variables q no tienen rango como a(hm) o pl
                    if not min_val <= self.valor <= max_val:
                        VentanaError(app) #Valor fuera del rango lanza pantalla error

                self.valores[nombre_variable] = self.valor #Creamos un diccionario con cada nombre variable y float ingresado

            except ValueError:
                self.valores[nombre_variable] = None #Si se ingresa otro valor q no sea numerico se llena con un None

        if None in self.valores.values():
            return VentanaError(app) #Si existe un valor none en valores{} lanza la ventana de error

        f = self.valores.get("Frecuencia (MHz)")
        d = self.valores.get("Distancia (Km)")
        pl = self.valores.get("Perdida (dB)")


        # Evalúa cada opción de cálculo del modelo costwalfisch
        if self.seleccion_modelo == "Frecuencia (MHz)":
            self.operacion = 10 ** ((pl - 42.6 - 26 * np.log10(d)) / 20)

        elif self.seleccion_modelo == "Distancia (Km)":
            self.operacion = 10 ** ((pl - 42.6 - 20 * np.log10(f)) / 26)

        elif self.seleccion_modelo == "Perdida (dB)":
            self.operacion = 42.6 + 26 * np.log10(d) + 20 * np.log10(f)