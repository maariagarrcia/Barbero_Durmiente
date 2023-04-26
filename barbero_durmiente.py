#Barbero ---> Thread, corta la barba o duerme
# clientes ---> Thread, volvera_otro_dia, esperando, siendo_atendido
# Silla barbero ---> No Thread ---> Región crítica, ocuapada o libre
# silla de espera ---> Semaphore ---> Región crítica, llista de clients, capacidad maxim
import threading
import enum

class BarberoStatus(enum.Enum):
    CORTANDO = 1
    DURMIENDO = 2

class Barbero(threading.Thread):
    def __init__(self):
        self.status = BarberoStatus.DURMIENDO
        pass

    def set_status(self, new_status):
        self.status = new_status
        

    def run(self):
        # si hay clientes coortar barba
        # si no hay clientes dormir
        pass


class  ClienteStatus(enum.Enum):
    VOLVERA_OTRO_DIA = 1
    ESPERANDO = 2
    SIENDO_ATENDIDO = 3
    
class Cliente(threading.Thread):
    def __init__(self):
        self.status = ClienteStatus.VOLVERA_OTRO_DIA
        pass

    def set_status(self, new_status):
        self.status = new_status

    def run(self):
        # Pide que le cooorten la barba
        # si no le pueden atender, inmmiediatamente pide esperar
        # ssi no hay silla de espera, vuelve otro dia
        pass



class SillaBarbero:
    def __init__(self):
        self.status = BarberoStatus.DURMIENDO
        pass
    def set_status(self, new_status):
        self.status = new_status
    def run(self):
        # si hay clientes coortar barba
        # si no hay clientes dormir
        pass