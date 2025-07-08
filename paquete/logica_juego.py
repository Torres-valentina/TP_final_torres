from paquete.constantes import PALOS, VALORES
from paquete.funciones_cartas import crear_baraja, barajar_baraja, repartir_cartas

def inicializar_estado_juego_cartas():
    """
    Inicializa las pilas, mazo y fundaciones para comenzar una nueva partida.
    Esta función se encarga solo de la lógica de las cartas.

    Returns:
        tuple: (pilas, mazo, fundaciones)
    """
    baraja = barajar_baraja(crear_baraja(PALOS, VALORES))
    pilas, mazo = repartir_cartas(baraja)
    fundaciones = [[] for _ in range(4)]
    return pilas, mazo, fundaciones

