# BARBERO
# =======
#   · Tiene un hilo asociado que modela su comportamiento
#   · El hilo del barbero no termina.
#   · Comportamiento:
#       1) Si hay un cliente en la silla AFEITAR.
#       2) Si la silla está libre pero hay clientes en la cola
#          atender el primer cliente de la cola: AFEITAR.
#       3) Si no hay clientes que atender se pone a DORMIR.
#   · Para "dormir" usamos un semáforo que no se puede adquirir y
#     el resultado es que el hilo se bloquea.
#   · Los clientes para despertarle liberan el semáforo.
#   · El estado inicial del barbero es DORMIDO

# CLIENTES
# ========
#   · Tienen un hilo asociado que modela su comportamiento.
#   · Comportamiento:
#       1) El cliente llega a la barberia y mira si hay
#          gente en la sala de espera.
#       2) Si NO hay clientes en espera intenta sentarse en la
#          silla del barbero para ser atendido de inmediato. Esto
#          es posible si la silla esta libre y en tal caso se sienta
#          (el hilo finaliza).
#       3) Llegado a este punto, significa que el cliente no ha
#          a podido ser atendido de inmediato así que intentará
#          ponerse en espera ...
#       4) Si hay espacio en la sala de espera se queda en la sala
#          (el hilo finaliza)
#       5) Si no hay espacio decide decide volver otro día y se
#          marcha (el hilo finaliza).
#   · Estados del cliente: VOLVERA_OTRO_DIA, ESPERANDO, SIENDO_ATENDIDO

# Silla Barbero
# =============
#   · Región crítica
#   · Puede estar Ocupada o libre

# Sala de espera
# ==============
#   · Se podria simular con solo un semáforo pero así es más realista.
#   · Contiene una lista de clientes.
#   · Región crítica ya que no se pueden añadir y eliminar clientes a la vez.
#   · Tiene una capacidad máxima que se establece cuando se crea.


import threading
import enum
from colorama import Fore
import time
import random

class BarberoStatus(enum.Enum):
    AFEITANDO = 1
    DURMIENDO = 2


class Barbero(threading.Thread):
    def __init__(self, sala_espera, silla_barbero, on_change_callback=None):
        super(Barbero, self).__init__()

        self.status: BarberoStatus = BarberoStatus.DURMIENDO
        self.on_change_callback = on_change_callback
        self.sala_espera: SalaDeEspera = sala_espera
        self.silla_barbero: SillaBarbero = silla_barbero
        self.semaforo: threading.Semaphore = threading.Semaphore(0)

    def __str__(self) -> str:
        return Fore.LIGHTRED_EX + "BARBERO " + Fore.RESET \
            + self.status.name

    def __set_status(self, new_status):
        self.status = new_status

        if self.on_change_callback != None:
            self.on_change_callback(self)

    def is_sleeping(self) -> bool:
        return (self.status == BarberoStatus.DURMIENDO)

    def afeitar(self):
        self.__set_status(BarberoStatus.AFEITANDO)
        self.silla_barbero.get_cliente().siendo_atendido()

        time.sleep(2)  # Simula tiempo de afeitado

    def dormir(self):
        self.__set_status(BarberoStatus.DURMIENDO)
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
    def __init__(self, client_num, barbero: Barbero, silla_barbero, sala_espera, on_change_callback=None):
        super(Cliente, self).__init__()

        self.client_num: int = client_num
        self.barbero: Barbero = barbero
        self.silla_barbero: SillaBarbero = silla_barbero
        self.sala_espera: SalaDeEspera = sala_espera
        self.on_change_callback = on_change_callback
        self.status: ClienteStatus = ClienteStatus.ESPERANDO

    def __str__(self) -> str:
        return Fore.LIGHTGREEN_EX + "CLIENTE " + Fore.RESET \
            + str(self.client_num) + " " + \
            self.status.name + Fore.RESET

    def __set_status(self, new_status: ClienteStatus):
        self.status = new_status

        if self.on_change_callback != None:
            self.on_change_callback(self)

    def afeitado_finalizado(self):
        self.__set_status(ClienteStatus.AFEITADO)

    def siendo_atendido(self):
        self.__set_status(ClienteStatus.SIENDO_ATENDIDO)

    def run(self):
        # El cliente llega a la barberia y mira si hay
        # gente en la sala de espera.
        if self.sala_espera.is_empty():
            # Si NO hay clientes en espera intenta sentarse en la
            # silla del barbero para ser atendido de inmediato.
            if self.silla_barbero.sentar_cliente(self):
                # La silla esta libre y en tal caso se sienta.
                # Despierta al barbero y este le atienda de inmediato
                self.barbero.despertar()
                return  # El hilo finaliza ====================>

        # Llegado a este punto, significa que el cliente no ha
        # a podido ser atendido de inmediato así que intentará
        # ponerse en espera ...
        if self.sala_espera.sentar_cliente(self):
            # Hay espacio en la sala por lo que se queda en cola
            self.__set_status(ClienteStatus.ESPERANDO)
            return  # El hilo finaliza ==========================>

        # La sala de espera esta al completo por lo que el
        # cliente tendrá que volver otro dia.
        self.__set_status(ClienteStatus.VOLVERA_OTRO_DIA)

        return  # El hilo finaliza ==============================>


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
        # Protege la región crítica (la lista de clientes)
        self.semaforo.acquire()

        if len(self) >= self.capacidad_maxima:
            # La sala de espera está al completo
            self.semaforo.release()
            return False  # ============>

        self.append(cliente)

        if self.on_change_callback != None:
            self.on_change_callback(self)

        # Libera la región crítica para que otro hilos la puedan usar
        self.semaforo.release()
        return True

    def siguiente_cliente(self) -> Cliente:
        # Protege la región crítica (la lista de clientes)
        self.semaforo.acquire()

        cliente = self.pop(0)

        # Libera la región crítica
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

    def nuevo_cliente(self):
        self.clientes.append(
            Cliente(len(self.clientes), self.barbero, self.silla_barbero, self.sala_espera, cliente_callback))
        self.clientes[-1].start()

    def start(self):
        # Arrancar el hilo del barbero
        self.barbero.start()

        # Crea y arranca 20 clientes
        for cliente_numero in range(1, 21):
            self.nuevo_cliente()

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
