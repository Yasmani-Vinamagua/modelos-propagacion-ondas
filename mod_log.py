import customtkinter as ctk
import numpy as np
import estilos
from error import VentanaError

app = ctk.CTk()

fuentes = estilos.cargar_fuentes() #Se llama a la funcion q tiene el diccionario de fuentes

class Log:

    def __init__(self, frame_inputs, frame_OptionMenu):
        self.frame_OptionMenu = frame_OptionMenu
        self.frame_inputs = frame_inputs

        self.operacion = 0.00

        self.valores = {} # Creamos una lista para almacenar los datos del input

        self.var_log = {
            "Pérdida a distancia d₀ (PL(d₀))": (0, 200, "Pérdida en d₀ (PL₀) en dB"),
            "Distancia d₀ (Km)": (0.01, 1, "Distancia de referencia (d₀) entre 0.01-1 Km"),
            "Distancia d (Km)": (0.01, 20, "Distancia d entre 0.01-20 Km"),
            "Exponente de pérdida (n)": (1, 6, "Exponente n entre 1-6"),
            "Variación Xσ (dB)": (-20, 20, "Variable aleatoria Xσ (normal, en dB)"),
            "Perdida (dB)": (0, 0, "Ingrese la pérdida total PL")
        }

        self.list_menu = list(self.var_log.keys())  # Opciones de cálculo modelo log

        self.entradas_log = []  # Lista para guardar los imputs del modelo log


    def menu(self):

        # Menú de opciones para modelo okomura
        self.optionmenu = ctk.StringVar(value=self.list_menu[0])
        self.optionlog = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=self.optionmenu,
                                             width=250, height=30,
                                             command= self.inputs) #cada vez que el usuario cambia la selección,
        # se llama automáticamente a la función inputs pasando el valor seleccionado como argumento.
        self.optionlog.grid(padx=32, pady=5)

        self.inputs(self.list_menu[0]) #Llama a la funcion inputs por primera vez para mostrar los inputs de la primera opción al cargar la interfaz por defecto.


    #Entradas del modelo log
    def inputs(self, seleccion):

        self.seleccion_modelo = seleccion #Guarda el valor seleccionado del menú

        # Limpiar todos los inputs
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        self.entradas_log.clear()

        fila = 0

        # Genera los labels e Imputs del modelo
        for self.variable in self.list_menu:
            if self.seleccion_modelo != self.variable: #Si el valor del menu seleccionado es diferente a la lista de opciones imprime

                self.label_log = ctk.CTkLabel(self.frame_inputs, text=self.variable, text_color="black", font=fuentes["text_resalt"])
                self.label_log.grid(row=fila, column=0,**estilos.pad_labels)

                self.in_log = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                               placeholder_text=self.var_log[self.variable][2], #Imprimer de la lista de var_log[key][item]
                                          font=fuentes["text"])
                self.in_log.grid(row=fila, column=1,**estilos.pad_inputs)

                self.entradas_log.append(self.in_log)  # Almacenamos los imputs en una lista

            fila += 1

    #Calculo de variables
    def calculo(self):

        #Refrescamos los valores
        self.valores.clear()
        self.operacion = 0

        variables = [v for v in self.list_menu if v != self.seleccion_modelo] #Generamos una lista con todas las variables menos la seleccionada

        for nombre_variable, entrada in zip(variables, self.entradas_log): #Asosiamos cada nombre de variable con su valor ingresado

            try:
                self.valor = float(entrada.get()) #Covertimos cada valor ingresado en un float

                min_val, max_val, _ = self.var_log[nombre_variable]

                if min_val !=0 or max_val!=0: #Evitar validar aquellas variables q no tienen rango como a(hm) o pl
                    if not (min_val <= self.valor <= max_val):
                        VentanaError(app) #Valor fuera del rango lanza pantalla error

                self.valores[nombre_variable] = self.valor #Creamos un diccionario con cada nombre variable y float ingresado

            except ValueError:
                self.valores[nombre_variable] = None #Si se ingresa otro valor q no sea numerico se llena con un None

        if None in self.valores.values():
            return VentanaError(app) #Si existe un valor none en valores{} lanza la ventana de error

        pl_d0 = self.valores.get("Pérdida a distancia d₀ (PL(d₀))")
        d0 = self.valores.get("Distancia d₀ (Km)")
        d = self.valores.get("Distancia d (Km)")
        n = self.valores.get("Exponente de pérdida (n)")
        x_sigma = self.valores.get("Variación Xσ (dB)")
        pl = self.valores.get("Perdida (dB)")


        # Evalúa cada opción de cálculo del modelo log
        if self.seleccion_modelo == "Pérdida a distancia d₀ (PL(d₀))":
            # Despejar PL(d₀)
            self.operacion = pl - 10 * n * np.log10(d / d0) - x_sigma

        elif self.seleccion_modelo == "Distancia d₀ (Km)":
            # Despejar d₀
            self.operacion = d / (10 ** ((pl - pl_d0 - x_sigma) / (10 * n)))

        elif self.seleccion_modelo == "Distancia d (Km)":
            # Despejar d
            self.operacion = d0 * (10 ** ((pl - pl_d0 - x_sigma) / (10 * n)))

        elif self.seleccion_modelo == "Exponente de pérdida (n)":
            # Despejar n
            self.operacion = (pl - pl_d0 - x_sigma) / (10 * np.log10(d / d0))

        elif self.seleccion_modelo == "Variación Xσ (dB)":
            # Despejar Xσ
            self.operacion = pl - pl_d0 - 10 * n * np.log10(d / d0)

        elif self.seleccion_modelo == "Perdida (dB)":
            # Calcular PL
            self.operacion = pl_d0 + 10 * n * np.log10(d / d0) + x_sigma