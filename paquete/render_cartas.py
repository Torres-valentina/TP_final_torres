import pygame
from paquete.constantes import *

# Cargar imágenes de cartas una vez
imagenes_cartas = {}
REVERSO = None

def inicializar_imagenes():
    """
    Inicializa la imagen del reverso de la carta y la escala al tamaño definido.
    Asigna la imagen escalada a la variable global REVERSO.
    """
    global REVERSO
    REVERSO = pygame.image.load("cartas/reverso.jpg").convert_alpha()
    REVERSO = pygame.transform.scale(REVERSO, TAM_CARTA)

def cargar_imagen(valor, palo):
    """
    Carga la imagen de una carta específica y la escala al tamaño definido.
    Si la imagen ya ha sido cargada previamente, la devuelve desde un caché
    (diccionario global 'imagenes_cartas').

    Args:
        valor (str): El valor de la carta (ej. "1", "sota").
        palo (str): El palo de la carta (ej. "oros", "copas").

    Returns:
        pygame.Surface: La superficie de Pygame que contiene la imagen de la carta.
    """
    clave = f"{valor} de {palo}"
    if clave not in imagenes_cartas:
        ruta = f"cartas/{clave}.jpg"
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.scale(img, TAM_CARTA)
        imagenes_cartas[clave] = img
    return imagenes_cartas[clave]

def dibujar_fundaciones(pantalla, fundaciones):
    """
    Dibuja las cuatro pilas de fundaciones en la pantalla.
    Si una fundación tiene cartas, dibuja la carta superior.
    Si una fundación está vacía, dibuja un marco blanco.

    Args:
        pantalla (pygame.Surface): La superficie de la pantalla de Pygame.
        fundaciones (list): Una lista de listas, donde cada sublista representa
                             una fundación y contiene las cartas en ella.
    """
    for i in range(4):
        x = FUNDACION_X + i * (TAM_CARTA[0] + 20)
        y = FUNDACION_Y

        if fundaciones[i]:
            valor, palo = fundaciones[i][-1]  # última carta
            imagen = cargar_imagen(valor, palo)
            pantalla.blit(imagen, (x, y))
        else:
            pygame.draw.rect(pantalla, (255, 255, 255), (x, y, *TAM_CARTA), 2)  # marco blanco

def dibujar_pilas_con_imagenes(pantalla, pilas, carta_mazo=None, fundaciones=None):
    """
    Dibuja todas las pilas de juego (ocultas y visibles), el mazo y las fundaciones
    en la pantalla.

    Args:
        pantalla (pygame.Surface): La superficie de la pantalla de Pygame.
        pilas (list): Una lista de tuplas, donde cada tupla contiene
                      (cartas_ocultas, cartas_visibles) para cada pila.
        carta_mazo (tuple, optional): La carta superior del mazo. Si es None,
                                      se dibuja el reverso del mazo.
        fundaciones (list, optional): Lista de listas que representan las fundaciones.
                                      Si es None, se inicializa como cuatro listas vacías.
    """
    pantalla.fill(VERDE)

    if fundaciones is None:
        fundaciones = [[], [], [], []]

    dibujar_fundaciones(pantalla, fundaciones)

    for i, (ocultas, visibles) in enumerate(pilas):
        x = ORIGEN_X + i * ESPACIADO_X
        y = ORIGEN_Y

        for _ in ocultas:
            pantalla.blit(REVERSO, (x, y))
            y += ESPACIADO_Y

        for carta in visibles:
            valor, palo = carta
            imagen = cargar_imagen(valor, palo)
            pantalla.blit(imagen, (x, y))
            y += ESPACIADO_Y

        if not ocultas and not visibles:
            # Dibujá un rectángulo gris para representar la pila vacía
                pygame.draw.rect(pantalla, (100, 100, 100), (x, y, 80, 120), 2)

    if carta_mazo:
        valor, palo = carta_mazo
        imagen = cargar_imagen(valor, palo)
        pantalla.blit(imagen, (50, 20))
    else:
        pantalla.blit(REVERSO, (50, 20))

