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
#----------------------BOTON VOLVER----------------------------------
imagen_boton_volver = pygame.image.load("imagenes/volver.png")
imagen_boton_volver = pygame.transform.scale(imagen_boton_volver, (80, 80))
BOTON_VOLVER_RECT = imagen_boton_volver.get_rect(topleft=(10, ALTO - 80))

#----------------------BOTON SIGUIENTE------------------------------------
imagen_boton_siguiente = pygame.image.load("imagenes/siguiente.png")
imagen_boton_siguiente = pygame.transform.scale(imagen_boton_siguiente, (80, 80))

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

                    mostrando_ranking = True
                    while mostrando_ranking:
                        for evento_ranking in pygame.event.get():
                            if evento_ranking.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif evento_ranking.type == pygame.MOUSEBUTTONDOWN:
                                if BOTON_VOLVER_RECT.collidepoint(evento_ranking.pos):
                                    mostrando_ranking = False

                        pantalla.fill(NEGRO)  # Redibujar fondo para que se vea todo
                        mostrar_textos(textos)  # Mostrar el ranking
                        pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)  # Mostrar botón volver
                        pygame.display.flip()

                    botones = mostrar_menu()
                    pygame.display.flip()

                elif botones["salir"].collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

def mover_grupo_de_pila_a_pila(pilas, origen_idx, carta_idx, destino_idx):
    ocultas_origen, visibles_origen = pilas[origen_idx]
    cartas_a_mover = visibles_origen[carta_idx:]

    if not cartas_a_mover:
        return False

    valor_mover, palo_mover = cartas_a_mover[0]
    ocultas_destino, visibles_destino = pilas[destino_idx]

    if not visibles_destino:
        if valor_mover != 10:
            return False
        else:
            pilas[destino_idx] = (ocultas_destino, visibles_destino + cartas_a_mover)
            pilas[origen_idx] = (ocultas_origen, visibles_origen[:carta_idx])
    else:
        valor_tope, palo_tope = visibles_destino[-1]

        if valor_mover == valor_tope - 1 and palo_mover != palo_tope:
            pilas[destino_idx] = (ocultas_destino, visibles_destino + cartas_a_mover)
            pilas[origen_idx] = (ocultas_origen, visibles_origen[:carta_idx])
        else:
            return False

    if not pilas[origen_idx][1] and pilas[origen_idx][0]:
        nueva_visible = pilas[origen_idx][0].pop()
        pilas[origen_idx] = (pilas[origen_idx][0], [nueva_visible])

    return True

def loop_juego():
    global icono_actual
    baraja = barajar_baraja(crear_baraja(PALOS, VALORES))
    pilas, mazo = repartir_cartas(baraja)
    fundaciones = [[], [], [], []]
    indice_mazo = 0
    carta_visible = None
    carta_seleccionada = None
    seleccion_visible = None
    movimientos = 0
    corriendo = True
    BOTON_SIGUIENTE_RECT = pygame.Rect(150, 50, 80, 40)  # Ajustá posición/tamaño a gusto

    while corriendo:
        # Actualizar carta visible del mazo
        if len(mazo) == 0:
            carta_visible = None
        elif indice_mazo >= len(mazo):
            indice_mazo = 0
            carta_visible = None
        else:
            carta_visible = mazo[indice_mazo]

        # DIBUJAR
        dibujar_pilas_con_imagenes(pantalla, pilas, carta_visible, fundaciones)
        pantalla.blit(icono_actual, boton_sonido_rect)
        pantalla.blit(imagen_boton_siguiente, BOTON_SIGUIENTE_RECT)
        pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)



        # DIBUJAR BORDE DE SELECCIÓN
        if carta_seleccionada and seleccion_visible:
            pygame.draw.rect(pantalla, (255, 0, 0), seleccion_visible, 3)

        pygame.display.flip()

        # VICTORIA
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

                if BOTON_VOLVER_RECT.collidepoint(pos):
                    corriendo = False  # sale del juego y vuelve al menú
                    continue

                if BOTON_SIGUIENTE_RECT.collidepoint(pos):
                    if len(mazo) > 0:
                        indice_mazo += 1
                        if indice_mazo >= len(mazo):
                            indice_mazo = 0
                    continue  # para que no siga procesando otros clics ese frame

                # Seleccionar carta del mazo
                if carta_visible:
                    rect_mazo = pygame.Rect(50, 20, 80, 120)
                    if rect_mazo.collidepoint(pos):
                        carta_seleccionada = {
                            "origen": "mazo",
                            "carta": carta_visible,
                        }
                        seleccion_visible = rect_mazo
                        continue

                # Clic en el mazo
                if MAZO_RECT.collidepoint(pos):
                    if len(mazo) == 0:
                        continue
                    carta, nuevo_indice = siguiente_carta(mazo, indice_mazo)

                    se_movio = False
                    if mover_a_fundacion(carta, fundaciones, PALOS):
                        movimientos += 1
                        se_movio = True
                    elif mover_a_pila_en_indice(carta, pilas) or mover_a_pila_vacia(carta, pilas):
                        movimientos += 1
                        se_movio = True

                    if se_movio:
                        mazo.pop(indice_mazo)
                    else:
                        indice_mazo = nuevo_indice
                    continue

                # Si ya hay una selección activa
                    # Intentar mover a fundación
                    # Intentar mover a fundación
                if carta_seleccionada:
                    carta = carta_seleccionada["carta"]

                    for i, rect in enumerate(FUNDACION_RECTS):
                        if rect.collidepoint(pos):
                            if mover_a_fundacion(carta, fundaciones, PALOS):
                                movimientos += 1

                                if carta_seleccionada is not None and carta_seleccionada["origen"] == "pila":
                                    indice = carta_seleccionada["indice"]
                                    ocultas, visibles = pilas[indice]
                                    if carta in visibles:
                                        visibles.remove(carta)
                                    if not visibles and ocultas:
                                        nueva_visible = ocultas.pop()
                                        pilas[indice] = (ocultas, [nueva_visible])

                                elif carta_seleccionada["origen"] == "mazo":
                                    mazo.pop(indice_mazo)
                                    carta_visible = None

                                carta_seleccionada = None
                                seleccion_visible = None
                            break
                                                # Si la carta seleccionada viene del mazo, intentar mover a pilas
                        if carta_seleccionada is not None and carta_seleccionada["origen"] == "mazo":
                            for i, (ocultas, visibles) in enumerate(pilas):
                                x = ORIGEN_X + i * ESPACIADO_X
                                y = ORIGEN_Y
                                if visibles:
                                    y += len(ocultas) * ESPACIADO_Y + len(visibles) * ESPACIADO_Y
                                else:
                                    y += len(ocultas) * ESPACIADO_Y

                                rect = pygame.Rect(x, y, 80, 120)

                                if rect.collidepoint(pos):
                                    #  Esta es la corrección importante: pasar solo la pila específica
                                    if mover_a_pila_en_indice(carta_seleccionada["carta"], pilas[i]):
                                        movimientos += 1
                                        mazo.pop(indice_mazo)
                                        if indice_mazo >= len(mazo):
                                            indice_mazo = 0
                                        carta_seleccionada = None
                                        seleccion_visible = None
                                    break


                    # Intentar mover a otra pila
                    if carta_seleccionada is not None and carta_seleccionada["origen"] == "pila":
                        # Código para mover cartas entre pilas:
                        origen = carta_seleccionada["indice"]
                        # ... seguir con lógica de mover de una pila a otra
                        carta = carta_seleccionada["carta"]
                        carta_idx = pilas[origen][1].index(carta)

                        for i, (ocultas, visibles) in enumerate(pilas):
                            x = ORIGEN_X + i * ESPACIADO_X
                            if visibles:
                                y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + len(visibles) * ESPACIADO_Y
                            else:
                                y = ORIGEN_Y  # Si está vacía, el rect va más arriba

                            rect = pygame.Rect(x, y, 80, 120)

                            if rect.collidepoint(pos):
                                if mover_grupo_de_pila_a_pila(pilas, origen, carta_idx, i):
                                    movimientos += 1
                                break


                        if rect.collidepoint(pos):
                            if mover_grupo_de_pila_a_pila(pilas, origen, carta_idx, i):
                                movimientos += 1
                            carta_seleccionada = None
                            seleccion_visible = None
                            break  # salimos del evento

                    # Si no hizo ningún movimiento, deseleccionamos
                    carta_seleccionada = None
                    seleccion_visible = None
                    break  # clic vacío cancela

                # Si no había selección activa: detectar selección nueva
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
                            seleccion_visible = pygame.Rect(
                                x,
                                y + j * ESPACIADO_Y,
                                80,
                                120 + ESPACIADO_Y * (len(visibles[j:]) - 1)
                            )
                            break  # salimos del evento al seleccionar
