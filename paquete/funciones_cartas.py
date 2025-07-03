from .constantes import *
import random

def crear_baraja(palos, valores):
    """
    Genera una baraja española de 40 cartas (sin 8 ni 9).
    
    Recorre todos los palos y valores definidos en constantes,
    devolviendo una lista de tuplas (valor, palo).

    Returns:
        list: Lista de 40 tuplas representando las cartas.
    """
    baraja = []
    for palo in palos:
        for valor in valores:
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
    random.shuffle(baraja)
    return baraja

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

    for i in range(1, 8):
        cartas_pila = baraja[indice:indice + i]

        if not cartas_pila:
            break  # ⚠️ cortamos el reparto si no hay más cartas

        ocultas = cartas_pila[:-1]
        visibles = [cartas_pila[-1]]
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



def mover_a_fundacion(carta, fundaciones, palos):
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

    bandera = False
    if carta == None:
        bandera = False

    valor, palo = carta

    # Verificar que el palo esté en la lista de fundaciones
    if palo not in palos:
        bandera = False

    indice = palos.index(palo)
    fundacion = fundaciones[indice]

    if not fundacion:
        if valor == 1:
            fundacion.append(carta)
            bandera = True
    else:
        ultimo_valor, _ = fundacion[-1]
        if valor == ultimo_valor + 1:
            fundacion.append(carta)
            bandera = True

    return bandera

def mover_a_pila_en_indice(carta, pila):
    """
    Intenta mover una carta a una pila específica.

    Reglas:
    - Si la pila está vacía: solo acepta un 12 (rey)
    - Si la pila tiene cartas: acepta solo cartas de valor -1 y de palo distinto al tope

    Args:
        carta (tuple): (valor, palo)
        pila (tuple): (ocultas, visibles)

    Returns:
        bool: True si se pudo mover, False en caso contrario.
    """
    if carta is None:
        return False

    valor, palo = carta
    ocultas, visibles = pila

    if not visibles:  # Pila vacía
        if valor == 10:
            visibles.append(carta)
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

    if valor != 10:
        return False

    for i in range(len(pilas)):
        ocultas, visibles = pilas[i]
        if not visibles:
            pilas[i] = (ocultas, [carta])
            return True

    return False
def mover_grupo_de_pila_a_pila(pilas, origen_idx, carta_idx, destino_idx):
    ocultas_origen, visibles_origen = pilas[origen_idx]
    cartas_a_mover = visibles_origen[carta_idx:]

    if not cartas_a_mover:
        return False

    valor_mover, palo_mover = cartas_a_mover[0]
    ocultas_destino, visibles_destino = pilas[destino_idx]

    if not visibles_destino:
        if valor_mover != 10:
            return False
        else:
            pilas[destino_idx] = (ocultas_destino, visibles_destino + cartas_a_mover)
            pilas[origen_idx] = (ocultas_origen, visibles_origen[:carta_idx])
    else:
        valor_tope, palo_tope = visibles_destino[-1]

        if valor_mover == valor_tope - 1 and palo_mover != palo_tope:
            pilas[destino_idx] = (ocultas_destino, visibles_destino + cartas_a_mover)
            pilas[origen_idx] = (ocultas_origen, visibles_origen[:carta_idx])
        else:
            return False

    if not pilas[origen_idx][1] and pilas[origen_idx][0]:
        nueva_visible = pilas[origen_idx][0].pop()
        pilas[origen_idx] = (pilas[origen_idx][0], [nueva_visible])

    return True
