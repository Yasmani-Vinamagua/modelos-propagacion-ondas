"""Aqui se configura la ventana de error de toda la app"""

import customtkinter as ctk

class VentanaError(ctk.CTkToplevel):

    """Configura la ventana de error"""
    def __init__(self, master):
        super().__init__(master)
        self.title("¡Error!")
        self.geometry("300x150")

        label = ctk.CTkLabel(self, text="Al parecer ingresaste mal un dato"
                                        "\n \n Vuelve a intentarlo")
        label.pack(pady=20)

        boton_cerrar = ctk.CTkButton(self, text="Cerrar",fg_color="red", command=self.destroy)

        boton_cerrar.pack(pady=10)
