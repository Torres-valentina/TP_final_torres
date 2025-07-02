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
        visibles = [cartas_pila[-1]]   # la última carta
        pilas.append((ocultas, visibles))
        indice += i

    mazo_reserva = baraja[indice:]  # lo que quedó sin repartir
    return pilas, mazo_reserva


def siguiente_carta(mazo, indice):
    """
    Devuelve la siguiente carta visible del mazo y el nuevo índice.
    Cuando se llega al final, vuelve a empezar desde 0.
    """
    if len(mazo) == 0:
        return None, 0

    if indice >= len(mazo):
        indice = 0

    return mazo[indice], indice + 1



def mover_a_fundacion(carta, fundaciones):
    """
    Intenta mover una carta a su fundación correspondiente.
    Cada palo tiene su propia fundación (según el orden definido en PALOS).

    Solo permite mover:
    - Un 1 (as) a una fundación vacía
    - O una carta cuyo valor sea +1 del último en su fundación y del mismo palo

    Parámetros:
        carta: (valor, palo)
        fundaciones: lista de 4 listas (una por palo)

    Devuelve:
        True si se movió con éxito, False si no se pudo
    """
    from .constantes import PALOS

    if carta is None:
        return False

    valor, palo = carta

    # Verificar que el palo esté en la lista de fundaciones
    if palo not in PALOS:
        return False

    indice = PALOS.index(palo)
    fundacion = fundaciones[indice]

    if not fundacion:
        if valor == 1:
            fundacion.append(carta)
            return True
    else:
        ultimo_valor, _ = fundacion[-1]
        if valor == ultimo_valor + 1:
            fundacion.append(carta)
            return True

    return False

def mover_a_pila(carta, pilas):
    """
    Intenta mover una carta a alguna de las 7 pilas.
    
    Reglas:
    - Si la pila está vacía: solo acepta un 12 (rey)
    - Si la pila tiene cartas: acepta solo cartas de valor -1 y de palo distinto al tope

    Args:
        carta (tuple): (valor, palo) a mover.
        pilas (list): Lista de 7 pilas, donde cada pila es (ocultas, visibles).

    Returns:
        bool: True si se pudo mover, False en caso contrario.
    """
    if carta is None:
        return False

    valor, palo = carta

    for i in range(len(pilas)):
        ocultas, visibles = pilas[i]

        if not visibles:  # Pila vacía
            if valor == 12:
                pilas[i] = (ocultas, [carta])
                return True
        else:
            tope_valor, tope_palo = visibles[-1]
            if valor == tope_valor - 1 and palo != tope_palo:
                visibles.append(carta)
                return True

    return False
def mover_a_pila_vacia(carta, pilas):
    """
    Intenta mover una carta a una pila vacía.
    Solo se permite si la carta es un 12 (rey).

    Args:
        carta (tuple): (valor, palo)
        pilas (list): Lista de 7 pilas (ocultas, visibles)

    Returns:
        bool: True si se movió con éxito, False si no se pudo
    """
    if carta is None:
        return False

    valor, _ = carta

    if valor != 12:
        return False

    for i in range(len(pilas)):
        ocultas, visibles = pilas[i]
        if not visibles:
            pilas[i] = (ocultas, [carta])
            return True

    return False