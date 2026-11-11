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

    # Nombre de la aplicacion, con la barra rosa corta de firma debajo
    nom_app = ctk.CTkLabel(app.frame_nombre, text="MODELTEC", text_color=estilos.color_texto, font=fuentes["h1"])
    nom_app.pack(anchor="w", padx=6, pady=(14, 0))
    subtitulo = ctk.CTkLabel(app.frame_nombre, text="Modelos de propagación", text_color=estilos.color_ayuda,
                             font=fuentes["small"], anchor="w")
    subtitulo.pack(anchor="w", padx=8, pady=(0, 10))
    barra = ctk.CTkFrame(app.frame_nombre, width=40, height=4, corner_radius=2, fg_color=estilos.ROSA)
    barra.pack(anchor="w", padx=8, pady=(0, 28))

    #Generar los botones de modelos
    for modelo in modelos:
        buton_izq = ctk.CTkButton(app.frame_opciones,
                                  text=modelo,
                                  **estilos.estilo_boton_modelo, #Lee el diccionario de estilo
                                  command=lambda mod=modelo: ventana_derecha(mod)) #Obtiene el modelo al hacer click
        buton_izq.pack(pady=(0, 18))
        botones_modelo[modelo] = buton_izq


def resaltar_modelo_activo(activo):
    """Marca en el menú lateral el modelo que se está viendo"""

    reposo = {clave: estilos.estilo_boton_modelo[clave]
              for clave in ("fg_color", "hover_color", "text_color", "border_color", "border_width")}

    for modelo, boton in botones_modelo.items():
        boton.configure(**(estilos.estilo_boton_modelo_activo if modelo == activo else reposo))


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
                                 text_color=estilos.color_texto,
                                 font=fuentes["h2"],
                                 anchor="w")
    titulo_modelo.pack(fill="x", padx=8, pady=(4, 4))

    # Formula del modelo
    formula_oku = ctk.CTkLabel(app.frame_formula, text=ecuaciones[mod], text_color=estilos.color_ayuda,
                               font=fuentes["text_resalt"], anchor="w", justify="left", wraplength=730)
    formula_oku.pack(fill="x", padx=8, pady=(0, 8))

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

        # Mostrar resultado de la operación: barra rosa de firma y, a su lado, el texto
        app.frame_resultados.grid_columnconfigure(1, weight=1)
        app.frame_resultados.grid_rowconfigure(0, weight=1)
        barra_resultado = ctk.CTkFrame(app.frame_resultados, width=4, height=58, corner_radius=2,
                                       fg_color=estilos.ROSA)
        barra_resultado.grid(row=0, column=0, padx=(8, 14), sticky="w")

        texto_resultado = ctk.CTkFrame(app.frame_resultados, fg_color="transparent", corner_radius=0)
        texto_resultado.grid(row=0, column=1, sticky="w")

        label_resultado = ctk.CTkLabel(texto_resultado,
                                       text="",
                                       text_color=estilos.color_ayuda,
                                       font=fuentes["text"],
                                       anchor="w")
        label_resultado.pack(anchor="w")

        resultado = ctk.CTkLabel(texto_resultado,
                                 text="—",
                                 text_color=estilos.color_texto,
                                 font=fuentes["resultado"],
                                 anchor="w")
        resultado.pack(anchor="w")

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
        buton_cal.pack(anchor="w", padx=8, pady=(6, 0))

        # Enter también calcula (el bind reemplaza al de la vista anterior)
        app.app.bind("<Return>", calcular_mostrar)


ventana_izquierda()
ventana_derecha("Okumura-Hata")

app.iniciar() #Mostrar ventana
