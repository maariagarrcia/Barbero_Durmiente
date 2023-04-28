import tkinter as tk
from PIL import Image, ImageTk
import math
import barbero_durmiente as bd #  importar el archivo que contiene la clase Barberia
import colorama


class MyViewer():
    def __init__(self):
        super(MyViewer, self).__init__()

        self.window = tk.Tk()
        self.window.title("Barbero Durmiente")

        self.canvas: tk.Canvas = tk.Canvas(self.window, width=500, height=500)
        self.canvas.pack()

        self.images = self.load_images()
        self.draw_complete_scenario()

        play_button = tk.Button(text='Play simulation', command=self.myTask)
        play_button.pack(ipadx=5, ipady=5, expand=True)

        self.window.mainloop()

    def barbero_status_changed(self,  new_status):
        print(colorama.Fore.YELLOW,  new_status)
        self.draw_barbero(self.images[new_status])

    def silla_status_changed(self, new_status):
        print(colorama.Fore.LIGHTBLUE_EX, new_status)
        self.draw_silla(new_status)

    def cliente_status_changed(self, cliente_num: int, new_status):
        print(colorama.Fore.LIGHTGREEN_EX, cliente_num, new_status)
        self.draw_cliente(cliente_num, self.images[new_status])

    def sala_espera_status_changed(self,  new_status):
        print(colorama.Fore.LIGHTGREEN_EX, new_status)

    def draw_complete_scenario(self):
        self.canvas.create_rectangle(0, 0, 500, 500, fill="#1E90FF")
        self.canvas.create_image(250, 250, image=self.images[bd.SillaBarberoStatus.LIBRE], anchor='center')
        self.canvas.create_text(250, 50, text="BARBERIA", font=("Arial", 30, "bold"))
        self.canvas.create_rectangle(40, 90, 160, 210,dash=(4, 2))
        self.draw_barbero(0, self.images[bd.BarberoStatus.DURMIENDO])
        # rectangulo para la sala de espera grande
        self.canvas.create_rectangle(50, 380, 450, 470, dash=(4, 2))
        self.canvas.create_text(250, 350, text="SALA DE ESPERA", font=("Arial", 18))
        # silla inicial
        for i in range(5):
            self.draw_cliente(i, self.images[bd.ClienteStatus.SIENDO_ATENDIDO])

    def draw_cliente(self, cliente_num, image: ImageTk.PhotoImage, color=""):
        # clientes en sillas una al lado de la otra
        
        x = 100 + 70 * (cliente_num)
        y = 425 
    
        self.canvas.create_image(x, y, image=image, anchor='center')

    def draw_barbero(self, barbero_num:int, image, color=""):
        x = 100 
        y = 150 
        self.canvas.create_image(x, y, image=image, anchor='center')
    
    def draw_silla(self,  image, color=""):
        self.canvas.create_image(300,120 , image=image, anchor='center')

    def load_image(self, filename, rotate_angle=0, widh=75, high=75):
        img = Image.open(filename)
        img = img.resize((widh, high), Image.ANTIALIAS)
        img = img.rotate(rotate_angle)

        return ImageTk.PhotoImage(img)

    def load_images(self) -> list:
        images = {
            bd.BarberoStatus.AFEITANDO: self.load_image(
                "barbero_afeitando.png", 0, 100, 100),
            bd.BarberoStatus.DURMIENDO: self.load_image(
                "barbero_durmiendo.png", 0, 95, 95),
            bd.SillaBarberoStatus.LIBRE: self.load_image(
                "silla_barbero.png", 0, 75, 75),
            bd.SillaBarberoStatus.OCUPADA: self.load_image("barbero_afeitando.png", 0, 100, 100),
            bd.ClienteStatus.ESPERANDO: self.load_image("cliente.png",0,65,65),
            bd.ClienteStatus.SIENDO_ATENDIDO: self.load_image("silla.png",0,65,65), # silla estara vacia cuando el cliente este siendo atendido
            bd.ClienteStatus.AFEITADO: self.load_image("ADIOS.png",0,65,65), # cliente se va de la barberia
            bd.ClienteStatus.VOLVERA_OTRO_DIA: self.load_image("ADIOS.png",0,65,65), # cliente esperando en la sala de espera
        }

        return images

    def myTask(self):
        sim = bd.Barberia(self.barbero_status_changed,
                           self.cliente_status_changed,self.sala_espera_status_changed,self.silla_status_changed)
        sim.start()


def main():
    vw = MyViewer()

if __name__ == '__main__':
    main()
