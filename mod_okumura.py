import customtkinter as ctk
import numpy as np
import estilos
from error import VentanaError

app = ctk.CTk()

fuentes = estilos.cargar_fuentes() #Se llama a la funcion q tiene el diccionario de fuentes

class Okumura:

    def __init__(self, frame_inputs, frame_OptionMenu):
        self.frame_OptionMenu = frame_OptionMenu
        self.frame_inputs = frame_inputs

        self.operacion = 0.00

        self.valores = {} # Creamos una lista para almacenar los datos del input

        self.var_okumura = {"Frecuencia (MHz)": (150,1500,"Frecuencia (f) entre 150-1500 MHz") ,
                       "Altura antena base (m)": (30,200,"Altura antena base (hb) entre 30-200 m"),
                       "Distancia (Km)": (1,20,"Distancia (d) entre 1-20 Km"),
                       "Corrección por altura del receptor": (0,0,"a(hm)"),
                       "Perdida (dB)": (0,0,"Ingrese la perdida en un entorno urbano")}

        self.list_menu = list(self.var_okumura.keys())  # Opciones de cálculo modelo okumura

        self.entradas_okumura = []  # Lista para guardar los imputs del modelo okumura


    def menu(self):

        # Menú de opciones para modelo okomura
        self.optionmenu = ctk.StringVar(value=self.list_menu[0])
        self.optionokumu = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=self.optionmenu,
                                             width=250, height=30,
                                             command= self.inputs) #cada vez que el usuario cambia la selección,
        # se llama automáticamente a la función inputs pasando el valor seleccionado como argumento.
        self.optionokumu.grid(padx=32, pady=5)

        self.inputs(self.list_menu[0]) #Llama a la funcion inputs por primera vez para mostrar los inputs de la primera opción al cargar la interfaz por defecto.


    #Entradas del modelo Okumura-Hata
    def inputs(self, seleccion):

        self.seleccion_modelo = seleccion #Guarda el valor seleccionado del menú

        # Limpiar todos los inputs
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        self.entradas_okumura.clear()

        fila = 0

        # Genera los labels e Imputs del modelo
        for self.variable in self.list_menu:
            if self.seleccion_modelo != self.variable: #Si el valor del menu seleccionado es diferente a la lista de opciones imprime

                self.label_okumura = ctk.CTkLabel(self.frame_inputs, text=self.variable, text_color="black", font=fuentes["text_resalt"])
                self.label_okumura.grid(row=fila, column=0,**estilos.pad_labels)

                self.in_okumura = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                               placeholder_text=self.var_okumura[self.variable][2], #Imprimer de la lista de var_okumura[key][item]
                                          font=fuentes["text"])
                self.in_okumura.grid(row=fila, column=1,**estilos.pad_inputs)

                self.entradas_okumura.append(self.in_okumura)  # Almacenamos los imputs en una lista

            fila += 1

    #Calculo de variables
    def calculo(self):

        #Refrescamos los valores
        self.valores.clear()
        self.operacion = 0

        variables = [v for v in self.list_menu if v != self.seleccion_modelo] #Generamos una lista con todas las variables menos la seleccionada

        for nombre_variable, entrada in zip(variables, self.entradas_okumura): #Asosiamos cada nombre de variable con su valor ingresado

            try:
                self.valor = float(entrada.get()) #Covertimos cada valor ingresado en un float

                min_val, max_val, _ = self.var_okumura[nombre_variable]

                if min_val !=0 or max_val!=0: #Evitar validar aquellas variables q no tienen rango como a(hm) o pl
                    if not (min_val <= self.valor <= max_val):
                        VentanaError(app) #Valor fuera del rango lanza pantalla error

                self.valores[nombre_variable] = self.valor #Creamos un diccionario con cada nombre variable y float ingresado

            except ValueError:
                self.valores[nombre_variable] = None #Si se ingresa otro valor q no sea numerico se llena con un None

        if None in self.valores.values():
            return VentanaError(app) #Si existe un valor none en valores{} lanza la ventana de error

        f = self.valores.get("Frecuencia (MHz)") #Ingresa el valor de la variable "Frecuencia# se usa un get() para que asigne automaticamente un None al Key, caso contrario salta error.
        hb = self.valores.get("Altura antena base (m)")
        d = self.valores.get("Distancia (Km)")
        ahm = self.valores.get("Corrección por altura del receptor")
        pl = self.valores.get("Perdida (dB)")

        #Evalua cada opcion de cálculo
        if self.seleccion_modelo == "Frecuencia (MHz)":

            # Calculamos la frecuencia
            self.operacion = 10 ** ((pl - 69.55 + 13.82 * np.log10(hb) + ahm - (44.9 - 6.55 * np.log10(hb)) * np.log10(d)) / 26.16)

        elif self.seleccion_modelo == "Altura antena base (m)":

            #Calculamos la altura antena base
            self.operacion = 10 ** ((69.55 + 26.16 * np.log10(f) - pl + 44.9 * np.log10(d) - ahm) / (13.82 + 6.55 * np.log10(d)))

        elif self.seleccion_modelo == "Distancia (Km)":

            #Calculamos la distancia
            self.operacion = 10 ** ((pl - 69.55 - 26.16 * np.log10(d) + 13.82 * np.log10(hb) + ahm) / (44.9 - 6.55 * np.log10(hb)))

        elif self.seleccion_modelo == "Corrección por altura del receptor":

            #Calculamos Correccion de antena movil
            self.operacion = (69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(hb) + (44.9 - 6.55 * np.log10(hb)) * np.log10(d) - pl)


        elif self.seleccion_modelo  == "Perdida (dB)":

            # Calculamos la pérdida
            self.operacion = 69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(hb) - ahm + (44.9 - 6.55 * np.log10(hb)) * np.log10(d)

