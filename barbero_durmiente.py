# Barbero ---> Thread, corta la barba o duerme
# clientes ---> Thread, volvera_otro_dia, esperando, siendo_atendido
# Silla barbero ---> No Thread ---> Región crítica, ocuapada o libre
# silla de espera ---> Semaphore ---> Región crítica, llista de clients, capacidad maxim

import threading
import enum
from colorama import Fore


class BarberoStatus(enum.Enum):
    CORTANDO = 1
    DURMIENDO = 2


class Barbero(threading.Thread):
    def __init__(self, status_changed_callback=None):
        super(Barbero, self).__init__()

        self.status = BarberoStatus.DURMIENDO
        self.status_changed_callback = status_changed_callback

    def set_status(self, new_status):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.status)

    def run(self):
        # si hay clientes coortar barba
        # si no hay clientes dormir
        pass


class ClienteStatus(enum.Enum):
    VOLVERA_OTRO_DIA = 1
    ESPERANDO = 2
    SIENDO_ATENDIDO = 3


class Cliente(threading.Thread):
    def __init__(self, client_num, status_changed_callback=None):
        super(Cliente, self).__init__()
        self.client_num = client_num
        self.status = ClienteStatus.VOLVERA_OTRO_DIA
        self.status_changed_callback = status_changed_callback
    def set_status(self, new_status):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.client_num, new_status)
    def run(self):
        # Pide que le cooorten la barba
        # si no le pueden atender, inmmiediatamente pide esperar
        # ssi no hay silla de espera, vuelve otro dia
        pass


class SillaBarberoStatus(enum.Enum):
    OCUPADA = 1
    LIBRE = 2


class SillaBarbero:
    def __init__(self, status_changed_callback=None):
        self.status = SillaBarberoStatus.LIBRE
        self.status_changed_callback = status_changed_callback

    def set_status(self, new_status):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.status)

    def run(self):
        # si hay clientes coortar barba
        # si no hay clientes dormir
        pass


class SalaDeEspera(list):
    def __init__(self, value):
        super(list, self).__init__(value)


class Barberia():
    def __init__(self, barbero_status_changed_callback, cliente_status_changed_callback):
        # crear la sala de espera
        self.sala_espera = SalaDeEspera()
        # crear la silla del barbero
        self.silla_barbero = SillaBarbero()
        # crear el barbero
        self.barbero = Barbero()
        # crear los clientes
        self.clientes = []
        for cliente_numero in range(0, 100):
            self.clientes.append(Cliente(cliente_numero))

    def start(self):
        # arrancar el hilo del barbero
        # arrancar los hilos de los clientes
        for cliente in self.clientes:
            cliente.start()


def barbero_callback(new_status):
    print(Fore.YELLOW, new_status)

def cliente_callback(client_num, new_status):
    print(Fore.GREEN, client_num, new_status)

def main():
    barberia = Barberia(barbero_callback, cliente_callback)
    barberia.start()

if __name__ == "__main__":
    main()