# Barbero ---> Thread, corta la barba o duerme
# clientes ---> Thread, volvera_otro_dia, esperando, siendo_atendido
# Silla barbero ---> No Thread ---> Región crítica, ocuapada o libre
# silla de espera ---> Semaphore ---> Región crítica, llista de clients, capacidad maxim
import threading
import enum
from colorama import Fore
import time


class BarberoStatus(enum.Enum):
    AFEITANDO = 1
    DURMIENDO = 2


class Barbero(threading.Thread):
    def __init__(self, status_changed_callback=None, sala_espera=None, silla_barbero=None):
        super(Barbero, self).__init__()
        self.status = BarberoStatus.DURMIENDO
        self.status_changed_callback = status_changed_callback
        self.sala_espera: SalaDeEspera = sala_espera
        self.silla_barbero: SillaBarbero = silla_barbero

    def set_status(self, new_status):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.status)

    def afeitar(self):
        self.status = BarberoStatus.AFEITANDO
        self.silla_barbero.get_cliente().siendo_atentido()
        time.sleep(2)  # simular afeitado

    def dormir(self):
        self.status = BarberoStatus.DURMIENDO
        time.sleep(2)

    def despertar(self):
        # despertar el hilo del barbero
        # algun notify

        pass

    def atender_cliente_silla(self):
        self.afeitar()
        self.silla_barbero.liberar_silla()

    def atender_cliente_sala(self):
        cliente = self.sala_espera.siguiente_cliente()
        self.silla_barbero.sentar_cliente(cliente)
        self.afeitar()
        self.silla_barbero.liberar_silla(cliente)

    def run(self):
        while True:
            # atender cliente directamente
            if self.silla_barbero.is_ocupada():
                self.atender_cliente_silla(self.silla_barbero.get_cliente())
            elif not self.sala_espera.is_empty():
                self.atender_cliente_sala()
            else:
                self.dormir()

    def is_sleeping(self) -> bool:
        return self.status == BarberoStatus.DURMIENDO


class ClienteStatus(enum.Enum):
    VOLVERA_OTRO_DIA = 1
    ESPERANDO = 2
    SIENDO_ATENDIDO = 3
    AFEITADO = 4


class Cliente(threading.Thread):
    def __init__(self, client_num, barbero: Barbero, silla_barbero, sala_de_espera, status_changed_callback=None):
        super(Cliente, self).__init__()
        self.barbero: Barbero = barbero
        self.client_num: int = client_num
        self.silla_barbero: SillaBarbero = silla_barbero
        self.sala_de_espera: SalaDeEspera = sala_de_espera
        self.statu: ClienteStatus = ClienteStatus.VOLVERA_OTRO_DIA
        self.status_changed_callback = status_changed_callback

    def __str__(self):
        return "Cliente: " + str(self.client_num) + " Status " + str(self.status)

    def set_status(self, new_status):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.client_num, new_status)

    def afeitado(self):
        self.set_status(ClienteStatus.AFEITADO)

    def siendo_atendido(self):
        self.set_status(ClienteStatus.SIENDO_ATENDIDO)

    def run(self):
        # if el barbero esta durmiendo
        if self.barbero.is_sleeping():
            # el barbero esta disponible
            self.silla_barbero.sentar_cliente(self)
            self.barbero.despertar()

        else:
            # barbero esta trabajando
            # no s'ha pogut seure
            if not self.sala_de_espera.sentar_cliente(self):
                self.set_status(ClienteStatus.VOLVERA_OTRO_DIA)
        #    if la sala de espera no esta llena
        #        sentar en la sala de espera
        # else
        #    si la sala de espera esta llena---> volver otro dia
        pass


class SillaBarberoStatus(enum.Enum):
    OCUPADA = 1
    LIBRE = 2


class SillaBarbero:
    #  falta sincronizar---> RC
    def __init__(self, status_changed_callback: SillaBarberoStatus = None):
        self.status = SillaBarberoStatus.LIBRE
        self.cliente: Cliente = None
        self.status_changed_callback: SillaBarberoStatus = status_changed_callback

    def is_ocupada(self) -> bool:
        return self.status == SillaBarberoStatus.OCUPADA

    def get_cliente(self) -> Cliente:
        return self.cliente

    def set_status(self, new_status: SillaBarberoStatus):
        self.status = new_status

        if self.status_changed_callback != None:
            self.status_changed_callback(self.status)

    def sentar_cliente(self, cliente: Cliente):
        self.cliente = cliente
        cliente.afeitar()
        self.set_status(SillaBarberoStatus.OCUPADA)

    def liberar_silla(self):
        self.cliente.afeitado()
        self.cliente = None
        self.set_status(SillaBarberoStatus.LIBRE)


class SalaDeEspera(list):
    def __init__(self, capadidad_maxima: int, new_cliente_callback=None):
        super(list, self).__init__()
        self.new_cliente_callback = new_cliente_callback
        self.capacidad_maxima = capadidad_maxima

    def is_full(self) -> bool:
        if len(self) >= self.capacidad_maxima:
            return True  # =============>
        return False

    def is_empty(self) -> bool:
        if len(self) == 0:
            return True  # =============>
        return False

    def sentar_cliente(self, cliente: Cliente) -> bool:
        if self.is_full():
            return False  # =============>

        self.append(cliente)
        cliente.set_status(ClienteStatus.ESPERANDO)
        if self.new_cliente_callback != None:
            self.new_cliente_callback(cliente, len(self))
        return True  # =============>

    def siguiente_cliente(self) -> Cliente:
        return self.pop(0)


class Barberia():
    def __init__(self, barbero_status_changed_callback=None, cliente_status_changed_callback=None):
        self.sala_espera = SalaDeEspera()
        self.silla_barbero = SillaBarbero()
        self.barbero_status_changed_callback = barbero_status_changed_callback
        self.cliente_status_changed_callback = cliente_status_changed_callback
        self.barbero = Barbero(barbero_status_changed_callback)
        self.clientes = []
        for cliente_numero in range(0, 100):
            self.clientes.append(
                Cliente(cliente_numero, cliente_status_changed_callback))

    def start(self):
        # arrancar el hilo del barbero
        # arrancar los hilos de los clientes
        for cliente in self.clientes:
            cliente.start()


def barbero_callback(new_status):
    print(Fore.YELLOW, new_status)


def sala_espera_callback(new_cliente, num_cliente_cola):
    print(Fore.BLUE, new_cliente, num_cliente_cola)


def cliente_callback(client_num, new_status):
    print(Fore.GREEN, client_num, new_status)


def main():

    barberia = Barberia(barbero_callback, cliente_callback)
    barberia.start()


if __name__ == "__main__":
    main()
