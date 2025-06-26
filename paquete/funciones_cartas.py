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

def mostrar_juego(pilas, mazo_reserva):
    """
    Muestra por consola el estado actual del juego:
    - Cada una de las 7 pilas con cartas ocultas y visibles.
    - Cantidad de cartas restantes en el mazo de reserva.

    Args:
        pilas (list): Lista de 7 tuplas (ocultas, visible).
        mazo_reserva (list): Lista de cartas no repartidas (mazo).
    """
    print("\nEstado del juego:")
    for i, (ocultas, visible) in enumerate(pilas):
        ocultas_str = "*" * len(ocultas)
        visible_str = f"({visible[0]} de {visible[1]})"
        print(f"Pila {i+1}: {ocultas_str} {visible_str}")

    print(f"\nMazo de reserva: {len(mazo_reserva)} cartas")







# baraja = crear_baraja()
# barajada = barajar_baraja(baraja)
# pilas, mazo = repartir_cartas(barajada)

# mostrar_juego(pilas, mazo)