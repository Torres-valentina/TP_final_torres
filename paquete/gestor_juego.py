import pygame
import sys # Para sys.exit()
from paquete.constantes import (
    PALOS, VALORES, VERDE, ORIGEN_X, ORIGEN_Y, ESPACIADO_X, ESPACIADO_Y,
    MAZO_RECT, FUNDACION_RECTS, BOTON_SIGUIENTE_RECT, BOTON_VOLVER_RECT,
    TAM_CARTA # ASUME que TAM_CARTA está definido en constantes.py
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
                                       imagen_boton_volver, imagen_boton_siguiente,
                                       musica_activada_inicial, icono_actual_inicial): # <-- NUEVOS PARÁMETROS
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
        "musica_activada": musica_activada_inicial, # <-- USAR EL VALOR PASADO DEL MENÚ
        "icono_actual": icono_actual_inicial,       # <-- USAR EL VALOR PASADO DEL MENÚ
        "movimientos": 0,
        "corriendo": True # Flag para controlar el bucle principal del juego
    }
    return estado

# --- Funciones Auxiliares Modularizadas para el manejo de clics ---

def _manejar_clic_boton_control(pos, estado_juego):
    """
    Maneja los clics en los botones de control (Sonido, Volver, Siguiente).
    Devuelve True si se procesó un clic de botón, False en caso contrario.
    """
    if estado_juego["boton_sonido_rect"].collidepoint(pos):
        musica_activada, icono_actual = toggle_musica(
            estado_juego["musica_activada"],
            estado_juego["icono_sonido"],
            estado_juego["icono_silencio"]
        )
        estado_juego["musica_activada"] = musica_activada
        estado_juego["icono_actual"] = icono_actual
        # Se redibuja la escena para actualizar el icono
        dibujar_escena_juego(
            estado_juego["pantalla"], estado_juego["pilas"], estado_juego["carta_visible"], estado_juego["fundaciones"],
            estado_juego["icono_actual"], estado_juego["boton_sonido_rect"], estado_juego["imagen_boton_siguiente"],
            BOTON_SIGUIENTE_RECT, estado_juego["imagen_boton_volver"], BOTON_VOLVER_RECT,
            estado_juego["carta_seleccionada"], estado_juego["seleccion_visible"],
            estado_juego["reverso"], estado_juego["imagenes_cartas"]
        )
        return True

    if BOTON_VOLVER_RECT.collidepoint(pos):
        estado_juego["corriendo"] = False # Esto hará que el bucle del juego termine
        return True

    if BOTON_SIGUIENTE_RECT.collidepoint(pos):
        if estado_juego["mazo"]:
            estado_juego["indice_mazo"] = (estado_juego["indice_mazo"] + 1) % len(estado_juego["mazo"])
            estado_juego["carta_visible"] = estado_juego["mazo"][estado_juego["indice_mazo"]] # Actualizar carta visible
        return True
    return False

def _manejar_clic_mazo(pos, estado_juego):
    """
    Maneja los clics en el mazo (seleccionar carta visible o intentar mover la carta actual del mazo).
    Devuelve True si se procesó un clic relacionado con el mazo, False en caso contrario.
    """
    mazo = estado_juego["mazo"]
    indice_mazo = estado_juego["indice_mazo"]
    carta_visible = estado_juego["carta_visible"]
    fundaciones = estado_juego["fundaciones"]
    pilas = estado_juego["pilas"]
    movimientos = estado_juego["movimientos"]

    if carta_visible and pygame.Rect(MAZO_RECT.x, MAZO_RECT.y, TAM_CARTA[0], TAM_CARTA[1]).collidepoint(pos):
        estado_juego["carta_seleccionada"] = {"origen": "mazo", "carta": carta_visible}
        estado_juego["seleccion_visible"] = pygame.Rect(MAZO_RECT.x, MAZO_RECT.y, TAM_CARTA[0], TAM_CARTA[1])
        return True

    if MAZO_RECT.collidepoint(pos):
        if mazo:
            carta_actual_mazo = mazo[indice_mazo]
            
            se_movio = False
            if mover_a_fundacion(carta_actual_mazo, fundaciones, PALOS):
                movimientos += 1
                se_movio = True
            elif mover_a_pila_en_indice(carta_actual_mazo, pilas) or mover_a_pila_vacia(carta_actual_mazo, pilas):
                movimientos += 1
                se_movio = True

            if se_movio:
                mazo.pop(indice_mazo)
                estado_juego["indice_mazo"] = indice_mazo % len(mazo) if mazo else 0
            
            estado_juego["movimientos"] = movimientos
            estado_juego["carta_visible"] = mazo[estado_juego["indice_mazo"]] if mazo else None
        return True
    return False

def _eliminar_carta_de_origen(estado_juego, carta_seleccionada):
    """
    Elimina la carta (o grupo de cartas) de su origen original
    (mazo o pila) después de un movimiento exitoso.
    """
    if carta_seleccionada["origen"] == "pila":
        idx = carta_seleccionada["indice"]
        ocultas, visibles = estado_juego["pilas"][idx]
        carta_a_mover = carta_seleccionada["carta"]
        
        if carta_a_mover in visibles:
            idx_carta_a_mover_en_visibles = visibles.index(carta_a_mover)
            visibles_restantes = visibles[:idx_carta_a_mover_en_visibles]
            
            if not visibles_restantes and ocultas:
                nueva_visible = ocultas.pop()
                estado_juego["pilas"][idx] = (ocultas, [nueva_visible])
            else:
                estado_juego["pilas"][idx] = (ocultas, visibles_restantes)
        else:
            print("Advertencia: La carta seleccionada no se encontró en la pila visible para eliminar.")


    elif carta_seleccionada["origen"] == "mazo":
        indice_mazo = estado_juego["indice_mazo"]
        mazo = estado_juego["mazo"]
        if mazo and indice_mazo < len(mazo):
            mazo.pop(indice_mazo)
            estado_juego["indice_mazo"] = indice_mazo % len(mazo) if mazo else 0
            estado_juego["carta_visible"] = mazo[estado_juego["indice_mazo"]] if mazo else None
        else:
            estado_juego["carta_visible"] = None
            print("Advertencia: Intento de eliminar carta del mazo vacío o índice inválido.")


def _intentar_mover_a_fundacion(pos, estado_juego):
    """
    Intenta mover la carta seleccionada a una de las fundaciones.
    Devuelve True si el movimiento fue exitoso, False en caso contrario.
    """
    carta_seleccionada = estado_juego["carta_seleccionada"]
    carta_a_mover = carta_seleccionada["carta"]
    fundaciones = estado_juego["fundaciones"]
    movimientos = estado_juego["movimientos"]

    for i, rect in enumerate(FUNDACION_RECTS):
        if rect.collidepoint(pos):
            if mover_a_fundacion(carta_a_mover, fundaciones, PALOS):
                estado_juego["movimientos"] = movimientos + 1
                _eliminar_carta_de_origen(estado_juego, carta_seleccionada)
                estado_juego["carta_seleccionada"] = None
                estado_juego["seleccion_visible"] = None
                return True
    return False

def _intentar_mover_mazo_a_pila(pos, estado_juego):
    """
    Intenta mover la carta seleccionada (si es del mazo) a una pila.
    Devuelve True si el movimiento fue exitoso, False en caso contrario.
    """
    carta_seleccionada = estado_juego["carta_seleccionada"]
    if carta_seleccionada["origen"] != "mazo":
        return False

    carta_a_mover = carta_seleccionada["carta"]
    pilas = estado_juego["pilas"]
    movimientos = estado_juego["movimientos"]

    for i, (ocultas, visibles) in enumerate(pilas):
        x = ORIGEN_X + i * ESPACIADO_X
        y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + (len(visibles) * ESPACIADO_Y if visibles else 0)
        rect_destino_pila = pygame.Rect(x, y, TAM_CARTA[0], TAM_CARTA[1])

        if rect_destino_pila.collidepoint(pos):
            if mover_a_pila_en_indice(carta_a_mover, pilas[i]):
                estado_juego["movimientos"] = movimientos + 1
                _eliminar_carta_de_origen(estado_juego, carta_seleccionada)
                estado_juego["carta_seleccionada"] = None
                estado_juego["seleccion_visible"] = None
                return True
    return False

def _intentar_mover_pila_a_pila(pos, estado_juego):
    """
    Intenta mover la carta seleccionada (si es de una pila) a otra pila.
    Devuelve True si el movimiento fue exitoso, False en caso contrario.
    """
    carta_seleccionada = estado_juego["carta_seleccionada"]
    if carta_seleccionada["origen"] != "pila":
        return False

    origen_idx = carta_seleccionada["indice"]
    carta_a_mover = carta_seleccionada["carta"]
    pilas = estado_juego["pilas"]

    if carta_a_mover not in pilas[origen_idx][1]:
        print("Advertencia: Carta seleccionada de pila no encontrada en su pila de origen para mover.")
        estado_juego["carta_seleccionada"] = None
        estado_juego["seleccion_visible"] = None
        return False

    carta_idx_en_pila = pilas[origen_idx][1].index(carta_a_mover)
    movimientos = estado_juego["movimientos"]

    for i, (ocultas, visibles) in enumerate(pilas):
        if i == origen_idx:
            continue

        x = ORIGEN_X + i * ESPACIADO_X
        y = ORIGEN_Y + len(ocultas) * ESPACIADO_Y + (len(visibles) * ESPACIADO_Y if visibles else 0)
        rect_destino_pila = pygame.Rect(x, y, TAM_CARTA[0], TAM_CARTA[1])
        
        if rect_destino_pila.collidepoint(pos):
            if mover_grupo_de_pila_a_pila(pilas, origen_idx, carta_idx_en_pila, i):
                estado_juego["movimientos"] = movimientos + 1
                estado_juego["carta_seleccionada"] = None
                estado_juego["seleccion_visible"] = None
                return True
    return False

def _manejar_movimiento_carta_seleccionada(pos, estado_juego):
    """
    Intenta mover la carta que ya está seleccionada a una fundación o a otra pila.
    Devuelve True si la carta fue movida, False en caso contrario.
    """
    if _intentar_mover_a_fundacion(pos, estado_juego):
        return True

    if _intentar_mover_mazo_a_pila(pos, estado_juego):
        return True

    if _intentar_mover_pila_a_pila(pos, estado_juego):
        return True

    return False


def _manejar_seleccion_carta_pila(pos, estado_juego):
    """
    Maneja el clic para seleccionar una carta de una de las pilas.
    """
    pilas = estado_juego["pilas"]

    for i, (ocultas, visibles) in enumerate(pilas):
        x = ORIGEN_X + i * ESPACIADO_X
        y_inicial_pila = ORIGEN_Y + len(ocultas) * ESPACIADO_Y
        for j, carta in enumerate(visibles):
            rect_carta = pygame.Rect(x, y_inicial_pila + j * ESPACIADO_Y, TAM_CARTA[0], TAM_CARTA[1])
            if rect_carta.collidepoint(pos):
                estado_juego["carta_seleccionada"] = {
                    "origen": "pila",
                    "indice": i,
                    "carta": carta,
                    "grupo": visibles[j:]
                }
                alto_seleccion = TAM_CARTA[1] + ESPACIADO_Y * (len(visibles[j:]) - 1)
                estado_juego["seleccion_visible"] = pygame.Rect(
                    x, y_inicial_pila + j * ESPACIADO_Y, TAM_CARTA[0], alto_seleccion
                )
                return

def _manejar_clic_raton(pos, estado_juego):
    """
    Función principal para manejar los clics del ratón, actualizando el estado del juego.
    Coordina las funciones auxiliares.
    """
    if _manejar_clic_boton_control(pos, estado_juego):
        return

    if _manejar_clic_mazo(pos, estado_juego):
        return

    if estado_juego["carta_seleccionada"]:
        if _manejar_movimiento_carta_seleccionada(pos, estado_juego):
            return
        else:
            # Si había una carta seleccionada pero no se pudo mover a ningún sitio válido
            # se deselecciona al hacer clic en otro lugar no válido
            estado_juego["carta_seleccionada"] = None
            estado_juego["seleccion_visible"] = None
            return

    _manejar_seleccion_carta_pila(pos, estado_juego)

def _manejar_eventos_juego(estado_juego):
    """
    Maneja todos los eventos del juego, actualizando el estado_juego.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado_juego["corriendo"] = False
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            estado_juego["corriendo"] = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            _manejar_clic_raton(evento.pos, estado_juego)

def ejecutar_bucle_juego(pantalla, fuente, reverso, imagenes_cartas,
                         icono_sonido, icono_silencio, boton_sonido_rect,
                         imagen_boton_volver, imagen_boton_siguiente,
                         musica_activada_inicial, icono_actual_inicial): # <-- NUEVOS PARÁMETROS RECIBIDOS
    """
    Contiene el bucle principal del juego.
    """
    estado_juego = _inicializar_estado_juego_completo(
        pantalla, fuente, reverso, imagenes_cartas,
        icono_sonido, icono_silencio, boton_sonido_rect,
        imagen_boton_volver, imagen_boton_siguiente,
        musica_activada_inicial, icono_actual_inicial # <-- PASAR A LA FUNCIÓN DE INICIALIZACIÓN
    )
    
    while estado_juego["corriendo"]:
        # Actualizar la carta visible del mazo en cada ciclo (asegurarse de que sea válida)
        if estado_juego["mazo"] and estado_juego["indice_mazo"] < len(estado_juego["mazo"]):
            estado_juego["carta_visible"] = estado_juego["mazo"][estado_juego["indice_mazo"]]
        else:
            estado_juego["carta_visible"] = None

        dibujar_escena_juego(
            estado_juego["pantalla"], estado_juego["pilas"], estado_juego["carta_visible"], estado_juego["fundaciones"],
            estado_juego["icono_actual"], estado_juego["boton_sonido_rect"], # <-- Usar el icono actual del estado del juego
            estado_juego["imagen_boton_siguiente"], BOTON_SIGUIENTE_RECT,
            estado_juego["imagen_boton_volver"], BOTON_VOLVER_RECT,
            estado_juego["carta_seleccionada"], estado_juego["seleccion_visible"],
            estado_juego["reverso"], estado_juego["imagenes_cartas"]
        )

        # Verificar condición de victoria
        if sum(len(f) for f in estado_juego["fundaciones"]) == 40: # Si hay 40 cartas en las fundaciones, se ganó
            mostrar_mensaje_ganaste_y_guardar_ranking(
                estado_juego["pantalla"], estado_juego["fuente"], estado_juego["movimientos"],
                estado_juego["imagen_boton_volver"], BOTON_VOLVER_RECT
            )
            estado_juego["corriendo"] = False # Termina el juego al ganar
            # No necesitamos 'continue' aquí porque el bucle terminará
        
        _manejar_eventos_juego(estado_juego)
    
    # Devolver el estado final de la música al salir del bucle del juego
    return estado_juego["musica_activada"], estado_juego["icono_actual"]