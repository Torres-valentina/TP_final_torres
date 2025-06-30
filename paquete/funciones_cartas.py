from .constantes import *
import random

def crear_baraja():
    """
    Genera una baraja española de 40 cartas (sin 8 ni 9).
    
    Recorre todos los palos y valores definidos en constantes,
    devolviendo una lista de tuplas (valor, palo).

    Returns:
        list: Lista de 40 tuplas representando las cartas.
    """
    baraja = []
    for palo in PALOS:
        for valor in VALORES:
            carta = (valor, palo)
            baraja.append(carta)
    return baraja

def barajar_baraja(baraja):
    """
    Mezcla aleatoriamente las cartas de una baraja sin modificar la original.

    Args:
        baraja (list): Lista de cartas ordenadas.

    Returns:
        list: Nueva lista de cartas mezcladas.
    """
    nueva_baraja = baraja.copy()
    random.shuffle(nueva_baraja)
    return nueva_baraja

def repartir_cartas(baraja):
    """
    Reparte las cartas en 7 pilas, donde cada pila tiene una carta visible y el resto ocultas.
    El resto de la baraja se devuelve como mazo de reserva.

    Args:
        baraja (list): Lista de cartas mezcladas.

    Returns:
        tuple: (pilas, mazo_reserva)
            pilas (list): Lista de 7 tuplas (ocultas, visible)
            mazo_reserva (list): Lista de cartas no repartidas
    """
    pilas = []
    indice = 0

    for i in range(1, 8):  # 1 a 7 inclusive
        cartas_pila = baraja[indice:indice + i]
        ocultas = cartas_pila[:-1]     # todas menos la última
        visible = cartas_pila[-1]      # la última carta
        pilas.append((ocultas, visible))
        indice += i

    mazo_reserva = baraja[indice:]  # lo que quedó sin repartir
    return pilas, mazo_reserva

def siguiente_carta(mazo, indice):
    """
    Devuelve la siguiente carta visible del mazo.

    Args:
        mazo (list): Lista de cartas en el mazo.
        indice (int): Índice actual.

    Returns:
        tuple: (carta actual o None, nuevo índice)
    """
    if indice < len(mazo):
        carta_mas_indice = mazo[indice], indice + 1
    else:
        carta_mas_indice = None, 0  # si termina el mazo, reinicia

    return carta_mas_indice



