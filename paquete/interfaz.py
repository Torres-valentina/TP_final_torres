import pygame
import sys
from .funciones_cartas import *
from .funciones_ranking import obtener_estado_ranking
from .render_cartas import *
from .constantes import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sonidos/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ---------- TÍTULO E ÍCONO DE LA VENTANA ----------
pygame.display.set_caption("Solitario")
icono = pygame.image.load("imagenes/icono.png") 
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
fuente = pygame.font.SysFont("consolas", 24)
inicializar_imagenes()

# ---------- BOTÓN DE SONIDO ----------
icono_sonido = pygame.image.load("sonidos/sonido.png")
icono_silencio = pygame.image.load("sonidos/silencio.png")
icono_sonido = pygame.transform.scale(icono_sonido, (40, 40))
icono_silencio = pygame.transform.scale(icono_silencio, (40, 40))
icono_actual = icono_sonido
boton_sonido_rect = icono_sonido.get_rect(topright=(ANCHO - 10, 10))

musica_activada = True

# ---------- ÁREAS INTERACTIVAS ----------
MAZO_RECT = pygame.Rect(50, 20, 80, 120)
FUNDACION_RECTS = [pygame.Rect(400 + i * 100, 20, 80, 120) for i in range(4)]

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

def mostrar_mensaje_ganaste_y_guardar_ranking(movimientos):
    pantalla.fill(NEGRO)
    texto = fuente.render("¡Ganaste! 🎉", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 40))
    texto2 = fuente.render(f"Movimientos: {movimientos}", True, BLANCO)
    pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2))
    texto3 = fuente.render("Escribí tu nombre en la consola...", True, BLANCO)
    pantalla.blit(texto3, (ANCHO // 2 - texto3.get_width() // 2, ALTO // 2 + 40))
    pygame.display.flip()

    print("\n¡Ganaste! 🎉")
    print(f"Movimientos: {movimientos}")
    nombre = input("Ingresá tu nombre para el ranking: ")

    from .funciones_ranking import guardar_ranking
    guardar_ranking(nombre, movimientos)

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                esperando = False

def loop_menu():
    botones = mostrar_menu()
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_sonido_rect.collidepoint(evento.pos):
                    toggle_musica()
                    botones = mostrar_menu()
                    pygame.display.flip()
                    continue
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
    global icono_actual  # para el botón de sonido
    baraja = barajar_baraja(crear_baraja())
    pilas, mazo = repartir_cartas(baraja)
    fundaciones = [[], [], [], []]
    indice_mazo = 0
    carta_visible = None
    carta_seleccionada = None
    movimientos = 0
    corriendo = True

    while corriendo:
        # Actualizar carta visible del mazo
        if len(mazo) == 0:
            carta_visible = None
        elif indice_mazo >= len(mazo):
            indice_mazo = 0
            carta_visible = None
        else:
            carta_visible = mazo[indice_mazo]

        # Dibujar todo
        dibujar_pilas_con_imagenes(pantalla, pilas, carta_visible, fundaciones)
        pantalla.blit(icono_actual, boton_sonido_rect)
        pygame.display.flip()

        # Condición de victoria
        if sum(len(f) for f in fundaciones) == 40:
            mostrar_mensaje_ganaste_y_guardar_ranking(movimientos)
            corriendo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos

                # Botón de sonido
                if boton_sonido_rect.collidepoint(pos):
                    toggle_musica()
                    continue

                # Seleccionar grupo de cartas desde una pila
                for i, (ocultas, visibles) in enumerate(pilas):
                    x = ORIGEN_X + i * ESPACIADO_X
                    y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y

                    for j, carta in enumerate(visibles):
                        rect = pygame.Rect(x, y + j * ESPACIADO_Y, 80, 120)
                        if rect.collidepoint(pos):
                            carta_seleccionada = {
                                "origen": "pila",
                                "indice": i,
                                "carta": carta,
                                "grupo": visibles[j:]
                            }
                            break

                # Mover grupo a otra pila
                if carta_seleccionada and carta_seleccionada["origen"] == "pila":
                    for i, (ocultas, visibles) in enumerate(pilas):
                        x = ORIGEN_X + i * ESPACIADO_X
                        y = ORIGEN_Y + (len(ocultas) + len(visibles)) * ESPACIADO_Y
                        rect = pygame.Rect(x, y, 80, 120)

                        if rect.collidepoint(pos):
                            grupo = carta_seleccionada["grupo"]
                            carta = grupo[0]

                            if mover_a_pila(carta, pilas) or mover_a_pila_vacia(carta, pilas):
                                movimientos += 1
                                origen = carta_seleccionada["indice"]
                                _, visibles_origen = pilas[origen]

                                for c in grupo:
                                    if c in visibles_origen:
                                        visibles_origen.remove(c)

                                if not visibles_origen and pilas[origen][0]:
                                    nueva_visible = pilas[origen][0].pop()
                                    pilas[origen] = (pilas[origen][0], [nueva_visible])

                            carta_seleccionada = None

                # Mover carta seleccionada a fundación
                if carta_seleccionada:
                    for i, rect in enumerate(FUNDACION_RECTS):
                        if rect.collidepoint(pos):
                            carta = carta_seleccionada["carta"]

                            if mover_a_fundacion(carta, fundaciones):
                                movimientos += 1
                                if carta_seleccionada["origen"] == "pila":
                                    indice = carta_seleccionada["indice"]
                                    ocultas, visibles = pilas[indice]

                                    if carta in visibles:
                                        visibles.remove(carta)

                                    if not visibles and ocultas:
                                        nueva_visible = ocultas.pop()
                                        pilas[indice] = (ocultas, [nueva_visible])

                                carta_seleccionada = None
                                break

                # Clic en el mazo
                if MAZO_RECT.collidepoint(pos):
                    if len(mazo) == 0:
                        continue

                    carta, nuevo_indice = siguiente_carta(mazo, indice_mazo)

                    se_movio = False
                    if mover_a_fundacion(carta, fundaciones):
                        movimientos += 1
                        se_movio = True
                    elif mover_a_pila(carta, pilas) or mover_a_pila_vacia(carta, pilas):
                        movimientos += 1
                        se_movio = True

                    if se_movio:
                        mazo.pop(indice_mazo)
                    else:
                        indice_mazo = nuevo_indice
