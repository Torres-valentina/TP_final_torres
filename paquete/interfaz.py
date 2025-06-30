import pygame
import sys
from .funciones_cartas import *
from .funciones_ranking import obtener_estado_ranking
from .render_cartas import *
from .constantes import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Solitario Español")
fuente = pygame.font.SysFont("arial", 24)
inicializar_imagenes() 

# Área del mazo (zona clickeable)
MAZO_RECT = pygame.Rect(50, 20, 80, 120)

def dibujar_boton(texto, x, y, ancho, alto):
    """
    Dibuja un botón en la pantalla.

    Args:
         texto (str): El texto a mostrar en el botón.
         x (int): La coordenada X de la esquina superior izquierda del botón.
         y (int): La coordenada Y de la esquina superior izquierda del botón.
         ancho (int): El ancho del botón.
         alto (int): La altura del botón.

    Returns:
         pygame.Rect: El objeto Rect que representa el área del botón.
     """
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, AZUL, rect)
    texto_render = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_render, (x + 10, y + 10))
    return rect

def mostrar_menu():
    """
    Muestra el menú principal del juego en la pantalla.

    Returns:
        dict: Un diccionario que contiene los objetos Rect de los botones del menú,
              con las claves "jugar", "ranking" y "salir".
    """
    pantalla.fill(NEGRO)
    titulo = fuente.render("Solitario Español - Menú Principal", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

    boton_jugar = dibujar_boton("Jugar", 300, 150, 200, 50)
    boton_ranking = dibujar_boton("Ver Ranking", 300, 230, 200, 50)
    boton_salir = dibujar_boton("Salir", 300, 310, 200, 50)

    return {
        "jugar": boton_jugar,
        "ranking": boton_ranking,
        "salir": boton_salir
    }

def mostrar_textos(lista_textos):
    """
    Muestra una lista de textos en la pantalla.

    Args:
        lista_textos (list): Una lista de cadenas de texto a mostrar.
    """
    pantalla.fill(NEGRO)
    y = 50
    for texto in lista_textos:
        linea = fuente.render(texto, True, BLANCO)
        pantalla.blit(linea, (50, y))
        y += 30

def loop_menu():
    """
    Gestiona el bucle principal del menú, manejando la interacción del usuario
    con los botones del menú.
    """
    botones = mostrar_menu()
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botones["jugar"].collidepoint(evento.pos):
                    loop_juego()
                    botones = mostrar_menu()
                    pygame.display.flip()
                elif botones["ranking"].collidepoint(evento.pos):
                    textos = obtener_estado_ranking()
                    mostrar_textos(textos)
                    pygame.display.flip()
                elif botones["salir"].collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

def loop_juego():
    """
    Gestiona el bucle principal del juego de solitario, incluyendo la inicialización
    del juego, el dibujo de las cartas y el manejo de eventos del usuario.
    """
    baraja = barajar_baraja(crear_baraja())
    pilas, mazo = repartir_cartas(baraja)
    fundaciones = [[], [], [], []]
    indice_mazo = 0
    carta_visible = None

    corriendo = True
    while corriendo:
        carta_visible = mazo[indice_mazo - 1] if indice_mazo > 0 else None
        dibujar_pilas_con_imagenes(pantalla, pilas, carta_visible, fundaciones)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if MAZO_RECT.collidepoint(evento.pos):
                    _, indice_mazo = siguiente_carta(mazo, indice_mazo)
