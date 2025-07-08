import pygame
from paquete.constantes import *
from paquete.funciones_cartas import *
from paquete.render_cartas import *
from paquete.interfaz import toggle_musica

def inicializar_estado_juego():
    """
    Inicializa las pilas, mazo y fundaciones para comenzar una nueva partida.
    """
    baraja = barajar_baraja(crear_baraja(PALOS, VALORES))
    pilas, mazo = repartir_cartas(baraja)
    fundaciones = [[] for _ in range(4)]
    return pilas, mazo, fundaciones

def dibujar_escena_juego(pantalla, pilas, carta_visible, fundaciones,
                         icono_actual, boton_sonido_rect,
                         imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                         imagen_boton_volver, BOTON_VOLVER_RECT,
                         carta_seleccionada, seleccion_visible,
                         reverso, imagenes_cartas, carta_mazo):
    """
    Dibuja la escena completa del juego en pantalla.
    """
    pantalla.fill(VERDE)
    dibujar_pilas_con_imagenes(pantalla, pilas, reverso, imagenes_cartas, carta_mazo, fundaciones)
    pantalla.blit(icono_actual, boton_sonido_rect)
    pantalla.blit(imagen_boton_siguiente, BOTON_SIGUIENTE_RECT)
    pantalla.blit(imagen_boton_volver, BOTON_VOLVER_RECT)

    if carta_seleccionada and seleccion_visible:
        pygame.draw.rect(pantalla, (255, 0, 0), seleccion_visible, 3)

    pygame.display.flip()

def manejar_eventos(pantalla, fuente, eventos, pilas, mazo, fundaciones,
                    indice_mazo, carta_visible, carta_seleccionada, seleccion_visible,
                    musica_activada, icono_actual, boton_sonido_rect, imagen_boton_volver,
                    BOTON_VOLVER_RECT, imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                    MAZO_RECT, FUNDACION_RECTS, movimientos,
                    icono_sonido, icono_silencio,
                    reverso, imagenes_cartas):
    """
    Maneja todos los eventos del juego, incluyendo clics, teclas y acciones del jugador.
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False, indice_mazo, carta_visible, carta_seleccionada, seleccion_visible, musica_activada, icono_actual, movimientos

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos

            if boton_sonido_rect.collidepoint(pos):
                musica_activada, icono_actual = toggle_musica(musica_activada, icono_sonido, icono_silencio)
                dibujar_escena_juego(
                    pantalla, pilas, carta_visible, fundaciones, icono_actual,
                    boton_sonido_rect, imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
                    imagen_boton_volver, BOTON_VOLVER_RECT,
                    carta_seleccionada, seleccion_visible,
                    reverso, imagenes_cartas, carta_visible
                )
                continue

            if BOTON_VOLVER_RECT.collidepoint(pos):
                return False, indice_mazo, carta_visible, carta_seleccionada, seleccion_visible, musica_activada, icono_actual, movimientos

            if BOTON_SIGUIENTE_RECT.collidepoint(pos):
                if mazo:
                    indice_mazo = (indice_mazo + 1) % len(mazo)
                continue

            if carta_visible and pygame.Rect(50, 20, 80, 120).collidepoint(pos):
                carta_seleccionada = {"origen": "mazo", "carta": carta_visible}
                seleccion_visible = pygame.Rect(50, 20, 80, 120)
                continue

            if MAZO_RECT.collidepoint(pos):
                if mazo:
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

            if carta_seleccionada:
                carta = carta_seleccionada["carta"]

                for i, rect in enumerate(FUNDACION_RECTS):
                    if rect.collidepoint(pos):
                        if mover_a_fundacion(carta, fundaciones, PALOS):
                            movimientos += 1
                            if carta_seleccionada["origen"] == "pila":
                                idx = carta_seleccionada["indice"]
                                ocultas, visibles = pilas[idx]
                                visibles.remove(carta)
                                if not visibles and ocultas:
                                    nueva_visible = ocultas.pop()
                                    pilas[idx] = (ocultas, [nueva_visible])
                            elif carta_seleccionada["origen"] == "mazo":
                                mazo.pop(indice_mazo)
                                carta_visible = None
                            carta_seleccionada = None
                            seleccion_visible = None
                        break

                if carta_seleccionada and carta_seleccionada["origen"] == "mazo":
                    for i, (ocultas, visibles) in enumerate(pilas):
                        x = ORIGEN_X + i * ESPACIADO_X
                        y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + len(visibles) * ESPACIADO_Y if visibles else ORIGEN_Y + len(ocultas) * ESPACIADO_Y
                        rect = pygame.Rect(x, y, 80, 120)
                        if rect.collidepoint(pos):
                            if mover_a_pila_en_indice(carta, pilas[i]):
                                movimientos += 1
                                mazo.pop(indice_mazo)
                                indice_mazo %= len(mazo) if mazo else 1
                                carta_seleccionada = None
                                seleccion_visible = None
                            break

                if carta_seleccionada and carta_seleccionada["origen"] == "pila":
                    origen = carta_seleccionada["indice"]
                    carta = carta_seleccionada["carta"]
                    carta_idx = pilas[origen][1].index(carta)

                    for i, (ocultas, visibles) in enumerate(pilas):
                        x = ORIGEN_X + i * ESPACIADO_X
                        y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + len(visibles) * ESPACIADO_Y if visibles else ORIGEN_Y
                        rect = pygame.Rect(x, y, 80, 120)
                        if rect.collidepoint(pos):
                            if mover_grupo_de_pila_a_pila(pilas, origen, carta_idx, i):
                                movimientos += 1
                            break
                    carta_seleccionada = None
                    seleccion_visible = None
                    break

                carta_seleccionada = None
                seleccion_visible = None
                break

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
                            x, y + j * ESPACIADO_Y, 80, 120 + ESPACIADO_Y * (len(visibles[j:]) - 1)
                        )
                        break

    return True, indice_mazo, carta_visible, carta_seleccionada, seleccion_visible, musica_activada, icono_actual, movimientos
