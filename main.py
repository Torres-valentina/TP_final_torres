import pygame
import sys
from paquete.constantes import ANCHO, ALTO, PALOS, VALORES, BOTON_VOLVER_RECT
from paquete.carga import *
from paquete.render_cartas import inicializar_reverso, cargar_imagenes_cartas
from paquete.interfaz import mostrar_menu, toggle_musica, mostrar_textos
from paquete.funciones_ranking import obtener_estado_ranking
from paquete.gestor_juego import ejecutar_bucle_juego # Importar la nueva función del bucle de juego

# --- Inicialización ---
pygame.init()
pygame.mixer.init()

# Cargar recursos una sola vez al inicio
reverso = inicializar_reverso()
imagenes_cartas = cargar_imagenes_cartas(PALOS, VALORES) # Cargar todas las imágenes de cartas
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Solitario")
pygame.display.set_icon(pygame.image.load("imagenes/icono.png"))

#--------------MUSICA-----------------------
pygame.mixer.music.load("sonidos/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#fuente, tipo y tamaño de la letra
fuente = pygame.font.SysFont("consolas", 24)

# --- Recursos visuales (botones e iconos) ---
icono_sonido, icono_silencio, boton_sonido_rect = cargar_iconos_sonido()
imagen_boton_volver, BOTON_VOLVER_RECT = cargar_boton_volver()
imagen_boton_siguiente = cargar_boton_siguiente()


# --- Estado de la música para el menú (persiste entre el menú y el juego) ---
musica_activada_global = True
icono_actual_global = icono_sonido

# --- Bucle principal del juego / menú ---
while True:
    # Mostrar menú principal cada vez que se regresa al menú
    botones_menu = mostrar_menu(pantalla, fuente, icono_actual_global, boton_sonido_rect)
    pygame.display.flip()

    menu_activo = True
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_sonido_rect.collidepoint(evento.pos):
                    musica_activada_global, icono_actual_global = toggle_musica(
                        musica_activada_global, icono_sonido, icono_silencio
                    )
                    # Redibujar el menú inmediatamente para mostrar el cambio de icono
                    botones_menu = mostrar_menu(pantalla, fuente, icono_actual_global, boton_sonido_rect)
                    pygame.display.flip()
                    continue # Salir del bucle de eventos para evitar clics dobles

                if botones_menu["jugar"].collidepoint(evento.pos):
                    # Pasar el estado actual de la música al bucle del juego
                    musica_activada_global, icono_actual_global = ejecutar_bucle_juego(
                        pantalla, fuente, reverso, imagenes_cartas,
                        icono_sonido, icono_silencio, boton_sonido_rect,
                        imagen_boton_volver, imagen_boton_siguiente,
                        musica_activada_global, icono_actual_global # <-- Pasar el estado
                    )
                    menu_activo = False # Salir del bucle del menú para redibujar el menú principal
                    break # Salir del for de eventos
                
                elif botones_menu["ranking"].collidepoint(evento.pos):
                    textos_ranking = obtener_estado_ranking()
                    mostrando_ranking = True

                    while mostrando_ranking:
                        for evento_ranking in pygame.event.get():
                            if evento_ranking.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif evento_ranking.type == pygame.MOUSEBUTTONDOWN:
                                if BOTON_VOLVER_RECT.collidepoint(evento_ranking.pos):
                                    mostrando_ranking = False

                        mostrar_textos(pantalla, fuente, textos_ranking, imagen_boton_volver, BOTON_VOLVER_RECT)
                        pygame.display.flip()
                    
                    # Al salir del ranking, el menú se redibujará
                    menu_activo = False # Salir del bucle del menú para redibujar el menú principal
                    break # Salir del for de eventos

                elif botones_menu["salir"].collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
