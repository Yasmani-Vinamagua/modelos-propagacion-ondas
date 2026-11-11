"""Clase base de los modelos de propagación.

Aquí vive todo lo que era idéntico en los seis modelos: el menú desplegable,
la creación de las entradas, la validación y el manejo de errores.
Cada modelo solo define sus variables y su fórmula.
"""

import math
import re

import customtkinter as ctk
import numpy as np

import estilos


def unidad_de(nombre):
    """Unidad de una variable a partir de su nombre, p. ej. 'Frecuencia (MHz)' -> 'MHz'."""
    if re.search(r"p[eé]rdida|correcci[oó]n", nombre, re.I) and "Exponente" not in nombre:
        return "dB"
    coincidencia = re.search(r"\(([^()]*)\)\s*$", nombre)
    if coincidencia and coincidencia.group(1) in ("MHz", "m", "km", "dB"):
        return coincidencia.group(1)
    return ""  # Sin unidad (por ejemplo el exponente n)


class ModeloBase:
    """Esqueleto común de un modelo de propagación.

    Las clases hijas deben definir:
      - variables: {nombre: (mínimo, máximo, texto_de_ayuda)}. Si mínimo y máximo
        son 0, la variable no tiene rango y no se valida (por ejemplo la pérdida).
        La primera variable es la opción que se muestra por defecto en el menú.
      - calcular(valores): devuelve el resultado de despejar la variable que está
        en self.seleccion_modelo. `valores` trae las demás, por nombre.

    Los errores se muestran dentro del formulario: el campo con problema se marca
    en rojo y debajo aparece el motivo. Bajo cada campo con rango se muestra el
    rango válido como ayuda permanente (el placeholder desaparece al escribir).
    """

    variables = {}

    def __init__(self, frame_inputs, frame_OptionMenu):
        self.frame_inputs = frame_inputs
        self.frame_OptionMenu = frame_OptionMenu

        # Las fuentes se cargan aquí (y no al importar) porque necesitan que la ventana ya exista
        self.fuentes = estilos.cargar_fuentes()

        self.seleccion_modelo = None  # Variable que se va a calcular (opción del menú)
        self.operacion = 0.00  # Último resultado
        self.valores = {}  # Valores numéricos ingresados, por nombre de variable
        self.list_menu = list(self.variables.keys())  # Opciones del menú desplegable
        self.entradas = []  # Cajas de texto visibles, en el orden de las variables
        self.mensajes = []  # Etiqueta bajo cada caja (ayuda o error), mismo orden que entradas
        self.errores = {}  # Último error por variable: {nombre: mensaje}
        self.error_general = ""  # Error que no pertenece a un solo campo
        self.etiqueta_general = None
        self.borde_normal = "gray50"
        self.al_cambiar = None  # Función opcional: se llama cuando el usuario cambia la variable a calcular

        # Lo más habitual es calcular la pérdida: es la opción por defecto si existe
        perdidas = [n for n in self.list_menu if n == "Pérdida (dB)"]
        self.defecto = perdidas[0] if perdidas else self.list_menu[0]

    def menu(self):
        """Crea el menú desplegable con la variable a calcular."""
        etiqueta = ctk.CTkLabel(self.frame_OptionMenu, text="Calcular:", text_color="black",
                                font=self.fuentes["text_resalt"])
        etiqueta.grid(row=0, column=0, padx=(32, 8), pady=5, sticky="w")

        self.optionmenu = ctk.StringVar(value=self.defecto)
        self.option_menu = ctk.CTkOptionMenu(self.frame_OptionMenu,
                                             values=self.list_menu,
                                             variable=self.optionmenu,
                                             width=330, height=32,
                                             font=self.fuentes["text"],
                                             dropdown_font=self.fuentes["text"],
                                             # Colores de la app (blanco sobre azul: contraste ~8:1)
                                             fg_color=estilos.color_primario,
                                             button_color=estilos.color_primario_oscuro,
                                             button_hover_color=estilos.color_primario_oscuro,
                                             text_color="white",
                                             dropdown_fg_color="white",
                                             dropdown_text_color="black",
                                             dropdown_hover_color="#E1F7FA",
                                             command=self.inputs)  # Se llama al cambiar la selección
        self.option_menu.grid(row=0, column=1, padx=(0, 32), pady=5, sticky="w")

        # Muestra los inputs de la opción por defecto
        self.inputs(self.defecto)

    def rango_texto(self, nombre):
        """Texto del rango válido, p. ej. 'Entre 30 y 200 m'. Vacío si la variable no tiene rango."""
        minimo, maximo, _ = self.variables[nombre]
        if minimo == 0 and maximo == 0:
            return ""
        unidad = unidad_de(nombre)
        return f"Entre {minimo:g} y {maximo:g}{' ' + unidad if unidad else ''}"

    def inputs(self, seleccion):
        """Dibuja una entrada por cada variable, excepto la que se va a calcular."""
        self.seleccion_modelo = seleccion

        if self.al_cambiar:
            self.al_cambiar()

        for widget in self.frame_inputs.winfo_children():
            widget.destroy()
        self.entradas.clear()
        self.mensajes.clear()
        self.errores.clear()
        self.error_general = ""

        # Columna de etiquetas de ancho fijo: las cajas quedan alineadas y las etiquetas largas se parten en dos líneas
        self.frame_inputs.grid_columnconfigure(0, minsize=estilos.ancho_etiquetas + 40)

        fila = 0
        for nombre in self.list_menu:
            if nombre == self.seleccion_modelo:
                continue

            # Cada variable ocupa dos filas: la caja y, debajo, su ayuda o error
            etiqueta = ctk.CTkLabel(self.frame_inputs, text=nombre, text_color="black",
                                    font=self.fuentes["text_resalt"],
                                    width=estilos.ancho_etiquetas, wraplength=estilos.ancho_etiquetas,
                                    anchor="w", justify="left")
            etiqueta.grid(row=fila, column=0, padx=(32, 8), pady=(8, 0), sticky="w")

            entrada = ctk.CTkEntry(self.frame_inputs, width=estilos.ancho_inputs,
                                   placeholder_text=self.variables[nombre][2],
                                   font=self.fuentes["text"])
            entrada.grid(row=fila, column=1, padx=(0, 32), pady=(8, 0), sticky="w")
            self.borde_normal = entrada.cget("border_color")

            mensaje = ctk.CTkLabel(self.frame_inputs, text=self.rango_texto(nombre), height=16,
                                   text_color=estilos.color_ayuda, font=self.fuentes["small"])
            mensaje.grid(row=fila + 1, column=1, padx=(6, 32), pady=0, sticky="w")
            # Al escribir se quita el error de ese campo
            entrada.bind("<Key>", lambda evento, n=nombre: self._limpiar_error(n), add="+")

            self.entradas.append(entrada)
            self.mensajes.append(mensaje)
            fila += 2

        # Mensaje para errores que no son de un solo campo (por ejemplo, una división entre cero)
        self.etiqueta_general = ctk.CTkLabel(self.frame_inputs, text="", height=18,
                                             text_color=estilos.color_error, font=self.fuentes["small"])
        self.etiqueta_general.grid(row=fila, column=0, columnspan=2, padx=32, pady=(6, 0), sticky="w")

    # ---------- errores dentro del formulario

    def _nombres_visibles(self):
        return [n for n in self.list_menu if n != self.seleccion_modelo]

    def _marcar_error(self, indice, nombre, texto):
        self.errores[nombre] = texto
        self.entradas[indice].configure(border_color=estilos.color_error)
        self.mensajes[indice].configure(text=texto, text_color=estilos.color_error)

    def _limpiar_error(self, nombre):
        """Quita el error de un campo y vuelve a mostrar su ayuda."""
        if nombre not in self.errores:
            return
        del self.errores[nombre]
        indice = self._nombres_visibles().index(nombre)
        self.entradas[indice].configure(border_color=self.borde_normal)
        self.mensajes[indice].configure(text=self.rango_texto(nombre), text_color=estilos.color_ayuda)

    def _limpiar_errores(self):
        for nombre in list(self.errores):
            self._limpiar_error(nombre)
        self.error_general = ""
        if self.etiqueta_general is not None:
            self.etiqueta_general.configure(text="")

    def _mensaje_de_error(self, nombre, texto, valor):
        """Motivo del error de un campo, con el rango válido cuando existe."""
        rango = self.rango_texto(nombre)
        if texto == "":
            return f"Falta este dato. {rango}".strip()
        if valor is None or not math.isfinite(valor):
            return f"Escribe un número. {rango}".strip()
        return f"Fuera de rango. {rango}".strip()

    def calculo(self):
        """Lee y valida las entradas y calcula. Devuelve False si algo está mal."""
        self.valores.clear()
        self.operacion = 0
        self._limpiar_errores()

        # Se revisan todos los campos, para marcar de una vez cada error
        for indice, (nombre, entrada) in enumerate(zip(self._nombres_visibles(), self.entradas)):
            texto = entrada.get().strip()
            try:
                # En español se escribe 1,5: se acepta la coma decimal
                valor = float(texto.replace(",", "."))
            except ValueError:
                valor = None

            minimo, maximo, _ = self.variables[nombre]
            con_rango = minimo != 0 or maximo != 0
            invalido = (valor is None or not math.isfinite(valor)
                        or (con_rango and not minimo <= valor <= maximo))

            if invalido:
                self._marcar_error(indice, nombre, self._mensaje_de_error(nombre, texto, valor))
            else:
                self.valores[nombre] = valor

        if self.errores:
            return False

        with np.errstate(all="ignore"):  # Un resultado inválido se detecta abajo, sin avisos de numpy
            resultado = self.calcular(self.valores)

        if not np.isfinite(resultado):  # Por ejemplo, una división entre cero
            self.error_general = "Con estos valores no se puede calcular (división entre cero)."
            if self.etiqueta_general is not None:
                self.etiqueta_general.configure(text=self.error_general)
            return False

        self.operacion = resultado
        return True

    def calcular(self, valores):
        raise NotImplementedError
