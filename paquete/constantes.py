
# --- Archivos ---
ARCHIVO_RANKING = "archivos/ranking.txt"

# --- Propiedades del Juego ---
VALORES = list(range(1, 11))
PALOS = ['oros', 'copas', 'espadas', 'bastos']

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (50, 100, 200)
VERDE = (0, 128, 0)
GRIS = (100, 100, 100)
ROJO = (255, 0, 0)
# --- Dimensiones de Pantalla ---
ANCHO = 800
ALTO = 600

# --- Posicionamiento de Cartas y Elementos del Tablero ---
TAM_CARTA = (80, 120)
ESPACIADO_X = 100
ESPACIADO_Y = 30
#----------------COORDENADAS PILAS ---------------------------
ORIGEN_X = 100
ORIGEN_Y = 170

#----------------COORDENADAS FUNDACIONES-------------------------------
FUNDACION_X = 250
FUNDACION_Y = 20

# --- Rectángulos de áreas interactivas fijas (pueden ser calculados una vez) ---

import pygame # Se importa pygame solo para usar pygame.Rect
MAZO_RECT = pygame.Rect(50, 20, TAM_CARTA[0], TAM_CARTA[1])

# Rectángulos de las fundaciones
FUNDACION_RECTS = []
for i in range(4):
    x = FUNDACION_X + i * (TAM_CARTA[0] + 20)
    y = FUNDACION_Y
    FUNDACION_RECTS.append(pygame.Rect(x, y, TAM_CARTA[0], TAM_CARTA[1]))

# Rectángulos para los botones de Siguiente y Volver (sus posiciones también son fijas)

BOTON_SIGUIENTE_RECT = pygame.Rect(150, 40, 80, 80) # Posición arbitraria basada en el render
BOTON_VOLVER_RECT = pygame.Rect(10, 500, 80, 80) # De cargar_boton_volver