# Barbero -> Thread, Corta el barba o duerme
# Clientes -> Thread, VOLVERA_OTRO_DIA, ESPERANDO, SIENDO_ATENDIDO
# Silla Barbero -> Región crítica, Ocupada o libre
# Sala de espera -> Región crítica, Lista clientes, capacidad máxima


import threading 
import enum
from colorama import  Fore
import time
import random


class BarberoStatus(enum.Enum):
    AFEITANDO = 1
    DURMIENDO = 2


class Barbero(threading.Thread):
    def __init__(
            self, sala_espera, silla_barbero, on_change_callback=None):

        self.status: BarberoStatus = BarberoStatus.DURMIENDO
        self.on_change_callback = on_change_callback
        self.sala_espera: SalaDeEspera = sala_espera
        self.silla_barbero: SillaBarbero = silla_barbero
        self.semaforo: threading.Semaphore = threading.Semaphore(0)

        super(Barbero, self).__init__()

    def __str__(self) -> str:
        return Fore.LIGHTRED_EX + "BARBERO " + Fore.RESET \
            + self.status.name

    def is_sleeping(self) -> bool:
        return (self.status == BarberoStatus.DURMIENDO)

        return durmiento

    def afeitar(self):
        self.set_status(BarberoStatus.AFEITANDO)
        self.silla_barbero.get_cliente().siendo_atendido()

        time.sleep(2)  # Simula tiempo de afeitado

    def dormir(self):
        self.set_status(BarberoStatus.DURMIENDO)
        self.semaforo.acquire()

    def despertar(self):
        self.semaforo.release()

    def atender_cliente_silla(self):
        self.afeitar()
        self.silla_barbero.liberar_silla()

    def atender_cliente_sala_espera(self):
        siguiente_cliente = self.sala_espera.siguiente_cliente()
        self.silla_barbero.sentar_cliente(siguiente_cliente)
        self.afeitar()
        self.silla_barbero.liberar_silla()

    def set_status(self, new_status):
        self.status = new_status

        if self.on_change_callback != None:
            self.on_change_callback(self)

    def run(self):
        while True:
            if self.silla_barbero.is_ocupada():
                self.atender_cliente_silla()
            elif not self.sala_espera.is_empty():
                self.atender_cliente_sala_espera()
            else:
                self.dormir()


class ClienteStatus(enum.Enum):
    VOLVERA_OTRO_DIA = 1
    ESPERANDO = 2
    SIENDO_ATENDIDO = 3
    AFEITADO = 4


class Cliente(threading.Thread):
    def __init__(self,
                 client_num,
                 barbero: Barbero, silla_barbero, sala_espera,
                 on_change_callback=None):

        self.client_num: int = client_num
        self.barbero: Barbero = barbero
        self.silla_barbero: SillaBarbero = silla_barbero
        self.sala_espera: SalaDeEspera = sala_espera
        self.on_change_callback = on_change_callback
        self.status: ClienteStatus = ClienteStatus.ESPERANDO

        super(Cliente, self).__init__()

    def __str__(self) -> str:
        return Fore.LIGHTGREEN_EX + "CLIENTE " + Fore.RESET \
            + str(self.client_num) + " " + \
            self.status.name + Fore.RESET

    def set_status(self, new_status: ClienteStatus):
        self.status = new_status

        if self.on_change_callback != None:
            self.on_change_callback(self)

    def afeitado_finalizado(self):
        self.set_status(ClienteStatus.AFEITADO)

    def siendo_atendido(self):
        self.set_status(ClienteStatus.SIENDO_ATENDIDO)

    def run(self):
        # Lo primero que hace un cliente es intentar sentarse
        # en la silla de barbero directamente.
        # Esto solo lo conseguirá si esta esta libre.
        if self.silla_barbero.sentar_cliente(self):
            self.barbero.despertar()
            # La silla está libre.
            # En este caso el barbero está disponible y atiende inmediatamente
            # EL hilo del cliente ya no tiene más que hacer... por lo que
            # finaliza con el return
            return

        # Si la silla no está libre es que el barbero está trabajando
        # Entonces el cliente intenta quedarse en la sala de espera
        if not self.sala_espera.sentar_cliente(self):
            # La sala de espera esta al completo por lo que el
            # cliente tendrá que volver otro dia.
            self.set_status(ClienteStatus.VOLVERA_OTRO_DIA)


class SillaBarberoStatus(enum.Enum):
    OCUPADA = 1
    LIBRE = 2


class SillaBarbero():
    def __init__(self, on_change_callback=None):
        self.status = SillaBarberoStatus.LIBRE
        self.cliente: Cliente = None
        self.on_change_callback: function = on_change_callback

        self.semaforo: threading.Semaphore = threading.Semaphore(
            1)  # Admite un thread inicialmente

    def __str__(self) -> str:
        return Fore.CYAN + "SILLA BARBERO " \
            + Fore.RESET + self.status.name + Fore.RESET

    def is_ocupada(self) -> bool:
        return self.status == SillaBarberoStatus.OCUPADA

    def get_cliente(self) -> Cliente:
        return self.cliente

    def __set_status(self, new_status: SillaBarberoStatus):
        self.status = new_status

        if self.on_change_callback != None:
            self.on_change_callback(self)

    def sentar_cliente(self, cliente: Cliente):
        # Un cliente se intenta sentar en la silla, pero
        # solo lo conseguirá si esta está libre.
        # Si consigue adquirir el semáforo (solo admite un thread).
        # se deja bloqueado y se libera solo al liberar la silla.
        if self.semaforo.acquire(blocking=False):
            self.cliente = cliente
            self.__set_status(SillaBarberoStatus.OCUPADA)
            return True

        return False

    def liberar_silla(self):
        self.cliente.afeitado_finalizado()
        self.cliente = None
        self.__set_status(SillaBarberoStatus.LIBRE)

        # Al finalizar el afeitado se libera la silla
        # y su semáforo, así otro hilo podrá entrar.
        self.semaforo.release()


class SalaDeEspera(list):
    def __init__(self, capacidad_maxima: int, on_change_callback):
        super(list, self).__init__()

        self.on_change_callback = on_change_callback
        self.capacidad_maxima: int = capacidad_maxima
        self.semaforo: threading.Semaphore = threading.Semaphore(1)

    def __str__(self) -> str:
        return Fore.LIGHTMAGENTA_EX + "SALA ESPERA " \
            + Fore.RESET + \
            str(len(self)) + Fore.RESET

    def is_empty(self) -> bool:
        return len(self) == 0

    def sentar_cliente(self, cliente: Cliente) -> bool:
        self.semaforo.acquire()

        if len(self) >= self.capacidad_maxima:
            # La sala de espera está al completo
            self.semaforo.release()
            return False  # ============>

        self.append(cliente)
        cliente.set_status(ClienteStatus.ESPERANDO)

        if self.on_change_callback != None:
            self.on_change_callback(self)

        self.semaforo.release()
        return True

    def siguiente_cliente(self) -> Cliente:
        self.semaforo.acquire()
        cliente = self.pop(0)
        self.semaforo.release()

        return cliente


class Barberia():
    def __init__(self, barbero_callback, cliente_callback, sala_espera_callback, silla_barbero_callback):

        self.barbero_callback = barbero_callback
        self.cliente_callback = cliente_callback
        self.sala_espera_callback = sala_espera_callback
        self.silla_barbero_callback = silla_barbero_callback

        self.sala_espera = SalaDeEspera(5, self.sala_espera_callback)
        self.silla_barbero = SillaBarbero(self.silla_barbero_callback)
        self.barbero = Barbero(
            self.sala_espera, self.silla_barbero, self.barbero_callback)

        self.clientes = []
        for cliente_numero in range(1, 21):
            self.clientes.append(
                Cliente(cliente_numero, self.barbero, self.silla_barbero, self.sala_espera, cliente_callback))

    def start(self):
        # Arrancar el hilo del barbero
        self.barbero.start()

        # Arrancar los hilos de los clientes
        for cliente in self.clientes:
            cliente.start()

            # Simulamos que los clientes llegan a la barberia
            # separados por intervalos aleatorios entre 1 y 2 segundos
            time.sleep(random.random()*2)


def barbero_callback(barbero: Barbero):
    print(barbero)


def sala_espera_callback(sala_espera: SalaDeEspera):
    print(sala_espera)


def silla_barbero_callback(silla_barbero: SillaBarbero):
    print(silla_barbero)


def cliente_callback(cliente: Cliente):
    print(cliente)


def main():
    barberia = \
        Barberia(barbero_callback, cliente_callback,
                 sala_espera_callback, silla_barbero_callback)

    barberia.start()


if __name__ == '__main__':
    main()
