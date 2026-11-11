"""Aqui se maneja toda la interfaz del programa"""

import customtkinter as ctk
import estilos
from ventana import VentanaApp
from mod_okumura import Okumura
from mod_costhata import COSTHata
from mod_walfisch import Walfisch
from mod_costwalfisch import COSTWalfisch
from mod_egli import Egli
from mod_log import Log
from modelo_base import unidad_de


estilos.registrar_fuentes() #Carga Montserrat desde la carpeta fuentes antes de crear la ventana

app = VentanaApp()

fuentes = estilos.cargar_fuentes() #Se llama a la funcion q tiene el diccionario de fuentes

ecuaciones = {
    "Okumura-Hata": "PL(dB) = 69.55 + 26.16·log₁₀(f) − 13.82·log₁₀(hb) − a(hm) + [44.9 − 6.55·log₁₀(hb)]·log₁₀(d)",
    "COST-231 Hata": "PL(dB) = 46.3 + 33.9·log₁₀(f) − 13.82·log₁₀(hb) − a(hm) + [44.9 − 6.55·log₁₀(hb)]·log₁₀(d) + C",
    "Walfisch-Ikegami": "PL(dB) = L₀ + Lᵣₜₛ + Lₘₛd",
    "COST-231 Walfisch-Ikegami": "PL(dB) = 42.6 + 26·log₁₀(d) + 20·log₁₀(f)",
    "Modelo Egli": "PL(dB) = K + 20·log₁₀(f) + 40·log₁₀(d) − 20·log₁₀(ht) − a·log₁₀(hr)\nhr ≤ 10 m: K = 76.3, a = 10   |   hr > 10 m: K = 85.9, a = 20",
    "Log-Normal": "PL(dB) = PL(d₀) + 10·n·log₁₀(d/d₀) + Xσ"
}

modelos = list(ecuaciones.keys()) #Genera una lista con los nombres de los modelos
botones_modelo = {} #Botones del menú lateral, por nombre de modelo


def ventana_izquierda():
    """Agrega todos los elementos de la parte izquierda de la ventana"""

    # Nombre de la aplicacion
    nom_app = ctk.CTkLabel(app.frame_nombre, text="MODELTEC", text_color="white", font=fuentes["h1"])
    nom_app.pack(padx=0, pady=32)

    #Generar los botones de modelos
    for modelo in modelos:
        buton_izq = ctk.CTkButton(app.frame_opciones,
                                  text=modelo,
                                  **estilos.estilo_boton_modelo, #Lee el diccionario de estilo
                                  command=lambda mod=modelo: ventana_derecha(mod)) #Obtiene el modelo al hacer click
        buton_izq.pack(padx=32, pady=20)
        botones_modelo[modelo] = buton_izq


def resaltar_modelo_activo(activo):
    """Marca en el menú lateral el modelo que se está viendo"""

    for modelo, boton in botones_modelo.items():
        if modelo == activo:
            boton.configure(fg_color="#FFFFFF", border_color="#E88C0C", border_width=3)
        else:
            boton.configure(fg_color=estilos.estilo_boton_modelo["fg_color"],
                            border_color=estilos.estilo_boton_modelo["border_color"],
                            border_width=estilos.estilo_boton_modelo["border_width"])


def limpiar_frames_derecha():
    """Limpiar la ventana derecha cada q se presiona un boton"""

    for frame in [app.frame_titulo, app.frame_formula, app.frame_inputs,
                  app.frame_boton, app.frame_OptionMenu, app.frame_resultados]:
        for widget in frame.winfo_children():
            widget.destroy()

modelo_actual = None


def ventana_derecha(mod):
    """Agrega todos los elementos de la parte derecha de la ventana"""

    global modelo_actual

    limpiar_frames_derecha()

    #Título del modelo seleccionado
    titulo_modelo = ctk.CTkLabel(app.frame_titulo,
                                 text=mod if mod.startswith("Modelo") else f"Modelo {mod}",
                                 text_color="black",
                                 font=fuentes["h2"]
                                 )
    titulo_modelo.pack(padx=32, pady=(32,10))

    # Formula del modelo
    formula_oku = ctk.CTkLabel(app.frame_formula, text=ecuaciones[mod], text_color="black",
                               font=fuentes["text_resalt"])  # Rempalazar variable del txt por el boton seleccionado
    formula_oku.grid(padx=32, pady=10)

    # Llama a la funcion del modelo seleccionado
    clases_modelos = {
        "Okumura-Hata": Okumura,
        "COST-231 Hata": COSTHata,
        "Walfisch-Ikegami": Walfisch,
        "COST-231 Walfisch-Ikegami": COSTWalfisch,
        "Modelo Egli": Egli,
        "Log-Normal": Log
    }

    clase_modelo = clases_modelos.get(mod)

    if clase_modelo:

        #Se pasan parametros basicos a la clase del modelo
        modelo_actual = clase_modelo(app.frame_inputs, app.frame_OptionMenu)
        #Se llama al metodo para crear el menu desplegable
        modelo_actual.menu()
        resaltar_modelo_activo(mod)

        # Limpiar resultados
        for widget in app.frame_resultados.winfo_children():
            widget.destroy()

        # Mostrar resultado de la operación
        label_resultado = ctk.CTkLabel(app.frame_resultados,
                                       text="",
                                       text_color="black",
                                       font=fuentes["text"])
        label_resultado.grid(row=0, column=0, **estilos.pad_result)

        resultado = ctk.CTkLabel(app.frame_resultados,
                                 text="—",
                                 text_color="black",
                                 font=fuentes["h1"])
        resultado.grid(row=1, column=0, **estilos.pad_result)

        def mostrar_vacio():
            """Antes de calcular (o al cambiar de variable) no se muestra ningún número"""
            label_resultado.configure(text=f"Resultado: {modelo_actual.seleccion_modelo}")
            resultado.configure(text="—")

        mostrar_vacio()
        modelo_actual.al_cambiar = mostrar_vacio

        def calcular_mostrar(evento=None):

            #Ejecuta el calculo con los datos ingresados
            #Si la validación falla (dato inválido o fuera de rango) no se actualiza el resultado
            if modelo_actual.calculo() is False:
                return

            #Actualiza los label con el cálculo realizado, con su unidad
            unidad = unidad_de(modelo_actual.seleccion_modelo)
            label_resultado.configure(text=f"Resultado: {modelo_actual.seleccion_modelo}")
            resultado.configure(text=f"{modelo_actual.operacion:.2f} {unidad}".strip())


        # Boton de calcular
        buton_cal = ctk.CTkButton(app.frame_boton,
                                      text="Calcular",
                                      **estilos.estilo_boton_calcular,
                                      command=calcular_mostrar)  # Se llama a la funcion calculo del modelo actual
        buton_cal.grid(row=0, column=0, padx=32, pady=5, sticky="w")

        # Enter también calcula (el bind reemplaza al de la vista anterior)
        app.app.bind("<Return>", calcular_mostrar)


ventana_izquierda()
ventana_derecha("Okumura-Hata")

app.iniciar() #Mostrar ventana
