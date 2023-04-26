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
        while True:
            pass


class ClienteStatus(enum.Enum):
    VOLVERA_OTRO_DIA = 1
    ESPERANDO = 2
    SIENDO_ATENDIDO = 3
    AFEITADO = 4


class Cliente(threading.Thread):
    def __init__(self, client_num, status_changed_callback=None):
        super(Cliente, self).__init__()

        self.client_num: int = client_num
        self.statu: ClienteStatus = ClienteStatus.VOLVERA_OTRO_DIA
        self.status_changed_callback = status_changed_callback

    def __str__(self):
        return "Cliente: " + str(self.client_num) + " Status " + str(self.status)

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
    #  falta sincronizar---> RC
    def __init__(self, status_changed_callback: SillaBarberoStatus = None):
        self.status = SillaBarberoStatus.LIBRE
        self.cliente: Cliente = None
        self.status_changed_callback: SillaBarberoStatus = status_changed_callback

    def set_status(self, new_status: SillaBarberoStatus):
        self.status = new_status
        if self.status_changed_callback != None:
            self.status_changed_callback(self.status)

    def sentar_cliente(self, cliente: Cliente):
        self.cliente = cliente
        cliente.set_status(ClienteStatus.SIENDO_ATENDIDO)
        self.set_status(SillaBarberoStatus.OCUPADA)

    def cliente_efitado(self):
        self.set_status(ClienteStatus.AFEITADO)
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

    def nuevo_cliente(self, cliente: Cliente):
        if self.is_full():
            return False  # =============>
        self.append(cliente)
        cliente.set_status(ClienteStatus.ESPERANDO)

        if self.new_cliente_callback != None:
            self.new_cliente_callback(cliente, len(self))

        return True  # =============>


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
