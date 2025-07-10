import pygame
import sys
from .constantes import BLANCO, AZUL, NEGRO
from .funciones_ranking import guardar_ranking

def toggle_musica(musica_activada, icono_sonido, icono_silencio):
    """
    Activa o pausa la música de fondo del juego y devuelve el nuevo estado junto al ícono actualizado.

    Args:
        musica_activada (bool): Estado actual de la música (True si está sonando).
        icono_sonido (pygame.Surface): Imagen del ícono de sonido.
        icono_silencio (pygame.Surface): Imagen del ícono de silencio.

    Returns:
        tuple: (nuevo_estado, nuevo_icono)
            nuevo_estado (bool): True si la música queda activada, False si se pausa.
            nuevo_icono (pygame.Surface): Imagen del ícono actualizado según el nuevo estado.
    """
    if musica_activada:
        pygame.mixer.music.pause()
        return False, icono_silencio
    else:
        pygame.mixer.music.unpause()
        return True, icono_sonido


def dibujar_boton(pantalla, fuente, texto, x, y, ancho, alto):
    """
    Dibuja un botón rectangular con texto sobre la pantalla y devuelve su rectángulo.

    Args:
        pantalla (pygame.Surface): Superficie sobre la que se dibuja.
        fuente (pygame.font.Font): Fuente para renderizar el texto.
        texto (str): Texto que se mostrará sobre el botón.
        x (int): Coordenada horizontal del botón.
        y (int): Coordenada vertical del botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.

    Returns:
        pygame.Rect: Rectángulo del botón, útil para detectar clics.
    """
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, AZUL, rect)
    texto_render = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_render, (x + 10, y + 10))
    return rect

def mostrar_menu(pantalla, fuente, icono_actual, boton_sonido_rect):
    """
    Dibuja el menú principal del juego con su título, botones de opciones y el ícono de sonido/silencio.

    Args:
        pantalla (pygame.Surface): Superficie de Pygame donde se dibujará el menú.
        fuente (pygame.font.Font): Fuente usada para los textos del menú.
        icono_actual (pygame.Surface): Imagen del ícono actual (sonido o silencio).
        boton_sonido_rect (pygame.Rect): Rectángulo para posicionar y detectar clic sobre el ícono.

    Returns:
        dict: Diccionario con los rectángulos de los botones interactivos:
            {
                "jugar": pygame.Rect,
                "ranking": pygame.Rect,
                "salir": pygame.Rect
            }
    """
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

def mostrar_textos(pantalla, fuente, lista_textos, imagen_boton_volver, BOTON_VOLVER_RECT):#muestra el ranking
    """
    Muestra una lista de líneas de texto en pantalla, una debajo de otra, y dibuja el botón 'Volver'.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibujan los textos.
        fuente (pygame.font.Font): Fuente utilizada para renderizar los textos.
        lista_textos (list): Lista de strings, cada uno representando una línea a mostrar.
        imagen_boton_volver (pygame.Surface): Imagen del botón 'Volver'.
        BOTON_VOLVER_RECT (pygame.Rect): Rectángulo del botón para su ubicación y detección de clics.

    Returns:
        None
    """
    pantalla.fill(NEGRO)
    y = 50
    for texto in lista_textos:
        linea = fuente.render(texto, True, BLANCO)
        pantalla.blit(linea, (50, y))
        y += 30
    pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

def mostrar_mensaje_ganaste_y_guardar_ranking(pantalla, fuente, movimientos, imagen_boton_volver, BOTON_VOLVER_RECT):
    """
    Muestra el mensaje de victoria cuando el jugador gana, permite ingresar su nombre,
    y guarda su puntaje en el ranking.

    Args:
        pantalla (pygame.Surface): Superficie del juego donde se dibuja el mensaje.
        fuente (pygame.font.Font): Fuente usada para los textos.
        movimientos (int): Cantidad de movimientos que realizó el jugador.
        imagen_boton_volver (pygame.Surface): Imagen del botón 'Volver'.
        BOTON_VOLVER_RECT (pygame.Rect): Rectángulo para posicionar el botón 'Volver'.

    Returns:
        None
    """
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