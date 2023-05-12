from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

from barberia_model import *
import random


class BarberiaVista():
    def __init__(self, start_model_callback):
        self.window = tk.Tk()
        self.window.title("Barberia")

        self.__start_model_callback = start_model_callback
        self.canvas: tk.Canvas = tk.Canvas(self.window, width=1000, height=450)
        self.canvas.pack()

        self.images = self.__load_images()

        play_button = tk.Button(text='Play simulation',
                                command=self.__start_model_callback)
        play_button.pack(ipadx=5, ipady=5, expand=True)

        self.show_escenario()

    def __muestra_flecha(self):
        self.canvas.create_image(
            650, 150, image=self.images["flecha"], anchor='center')

    def __muestra_etiquetas(self):
        self.__barberia_label = ttk.Label(self.window, text="BARBERIA")
        self.__barberia_label.place(x=50, y=150)

        self.__afeidatos_label = ttk.Label(self.window, text="AFEITADOS")
        self.__afeidatos_label.place(x=50, y=285)

        self.__volveran_label = ttk.Label(self.window, text="OTRO DIA ...")
        self.__volveran_label.place(x=50, y=360)

        self.__sala_espera_label = ttk.Label(
            self.window, text="SALA DE ESPERA")
        self.__sala_espera_label.place(x=300, y=60)

    def __load_image(self, filename, rotate_angle=None, widh=None, high=None):
        # try/except
        img = Image.open(filename)

        if widh is not None and high is not None:
            img = img.resize((widh, high), Image.ANTIALIAS)

        if rotate_angle is not None:
            img = img.rotate(rotate_angle)

        return ImageTk.PhotoImage(img)

    def __load_images(self) -> list:
        images = {
            BarberoStatus.AFEITANDO: self.__load_image("barbero_afeitando.png"),
            BarberoStatus.DURMIENDO: self.__load_image("barbero_durmiendo.png"),
            ClienteStatus.ESPERANDO: self.__load_image("cliente_esperando.png"),
            ClienteStatus.AFEITADO: self.__load_image("cliente_afeitado.png"),
            ClienteStatus.VOLVERA_OTRO_DIA: self.__load_image("cliente_se_va.png"),
            SillaBarberoStatus.LIBRE: self.__load_image("silla_libre.png"),
            SillaBarberoStatus.OCUPADA: [self.__load_image("barbero_afeitando.png")],
            "flecha": self.__load_image("flecha.png"),
        }

        # Cargar segunda imagen silla para animación
        images[SillaBarberoStatus.OCUPADA].append(
            self.__load_image("barbero_afeitando_2.png"))

        return images

    def start(self) -> None:
        self.window.mainloop()

    def muestra_barbero(self, estatus: BarberoStatus, frame=0) -> None:
        if estatus == BarberoStatus.AFEITANDO:
            self.muestra_silla(SillaBarberoStatus.OCUPADA, frame)
        else:
            self.muestra_silla(SillaBarberoStatus.LIBRE)

    def muestra_silla(self, estatus: SillaBarberoStatus, frame=0) -> None:
        self.__barbero_label = ttk.Label(
            self.window, text="EL BARBERO Y SU SILLA")
        self.__barbero_label.place(x=775, y=50)
        self.canvas.create_rectangle(
            750, 100, 950, 200, width=3, fill='yellow')

        if estatus == SillaBarberoStatus.OCUPADA:
            self.canvas.create_image(
                850, 150, image=self.images[SillaBarberoStatus.OCUPADA][frame], anchor='center')
        else:
            self.canvas.create_image(
                800, 150, image=self.images[BarberoStatus.DURMIENDO], anchor='center')
            self.canvas.create_image(
                900, 150, image=self.images[SillaBarberoStatus.LIBRE], anchor='center')

    def muestra_sala_espera(self, num_clientes: int) -> None:
        self.canvas.create_rectangle(
            150, 100, 550, 200, width=3, fill='orange')

        for c in range(0, num_clientes):
            self.canvas.create_image(
                200 + c*75, 150, image=self.images[ClienteStatus.ESPERANDO], anchor='center')

    def muestra_clientes_afeitados(self, num_clientes: int) -> None:
        self.canvas.create_rectangle(
            150, 265, 950, 330, width=3, fill='lightgreen')

        for c in range(0, num_clientes):
            self.canvas.create_image(
                180 + c*38, 300, image=self.images[ClienteStatus.AFEITADO], anchor='center')

    def muestra_clientes_NO_atendidos(self, num_clientes: int) -> None:
        self.canvas.create_rectangle(150, 340, 950, 400, width=3, fill='red')

        for c in range(0, num_clientes):
            self.canvas.create_image(
                180 + c*38, 375, image=self.images[ClienteStatus.VOLVERA_OTRO_DIA], anchor='center')

    def show_escenario(self) -> None:
        self.__muestra_etiquetas()
        self.muestra_sala_espera(0)
        self.__muestra_flecha()
        self.muestra_silla(SillaBarberoStatus.OCUPADA)
        self.muestra_clientes_NO_atendidos(0)
        self.muestra_clientes_afeitados(0)


def main():
    print("Prueba escenario barberia")
    bar = BarberiaVista(None)

    bar.show_escenario()

    bar.start()


if __name__ == '__main__':
    main()
