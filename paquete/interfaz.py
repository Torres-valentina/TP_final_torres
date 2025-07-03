import pygame
import sys
from .funciones_cartas import *
from .funciones_ranking import obtener_estado_ranking
from .render_cartas import *
from .constantes import *
from .variables_pygame import *

def toggle_musica():
    global musica_activada, icono_actual
    if musica_activada:
        pygame.mixer.music.pause()
        icono_actual = icono_silencio
    else:
        pygame.mixer.music.unpause()
        icono_actual = icono_sonido
    musica_activada = not musica_activada

def dibujar_boton(texto, x, y, ancho, alto):
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, AZUL, rect)
    texto_render = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_render, (x + 10, y + 10))
    return rect

def mostrar_menu():
    pantalla.fill(NEGRO)
    titulo = fuente.render("Solitario - Menú Principal", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

    boton_jugar = dibujar_boton("Jugar", 300, 150, 200, 50)
    boton_ranking = dibujar_boton("Ver Ranking", 300, 230, 200, 50)
    boton_salir = dibujar_boton("Salir", 300, 310, 200, 50)

    pantalla.blit(icono_actual, boton_sonido_rect)

    return {
        "jugar": boton_jugar,
        "ranking": boton_ranking,
        "salir": boton_salir
    }

def mostrar_textos(lista_textos):
    pantalla.fill(NEGRO)
    y = 50
    for texto in lista_textos:
        linea = fuente.render(texto, True, BLANCO)
        pantalla.blit(linea, (50, y))
        y += 30
    pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

def mostrar_mensaje_ganaste_y_guardar_ranking(movimientos):
    pantalla.fill(NEGRO)
    texto_ganaste = fuente.render("¡Ganaste! 🎉", True, BLANCO)
    texto_movs = fuente.render(f"Movimientos: {movimientos}", True, BLANCO)
    texto_ingresa = fuente.render("Ingresá tu nombre:", True, BLANCO)

    nombre = ""
    ingresando = True

    while ingresando:
        pantalla.fill(NEGRO)
        pantalla.blit(texto_ganaste, (ANCHO // 2 - texto_ganaste.get_width() // 2, 100))
        pantalla.blit(texto_movs, (ANCHO // 2 - texto_movs.get_width() // 2, 150))
        pantalla.blit(texto_ingresa, (ANCHO // 2 - texto_ingresa.get_width() // 2, 200))

        input_render = fuente.render(nombre + "|", True, BLANCO)
        pantalla.blit(input_render, (ANCHO // 2 - input_render.get_width() // 2, 250))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre.strip():
                        from .funciones_ranking import guardar_ranking
                        guardar_ranking(nombre.strip(), movimientos)
                        ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 20:
                        nombre += evento.unicode

        