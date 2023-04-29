# EL BARBERO DURMIENTE
1) VISUALIZACIÓN EN EL TKINTER

2) EXPLICACIÓN

El problema del barbero durmiente es un problema clásico de sincronización en la informática. En este problema, un barbero espera en una barbería para afeitar la barba a los clientes. 

- Si no hay clientes en la barbería, el barbero se duerme. 
- Cuando un cliente llega, si el barbero está durmiendo, el cliente se sienta en la silla del barbero, lo despierta y le afeita. 
- Si hay varios clientes en la barbería esperando a ser atendidos, el barbero atiende a uno de ellos y los demás deben esperar en una sala de espera. 
- Si la sala de espera esta llena el cliente volverá otro dia.

3) PREVENCIÓN DE DEADLOCK

Para proteger la región crítica usamos 2 semáforos.

- Un semáforo(0) para el barbero donde se controla cuando el barbero estará despierto o dormido.
- Un semaforo(1) para la lista de clientes
- Otro semáforo(1) para saber si la silla del barbero esta libre o ocupada. 


