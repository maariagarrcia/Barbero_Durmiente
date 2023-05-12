from threading import Thread
from random import random
from barberia_model import *
from barberia_vista import *


class BarberiaController():
    def __init__(self):
        self.__sala_espera = SalaDeEspera(5, self.__sala_espera_callback)
        self.__silla_barbero = SillaBarbero(self.__silla_barbero_callback)
        self.__barbero = None
        self.__clientes = []
        self.__vista = BarberiaVista(self.__start)
        self.__num_afeitados = 0
        self.__num_volveran_otro_dia = 0

    def __barbero_callback(self, barbero: Barbero, frame=0):
        print(barbero)
        self.__vista.muestra_barbero(barbero.status, frame)

    def __sala_espera_callback(self, sala_espera: SalaDeEspera):
        print(sala_espera)
        self.__vista.muestra_sala_espera(sala_espera.get_clientes_esperando())

    def __silla_barbero_callback(self, silla_barbero: SillaBarbero, frame=0):
        print(silla_barbero)
        self.__vista.muestra_silla(silla_barbero, frame)

    def __cliente_callback(self, cliente: Cliente):
        print(cliente)
        if cliente.status == ClienteStatus.AFEITADO:
            self.__num_afeitados += 1
            self.__vista.muestra_clientes_afeitados(self.__num_afeitados)

        elif cliente.status == ClienteStatus.VOLVERA_OTRO_DIA:
            self.__num_volveran_otro_dia += 1
            self.__vista.muestra_clientes_NO_atendidos(
                self.__num_volveran_otro_dia)

    def __nuevo_cliente(self):
        self.__clientes.append(
            Cliente(len(self.__clientes), self.__barbero, self.__silla_barbero, self.__sala_espera, self.__cliente_callback))
        self.__clientes[-1].start()

    def __start(self):
        self.__barbero = Barbero(
            self.__sala_espera, self.__silla_barbero, self.__barbero_callback)

        # Crea y arranca 20 clientes
        for num_cli in range(1, 21):
            self.__nuevo_cliente()

        self.__barbero.start()

    def start(self):
        self.__vista.start()


def main():
    barberia = BarberiaController()
    barberia.start()


if __name__ == '__main__':
    main()
