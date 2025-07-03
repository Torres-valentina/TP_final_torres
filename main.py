import pygame
import sys
from paquete.constantes import *
from paquete.funciones_cartas import *
from paquete.funciones_ranking import *
from paquete.complementarias import *
from paquete.render_cartas import *
from paquete.interfaz import mostrar_menu, mostrar_textos, toggle_musica
from paquete.variables_pygame import *
from paquete.interfaz import mostrar_mensaje_ganaste_y_guardar_ranking
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

                        pantalla.fill(NEGRO)
                        mostrar_textos(textos)
                        pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)
                        pygame.display.flip()

                    botones = mostrar_menu()
                    pygame.display.flip()

                elif botones["salir"].collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

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
    BOTON_SIGUIENTE_RECT = pygame.Rect(150, 50, 80, 40)

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

if __name__ == "__main__":
    loop_menu()
