import pygame
import sys # Para sys.exit()
from paquete.constantes import (
    PALOS, VALORES, VERDE, ORIGEN_X, ORIGEN_Y, ESPACIADO_X, ESPACIADO_Y,
    MAZO_RECT, FUNDACION_RECTS, BOTON_SIGUIENTE_RECT, BOTON_VOLVER_RECT
)
from paquete.funciones_cartas import (
    siguiente_carta, mover_a_fundacion, mover_a_pila_en_indice,
    mover_a_pila_vacia, mover_grupo_de_pila_a_pila
)
from paquete.render_cartas import dibujar_escena_juego
from paquete.interfaz import toggle_musica, mostrar_mensaje_ganaste_y_guardar_ranking
from paquete.logica_juego import inicializar_estado_juego_cartas # Renombrada para mayor claridad

def _inicializar_estado_juego_completo(pantalla, fuente, reverso, imagenes_cartas,
                                     icono_sonido, icono_silencio, boton_sonido_rect,
                                     imagen_boton_volver, imagen_boton_siguiente):
    """
    Inicializa el diccionario completo del estado del juego.
    """
    pilas, mazo, fundaciones = inicializar_estado_juego_cartas()

    estado = {
        "pantalla": pantalla,
        "fuente": fuente,
        "reverso": reverso,
        "imagenes_cartas": imagenes_cartas,
        "icono_sonido": icono_sonido,
        "icono_silencio": icono_silencio,
        "boton_sonido_rect": boton_sonido_rect,
        "imagen_boton_volver": imagen_boton_volver,
        "imagen_boton_siguiente": imagen_boton_siguiente,
        "pilas": pilas,
        "mazo": mazo,
        "fundaciones": fundaciones,
        "indice_mazo": 0,
        "carta_visible": mazo[0] if mazo else None,
        "carta_seleccionada": None,
        "seleccion_visible": None,
        "musica_activada": True, # Se inicializa al entrar al juego
        "icono_actual": icono_sonido, # Se inicializa al entrar al juego
        "movimientos": 0,
        "corriendo": True # Flag para controlar el bucle principal del juego
    }
    return estado

def _manejar_clic_raton(pos, estado_juego):
    """
    Función interna para manejar los clics del ratón, actualizando el estado del juego.
    """
    # Desempaquetar el estado del juego para facilitar el acceso
    pantalla = estado_juego["pantalla"]
    pilas = estado_juego["pilas"]
    mazo = estado_juego["mazo"]
    fundaciones = estado_juego["fundaciones"]
    indice_mazo = estado_juego["indice_mazo"]
    carta_visible = estado_juego["carta_visible"]
    carta_seleccionada = estado_juego["carta_seleccionada"]
    seleccion_visible = estado_juego["seleccion_visible"]
    musica_activada = estado_juego["musica_activada"]
    icono_actual = estado_juego["icono_actual"]
    boton_sonido_rect = estado_juego["boton_sonido_rect"]
    imagen_boton_volver = estado_juego["imagen_boton_volver"]
    imagen_boton_siguiente = estado_juego["imagen_boton_siguiente"]
    icono_sonido = estado_juego["icono_sonido"]
    icono_silencio = estado_juego["icono_silencio"]
    movimientos = estado_juego["movimientos"]
    reverso = estado_juego["reverso"]
    imagenes_cartas = estado_juego["imagenes_cartas"]

    if boton_sonido_rect.collidepoint(pos):
        musica_activada, icono_actual = toggle_musica(musica_activada, icono_sonido, icono_silencio)
        estado_juego["musica_activada"] = musica_activada
        estado_juego["icono_actual"] = icono_actual
        # Se redibuja la escena para actualizar el icono
        dibujar_escena_juego(
            pantalla, pilas, carta_visible, fundaciones, icono_actual,
            boton_sonido_rect, imagen_boton_siguiente, BOTON_SIGUIENTE_RECT,
            imagen_boton_volver, BOTON_VOLVER_RECT,
            carta_seleccionada, seleccion_visible,
            reverso, imagenes_cartas
        )
        return # Se manejó el evento

    if BOTON_VOLVER_RECT.collidepoint(pos):
        estado_juego["corriendo"] = False # Marcar para salir del bucle de juego
        return # Se manejó el evento

    if BOTON_SIGUIENTE_RECT.collidepoint(pos):
        if mazo:
            indice_mazo = (indice_mazo + 1) % len(mazo)
            estado_juego["indice_mazo"] = indice_mazo
            # La carta visible se actualizará en el siguiente ciclo del bucle principal
        return # Se manejó el evento

    # Lógica para seleccionar carta del mazo
    if carta_visible and pygame.Rect(50, 20, 80, 120).collidepoint(pos):
        estado_juego["carta_seleccionada"] = {"origen": "mazo", "carta": carta_visible}
        estado_juego["seleccion_visible"] = pygame.Rect(50, 20, 80, 120)
        return # Se manejó el evento

    # Lógica para intentar mover carta del mazo a fundación o pila
    if MAZO_RECT.collidepoint(pos):
        if mazo:
            carta_actual_mazo, nuevo_indice_mazo = siguiente_carta(mazo, indice_mazo)
            se_movio = False
            if mover_a_fundacion(carta_actual_mazo, fundaciones, PALOS):
                movimientos += 1
                se_movio = True
            elif mover_a_pila_en_indice(carta_actual_mazo, pilas) or mover_a_pila_vacia(carta_actual_mazo, pilas):
                movimientos += 1
                se_movio = True

            if se_movio:
                mazo.pop(indice_mazo)
                # Ajustar el índice si el mazo se acorta y el índice está fuera de rango
                estado_juego["indice_mazo"] = indice_mazo % len(mazo) if mazo else 0
            else:
                estado_juego["indice_mazo"] = nuevo_indice_mazo # Avanzar a la siguiente carta si no se movió
            estado_juego["movimientos"] = movimientos
            estado_juego["carta_visible"] = mazo[estado_juego["indice_mazo"]] if mazo else None
        return # Se manejó el evento

    # Lógica de movimiento de carta seleccionada
    if carta_seleccionada:
        carta_a_mover = carta_seleccionada["carta"]

        # Intentar mover a fundación
        for i, rect in enumerate(FUNDACION_RECTS):
            if rect.collidepoint(pos):
                if mover_a_fundacion(carta_a_mover, fundaciones, PALOS):
                    movimientos += 1
                    if carta_seleccionada["origen"] == "pila":
                        idx = carta_seleccionada["indice"]
                        ocultas, visibles = pilas[idx]
                        visibles.remove(carta_a_mover)
                        if not visibles and ocultas:
                            nueva_visible = ocultas.pop()
                            pilas[idx] = (ocultas, [nueva_visible])
                    elif carta_seleccionada["origen"] == "mazo":
                        mazo.pop(indice_mazo)
                        estado_juego["indice_mazo"] = indice_mazo % len(mazo) if mazo else 0
                        estado_juego["carta_visible"] = None
                    estado_juego["movimientos"] = movimientos
                    estado_juego["carta_seleccionada"] = None
                    estado_juego["seleccion_visible"] = None
                    return # Se manejó el evento

        # Intentar mover de mazo a pila (si la carta seleccionada es del mazo)
        if carta_seleccionada["origen"] == "mazo":
            for i, (ocultas, visibles) in enumerate(pilas):
                x = ORIGEN_X + i * ESPACIADO_X
                y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + (len(visibles) * ESPACIADO_Y if visibles else 0)
                rect_destino_pila = pygame.Rect(x, y, 80, 120)
                if rect_destino_pila.collidepoint(pos):
                    if mover_a_pila_en_indice(carta_a_mover, pilas[i]):
                        movimientos += 1
                        mazo.pop(indice_mazo)
                        estado_juego["indice_mazo"] = indice_mazo % len(mazo) if mazo else 0
                        estado_juego["movimientos"] = movimientos
                        estado_juego["carta_seleccionada"] = None
                        estado_juego["seleccion_visible"] = None
                        estado_juego["carta_visible"] = mazo[estado_juego["indice_mazo"]] if mazo else None
                        return # Se manejó el evento

        # Intentar mover de pila a pila (si la carta seleccionada es de una pila)
        if carta_seleccionada["origen"] == "pila":
            origen_idx = carta_seleccionada["indice"]
            carta_idx_en_pila = pilas[origen_idx][1].index(carta_a_mover)

            for i, (ocultas, visibles) in enumerate(pilas):
                x = ORIGEN_X + i * ESPACIADO_X
                y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + (len(visibles) * ESPACIADO_Y if visibles else 0)
                rect_destino_pila = pygame.Rect(x, y, 80, 120)
                if rect_destino_pila.collidepoint(pos):
                    if mover_grupo_de_pila_a_pila(pilas, origen_idx, carta_idx_en_pila, i):
                        movimientos += 1
                        estado_juego["movimientos"] = movimientos
                        estado_juego["carta_seleccionada"] = None
                        estado_juego["seleccion_visible"] = None
                        return # Se manejó el evento
        
        # Si la carta estaba seleccionada y no se pudo mover, deseleccionarla
        estado_juego["carta_seleccionada"] = None
        estado_juego["seleccion_visible"] = None
        return # Se manejó el evento de deselección

    # Lógica para seleccionar una carta de una pila (si no había nada seleccionado)
    for i, (ocultas, visibles) in enumerate(pilas):
        x = ORIGEN_X + i * ESPACIADO_X
        y_inicial_pila = ORIGEN_Y + len(ocultas) * ESPACIADO_Y
        for j, carta in enumerate(visibles):
            rect_carta = pygame.Rect(x, y_inicial_pila + j * ESPACIADO_Y, 80, 120)
            if rect_carta.collidepoint(pos):
                estado_juego["carta_seleccionada"] = {
                    "origen": "pila",
                    "indice": i,
                    "carta": carta,
                    "grupo": visibles[j:]
                }
                estado_juego["seleccion_visible"] = pygame.Rect(
                    x, y_inicial_pila + j * ESPACIADO_Y, 80, 120 + ESPACIADO_Y * (len(visibles[j:]) - 1)
                )
                return # Se manejó el evento

def _manejar_eventos_juego(estado_juego):
    """
    Maneja todos los eventos del juego, actualizando el estado_juego.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado_juego["corriendo"] = False
            sys.exit() # Salir completamente del programa
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            estado_juego["corriendo"] = False # Marcar para salir del bucle de juego
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            _manejar_clic_raton(evento.pos, estado_juego)

def ejecutar_bucle_juego(pantalla, fuente, reverso, imagenes_cartas,
                         icono_sonido, icono_silencio, boton_sonido_rect,
                         imagen_boton_volver, imagen_boton_siguiente):
    """
    Contiene el bucle principal del juego.
    """
    estado_juego = _inicializar_estado_juego_completo(
        pantalla, fuente, reverso, imagenes_cartas,
        icono_sonido, icono_silencio, boton_sonido_rect,
        imagen_boton_volver, imagen_boton_siguiente
    )
    
    while estado_juego["corriendo"]:
        # Actualizar la carta visible del mazo en cada ciclo
        if estado_juego["mazo"] and estado_juego["indice_mazo"] < len(estado_juego["mazo"]):
            estado_juego["carta_visible"] = estado_juego["mazo"][estado_juego["indice_mazo"]]
        else:
            estado_juego["carta_visible"] = None

        dibujar_escena_juego(
            estado_juego["pantalla"], estado_juego["pilas"], estado_juego["carta_visible"], estado_juego["fundaciones"],
            estado_juego["icono_actual"], estado_juego["boton_sonido_rect"],
            estado_juego["imagen_boton_siguiente"], BOTON_SIGUIENTE_RECT,
            estado_juego["imagen_boton_volver"], BOTON_VOLVER_RECT,
            estado_juego["carta_seleccionada"], estado_juego["seleccion_visible"],
            estado_juego["reverso"], estado_juego["imagenes_cartas"]
        )

        # Verificar condición de victoria
        if sum(len(f) for f in estado_juego["fundaciones"]) == 40:
            mostrar_mensaje_ganaste_y_guardar_ranking(
                estado_juego["pantalla"], estado_juego["fuente"], estado_juego["movimientos"],
                estado_juego["imagen_boton_volver"], BOTON_VOLVER_RECT
            )
            estado_juego["corriendo"] = False # Termina el juego al ganar
            continue # Salta el manejo de eventos para este ciclo final

        _manejar_eventos_juego(estado_juego)