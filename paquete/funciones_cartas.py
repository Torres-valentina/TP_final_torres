from .constantes import *
import random

def crear_baraja(palos, valores):
    """
    Genera una baraja de 40 cartas (sin 8 ni 9) combinando palos y valores.

    Args:
        palos (list): Lista de palos.
        valores (list): Lista de valores numéricos.

    Returns:
        list: Lista de tuplas (valor, palo) representando las cartas.
    """
    baraja = []
    for palo in palos:
        for valor in valores:
            baraja.append((valor, palo))
    return baraja

def barajar_baraja(baraja):
    """
    Mezcla aleatoriamente las cartas de una baraja (modifica in place).

    Args:
        baraja (list): Lista de cartas ordenadas.

    Returns:
        list: La misma lista mezclada.
    """
    random.shuffle(baraja)
    return baraja

def repartir_cartas(baraja):
    """
    Reparte las cartas en 7 pilas (una carta visible por pila, resto ocultas).
    El resto se usa como mazo de reserva.

    Args:
        baraja (list): Lista de cartas mezcladas.

    Returns:
        tuple: (pilas, mazo_reserva)
            pilas (list): Lista de 7 tuplas (ocultas, visibles).
            mazo_reserva (list): Lista de cartas sobrantes.
    """
    pilas = []
    indice = 0

    for i in range(1, 8):
        cartas_pila = baraja[indice:indice + i]

        ocultas = cartas_pila[:-1]
        visibles = [cartas_pila[-1]]
        pilas.append((ocultas, visibles))
        indice += i

    mazo_reserva = baraja[indice:]
    return pilas, mazo_reserva

def siguiente_carta(mazo, indice):
    """
    Devuelve la siguiente carta visible del mazo y el nuevo índice.

    Args:
        mazo (list): Lista de cartas del mazo.
        indice (int): Índice actual.

    Returns:
        tuple: (carta, nuevo_indice)
    """
    carta = None
    nuevo_indice = 0

    if mazo:
        if indice >= len(mazo):
            indice = 0
        carta = mazo[indice]
        nuevo_indice = indice + 1

    return carta, nuevo_indice

def mover_a_fundacion(carta, fundaciones, palos):
    """
    Intenta mover una carta a su fundación correspondiente.

    Reglas:
    - Si la fundación está vacía, solo se puede colocar un As (1).
    - Si tiene cartas, se debe colocar un valor +1 y mismo palo.

    Args:
        carta (tuple): Carta a mover (valor, palo).
        fundaciones (list): Lista de 4 listas, una por palo.
        palos (list): Lista de palos válidos.

    Returns:
        bool: True si se movió con éxito, False si no.
    """
    exito = False

    if carta is not None and carta[1] in palos:
        valor, palo = carta
        indice = palos.index(palo)
        fundacion = fundaciones[indice]

        if not fundacion:
            if valor == 1:
                fundacion.append(carta)
                exito = True
        else:
            ultimo_valor, _ = fundacion[-1]
            if valor == ultimo_valor + 1:
                fundacion.append(carta)
                exito = True

    return exito


def mover_a_pila_en_indice(carta, pila):
    """
    Intenta mover una carta a una pila específica.

    Reglas:
    - Si la pila está vacía, solo se acepta un 12 (rey).
    - Si tiene cartas, solo se acepta una carta con valor -1 y distinto palo.

    Args:
        carta (tuple): (valor, palo)
        pila (tuple): (ocultas, visibles)

    Returns:
        bool: True si se pudo mover, False si no.
    """
    exito = False

    if carta is not None:
        valor, palo = carta
        ocultas, visibles = pila

        if not visibles:
            if valor == 10:
                visibles.append(carta)
                exito = True
        else:
            tope_valor, tope_palo = visibles[-1]
            if valor == tope_valor - 1 and palo != tope_palo:
                visibles.append(carta)
                exito = True

    return exito


def mover_a_pila_vacia(carta, pilas):
    """
    Intenta mover una carta a una pila vacía. Solo el rey (12) puede moverse.

    Args:
        carta (tuple): (valor, palo)
        pilas (list): Lista de 7 pilas (ocultas, visibles)

    Returns:
        bool: True si se pudo mover, False si no.
    """
    exito = False

    if carta is not None and carta[0] == 10:
        for i in range(len(pilas)):
            ocultas, visibles = pilas[i]
            if not visibles:
                pilas[i] = (ocultas, [carta])
                exito = True
                break

    return exito


def mover_grupo_de_pila_a_pila(pilas, origen_idx, carta_idx, destino_idx):
    """
    Mueve un grupo de cartas desde una pila a otra si cumple las reglas del juego.

    Reglas:
    - Si destino está vacío, el grupo debe empezar con un rey (12).
    - Si destino tiene cartas, el primer del grupo debe ser de valor -1 y diferente palo.

    Args:
        pilas (list): Lista de 7 pilas (ocultas, visibles).
        origen_idx (int): Índice de la pila de origen.
        carta_idx (int): Posición de la carta seleccionada.
        destino_idx (int): Índice de la pila destino.

    Returns:
        bool: True si el grupo se movió con éxito, False si no.
    """
    exito = False

    ocultas_origen, visibles_origen = pilas[origen_idx]
    cartas_a_mover = visibles_origen[carta_idx:]

    if cartas_a_mover:
        valor_mover, palo_mover = cartas_a_mover[0]
        ocultas_destino, visibles_destino = pilas[destino_idx]

        if not visibles_destino:
            if valor_mover == 10:
                exito = True
        else:
            valor_tope, palo_tope = visibles_destino[-1]
            if valor_mover == valor_tope - 1 and palo_mover != palo_tope:
                exito = True

        if exito:
            pilas[destino_idx] = (ocultas_destino, visibles_destino + cartas_a_mover)
            pilas[origen_idx] = (ocultas_origen, visibles_origen[:carta_idx])

            if not pilas[origen_idx][1] and pilas[origen_idx][0]:
                nueva_visible = pilas[origen_idx][0].pop()
                pilas[origen_idx] = (pilas[origen_idx][0], [nueva_visible])

    return exito