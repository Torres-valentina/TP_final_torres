import pygame
import sys
from paquete.constantes import *
from paquete.variables_pygame import *
from paquete.render_cartas import inicializar_reverso
from paquete.interfaz import *
from paquete.funciones_ranking import obtener_estado_ranking
from paquete.logica_juego import *

# --- Inicialización ---
pygame.init()
pygame.mixer.init()
reverso = inicializar_reverso()
imagenes_cartas = {}
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Solitario")
pygame.display.set_icon(pygame.image.load("imagenes/icono.png"))

pygame.mixer.music.load("sonidos/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

fuente = pygame.font.SysFont("consolas", 24)

# --- Recursos visuales ---
icono_sonido, icono_silencio, boton_sonido_rect = cargar_iconos_sonido()
imagen_boton_volver, BOTON_VOLVER_RECT = cargar_boton_volver()
imagen_boton_siguiente = cargar_boton_siguiente()
MAZO_RECT = pygame.Rect(50, 20, 80, 120)
FUNDACION_RECTS = [pygame.Rect(400 + i * 100, 20, 80, 120) for i in range(4)]

# --- Estado de la música ---
musica_activada = True
icono_actual = icono_sonido

# --- Bucle de menú ---
botones = mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect)
pygame.display.flip()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_sonido_rect.collidepoint(evento.pos):
                musica_activada, icono_actual = toggle_musica(musica_activada, icono_sonido, icono_silencio)
                botones = mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect)
                pygame.display.flip()
                continue

            if botones["jugar"].collidepoint(evento.pos):
                # --- Preparar juego ---
                pilas, mazo, fundaciones = inicializar_estado_juego()
                indice_mazo = 0
                carta_visible = mazo[indice_mazo] #if mazo else None
                carta_seleccionada = None
                seleccion_visible = None
                movimientos = 0
                BOTON_SIGUIENTE_RECT = pygame.Rect(150, 50, 80, 40)
                corriendo = True

                while corriendo:
                    carta_visible = mazo[indice_mazo] if mazo and indice_mazo < len(mazo) else None

                    dibujar_escena_juego(
                        pantalla, pilas, carta_visible, fundaciones, icono_actual,
                        boton_sonido_rect, imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                        imagen_boton_volver, BOTON_VOLVER_RECT,
                        carta_seleccionada, seleccion_visible,
                        reverso, imagenes_cartas, carta_visible

                        )
                    pygame.display.flip()

                    if sum(len(f) for f in fundaciones) == 40:
                        mostrar_mensaje_ganaste_y_guardar_ranking(pantalla, fuente, movimientos, imagen_boton_volver, BOTON_VOLVER_RECT)
                        break

                    resultado = manejar_eventos(
                        pantalla, fuente, pygame.event.get(), pilas, mazo, fundaciones,
                        indice_mazo, carta_visible, carta_seleccionada, seleccion_visible,
                        musica_activada, icono_actual, boton_sonido_rect, imagen_boton_volver,
                        BOTON_VOLVER_RECT, imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                        MAZO_RECT, FUNDACION_RECTS, movimientos,
                        icono_sonido, icono_silencio,reverso, imagenes_cartas
                    )

                    (
                        corriendo, indice_mazo, carta_visible, carta_seleccionada,
                        seleccion_visible, musica_activada, icono_actual, movimientos
                    ) = resultado

                # Volver al menú al salir del juego
                botones = mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect)
                pygame.display.flip()

            elif botones["ranking"].collidepoint(evento.pos):
                textos = obtener_estado_ranking()
                mostrando = True

                while mostrando:
                    for evento_r in pygame.event.get():
                        if evento_r.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif evento_r.type == pygame.MOUSEBUTTONDOWN:
                            if BOTON_VOLVER_RECT.collidepoint(evento_r.pos):
                                mostrando = False

                    mostrar_textos(pantalla, fuente, textos, imagen_boton_volver, BOTON_VOLVER_RECT)
                    pygame.display.flip()

                botones = mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect)
                pygame.display.flip()

            elif botones["salir"].collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
