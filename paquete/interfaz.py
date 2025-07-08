import pygame
import sys
from .constantes import BLANCO, AZUL, NEGRO
from .funciones_ranking import guardar_ranking  

def toggle_musica(musica_activada, icono_sonido, icono_silencio):
    if musica_activada:
        pygame.mixer.music.pause()
        return False, icono_silencio
    else:
        pygame.mixer.music.unpause()
        return True, icono_sonido


def dibujar_boton(pantalla, fuente, texto, x, y, ancho, alto):
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, AZUL, rect)
    texto_render = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_render, (x + 10, y + 10))
    return rect

def mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect):
    pantalla.fill(NEGRO)
    titulo = fuente.render("Solitario - Menú Principal", True, BLANCO)
    pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 50))

    boton_jugar = dibujar_boton(pantalla, fuente, "Jugar", 300, 150, 200, 50)
    boton_ranking = dibujar_boton(pantalla, fuente, "Ver Ranking", 300, 230, 200, 50)
    boton_salir = dibujar_boton(pantalla, fuente, "Salir", 300, 310, 200, 50)

    pantalla.blit(icono_actual, boton_sonido_rect)

    return {
        "jugar": boton_jugar,
        "ranking": boton_ranking,
        "salir": boton_salir
    }

def mostrar_textos(pantalla, fuente, lista_textos, imagen_boton_volver, BOTON_VOLVER_RECT):
    pantalla.fill(NEGRO)
    y = 50
    for texto in lista_textos:
        linea = fuente.render(texto, True, BLANCO)
        pantalla.blit(linea, (50, y))
        y += 30
    pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

def mostrar_mensaje_ganaste_y_guardar_ranking(pantalla, fuente, movimientos, imagen_boton_volver, BOTON_VOLVER_RECT):
    texto_ganaste = fuente.render("¡Ganaste!", True, BLANCO)
    texto_movs = fuente.render(f"Movimientos: {movimientos}", True, BLANCO)
    texto_ingresa = fuente.render("Ingresá tu nombre:", True, BLANCO)

    nombre = ""
    ingresando = True

    while ingresando:
        pantalla.fill(NEGRO)
        pantalla.blit(texto_ganaste, (pantalla.get_width() // 2 - texto_ganaste.get_width() // 2, 100))
        pantalla.blit(texto_movs, (pantalla.get_width() // 2 - texto_movs.get_width() // 2, 150))
        pantalla.blit(texto_ingresa, (pantalla.get_width() // 2 - texto_ingresa.get_width() // 2, 200))

        input_render = fuente.render(nombre + "|", True, BLANCO)
        pantalla.blit(input_render, (pantalla.get_width() // 2 - input_render.get_width() // 2, 250))
        pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip():
                    guardar_ranking(nombre.strip(), movimientos)
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 20:
                    nombre += evento.unicode
