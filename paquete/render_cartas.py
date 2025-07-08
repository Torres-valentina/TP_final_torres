# import pygame
# from paquete.constantes import *

# def inicializar_reverso():
#     """
#     Carga y escala la imagen del reverso de las cartas.
#     """
#     reverso = pygame.image.load("cartas/reverso.jpg")
#     if pygame.display.get_surface():
#         reverso = reverso.convert_alpha()
#     reverso = pygame.transform.scale(reverso, TAM_CARTA)
#     return reverso

# def cargar_imagen(valor, palo, imagenes_cache):
#     """
#     Carga y escala una imagen de carta específica y la almacena en caché.

#     Args:
#         valor (int): Valor de la carta.
#         palo (str): Palo de la carta.
#         imagenes_cache (dict): Diccionario para almacenar imágenes ya cargadas.

#     Returns:
#         Surface: Imagen de la carta ya cargada y escalada.
#     """
#     clave = f"{valor} de {palo}"
#     if clave not in imagenes_cache:
#         ruta = f"cartas/{clave}.jpg"
#         imagen = pygame.image.load(ruta)
#         if pygame.display.get_surface():
#             imagen = imagen.convert_alpha()
#         imagen = pygame.transform.scale(imagen, TAM_CARTA)
#         imagenes_cache[clave] = imagen
#     return imagenes_cache[clave]

# def dibujar_fundaciones(pantalla, fundaciones, imagenes_cache):
#     """
#     Dibuja las fundaciones (pilas objetivo) en la pantalla.

#     Args:
#         pantalla (Surface): Pantalla de Pygame.
#         fundaciones (list): Lista de listas con las cartas en cada fundación.
#         imagenes_cache (dict): Caché de imágenes para evitar recarga.
#     """
#     for i in range(4):
#         x = FUNDACION_X + i * (TAM_CARTA[0] + 20)
#         y = FUNDACION_Y
#         if fundaciones[i]:
#             valor, palo = fundaciones[i][-1]
#             imagen = cargar_imagen(valor, palo, imagenes_cache)
#             pantalla.blit(imagen, (x, y))
#         else:
#             pygame.draw.rect(pantalla, (255, 255, 255), (x, y, *TAM_CARTA), 2)

# def dibujar_pilas_con_imagenes(pantalla, pilas, reverso, imagenes_cache, carta_mazo=None, fundaciones=None):
#     """
#     Dibuja las pilas del juego en la pantalla.

#     Args:
#         pantalla (Surface): Superficie de Pygame donde se dibuja.
#         pilas (list): Lista de tuplas con cartas ocultas y visibles.
#         reverso (Surface): Imagen del reverso de las cartas.
#         imagenes_cache (dict): Caché de imágenes.
#         carta_mazo (tuple or None): Carta visible del mazo actual.
#         fundaciones (list or None): Fundaciones del juego.
#     """
#     pantalla.fill(VERDE)
#     if fundaciones is None:
#         fundaciones = [[], [], [], []]

#     dibujar_fundaciones(pantalla, fundaciones, imagenes_cache)

#     for i, (ocultas, visibles) in enumerate(pilas):
#         x = ORIGEN_X + i * ESPACIADO_X
#         y = ORIGEN_Y

#         for _ in ocultas:
#             pantalla.blit(reverso, (x, y))
#             y += ESPACIADO_Y

#         for carta in visibles:
#             valor, palo = carta
#             imagen = cargar_imagen(valor, palo, imagenes_cache)
#             pantalla.blit(imagen, (x, y))
#             y += ESPACIADO_Y

#         if not ocultas and not visibles:
#             pygame.draw.rect(pantalla, (100, 100, 100), (x, y, *TAM_CARTA), 2)

#     if carta_mazo:
#         valor, palo = carta_mazo
#         imagen = cargar_imagen(valor, palo, imagenes_cache)
#         pantalla.blit(imagen, (50, 20))
#     else:
#         pantalla.blit(reverso, (50, 20))

import pygame
from paquete.constantes import *

def inicializar_reverso():
    """
    Carga y escala la imagen del reverso de las cartas.
    """
    reverso = pygame.image.load("cartas/reverso.jpg")
    if pygame.display.get_surface():
        reverso = reverso.convert_alpha()
    reverso = pygame.transform.scale(reverso, TAM_CARTA)
    return reverso

def cargar_imagen(valor, palo, imagenes_cache):
    """
    Carga y escala una imagen de carta específica y la almacena en caché.

    Args:
        valor (int): Valor de la carta.
        palo (str): Palo de la carta.
        imagenes_cache (dict): Diccionario para almacenar imágenes ya cargadas.

    Returns:
        Surface: Imagen de la carta ya cargada y escalada.
    """
    clave = f"{valor} de {palo}"
    if clave not in imagenes_cache:
        ruta = f"cartas/{clave}.jpg"
        imagen = pygame.image.load(ruta)
        if pygame.display.get_surface():
            imagen = imagen.convert_alpha()
        imagen = pygame.transform.scale(imagen, TAM_CARTA)
        imagenes_cache[clave] = imagen
    return imagenes_cache[clave]

def cargar_imagenes_cartas(palos, valores):
    """
    Carga todas las imágenes de las cartas y las almacena en un diccionario.

    Args:
        palos (list): Lista de palos.
        valores (list): Lista de valores numéricos.

    Returns:
        dict: Diccionario con todas las imágenes de las cartas cargadas.
    """
    imagenes_cache = {}
    for palo in palos:
        for valor in valores:
            cargar_imagen(valor, palo, imagenes_cache)
    return imagenes_cache


def dibujar_fundaciones(pantalla, fundaciones, imagenes_cache):
    """
    Dibuja las fundaciones (pilas objetivo) en la pantalla.

    Args:
        pantalla (Surface): Pantalla de Pygame.
        fundaciones (list): Lista de listas con las cartas en cada fundación.
        imagenes_cache (dict): Caché de imágenes para evitar recarga.
    """
    for i in range(4):
        x = FUNDACION_X + i * (TAM_CARTA[0] + 20)
        y = FUNDACION_Y
        if fundaciones[i]:
            valor, palo = fundaciones[i][-1]
            imagen = cargar_imagen(valor, palo, imagenes_cache)
            pantalla.blit(imagen, (x, y))
        else:
            pygame.draw.rect(pantalla, (255, 255, 255), (x, y, *TAM_CARTA), 2)

def dibujar_pilas_con_imagenes(pantalla, pilas, reverso, imagenes_cache, carta_mazo, fundaciones):
    """
    Dibuja las pilas del juego en la pantalla.

    Args:
        pantalla (Surface): Superficie de Pygame donde se dibuja.
        pilas (list): Lista de tuplas con cartas ocultas y visibles.
        reverso (Surface): Imagen del reverso de las cartas.
        imagenes_cache (dict): Caché de imágenes.
        carta_mazo (tuple or None): Carta visible del mazo actual.
        fundaciones (list): Fundaciones del juego.
    """
    pantalla.fill(VERDE)

    dibujar_fundaciones(pantalla, fundaciones, imagenes_cache)

    for i, (ocultas, visibles) in enumerate(pilas):
        x = ORIGEN_X + i * ESPACIADO_X
        y = ORIGEN_Y

        for _ in ocultas:
            pantalla.blit(reverso, (x, y))
            y += ESPACIADO_Y

        for carta in visibles:
            valor, palo = carta
            imagen = cargar_imagen(valor, palo, imagenes_cache)
            pantalla.blit(imagen, (x, y))
            y += ESPACIADO_Y

        if not ocultas and not visibles:
            pygame.draw.rect(pantalla, (100, 100, 100), (x, y, *TAM_CARTA), 2)

    if carta_mazo:
        valor, palo = carta_mazo
        imagen = cargar_imagen(valor, palo, imagenes_cache)
        pantalla.blit(imagen, (50, 20))
    else:
        pantalla.blit(reverso, (50, 20))

def dibujar_escena_juego(pantalla, pilas, carta_visible, fundaciones,
                         icono_actual, boton_sonido_rect,
                         imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                         imagen_boton_volver, BOTON_VOLVER_RECT,
                         carta_seleccionada, seleccion_visible,
                         reverso, imagenes_cartas):
    """
    Dibuja la escena completa del juego en pantalla.
    """
    pantalla.fill(VERDE)
    dibujar_pilas_con_imagenes(pantalla, pilas, reverso, imagenes_cartas, carta_visible, fundaciones)
    pantalla.blit(icono_actual, boton_sonido_rect)
    pantalla.blit(imagen_boton_siguiente, BOTON_SIGUIENTE_RECT)
    pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

    if carta_seleccionada and seleccion_visible:
        pygame.draw.rect(pantalla, (255, 0, 0), seleccion_visible, 3)

    pygame.display.flip()