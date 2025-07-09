
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
# Aunque las constantes no suelen tener lógica, estos rectángulos son fijos
# y útiles para la detección de clics en el bucle principal.
# Es una forma de "pre-calcular" estos elementos fijos sin usar clases.
import pygame # Se importa pygame solo para usar pygame.Rect
MAZO_RECT = pygame.Rect(50, 20, TAM_CARTA[0], TAM_CARTA[1])

# Rectángulos de las fundaciones
# Se calculan asumiendo 4 fundaciones, una por palo
FUNDACION_RECTS = []
for i in range(4):
    x = FUNDACION_X + i * (TAM_CARTA[0] + 20)
    y = FUNDACION_Y
    FUNDACION_RECTS.append(pygame.Rect(x, y, TAM_CARTA[0], TAM_CARTA[1]))

# Rectángulos para los botones de Siguiente y Volver (sus posiciones también son fijas)
# Estas constantes las definía la lógica de assets_loader, pero para que 'constantes'
# sea el único lugar con 'valores fijos', los pongo aquí y assets_loader
# sólo se encargaría de cargar la imagen.
# Sin embargo, el problema original ya los tenía en constantes.py o se pasaban como parámetros.
# En la refactorización anterior, me basé en el uso que se hacía en logica_juego.py.
# Dado que se usan en gestor_juego.py, los definiré aquí si no estaban ya.

# Los BOTON_SIGUIENTE_RECT y BOTON_VOLVER_RECT ya son constantes en gestor_juego.py.
# Si el usuario quiere que estén aquí para ser un "centro de constantes",
# debería ajustar las coordenadas, pero actualmente ya están bien en gestor_juego.py.
# Para evitar duplicidad o confusión, mantendré la última versión donde
# las imágenes y sus rects se manejan en assets_loader y se pasan al gestor.
# Pero sí es buena idea que los rectángulos del MAZO y FUNDACIONES estén aquí.

# Re-evaluando las constantes y su uso en `gestor_juego.py`:
# `BOTON_SIGUIENTE_RECT` y `BOTON_VOLVER_RECT` son importados directamente
# en `gestor_juego.py` desde `constantes.py`.
# En `assets_loader.py`, `cargar_boton_volver` devuelve la imagen Y EL RECT.
# Esto genera una pequeña inconsistencia.

# Para una mayor coherencia, los rectángulos de los botones (Volver, Siguiente)
# deberían definirse como constantes aquí si su posición es fija y no depende
# del tamaño de la imagen que podría variar.

# Basándome en la implementación de `assets_loader.py`:
# `boton_sonido_rect` se crea con `topright=(ANCHO - 10, 10)`
# `BOTON_VOLVER_RECT` se crea con `topleft=(10, ALTO - 80)`
# `BOTON_SIGUIENTE_RECT` no se crea un rect en `assets_loader.py`, solo la imagen.
# En `logica_juego.py` (ahora `gestor_juego.py`), `BOTON_SIGUIENTE_RECT` se importa directamente.
# Esto significa que `BOTON_SIGUIENTE_RECT` *necesita* ser una constante aquí.

# Ajusto el archivo `constantes.py` para incluir estos rectángulos fijos:

BOTON_SIGUIENTE_RECT = pygame.Rect(150, 40, 80, 80) # Posición arbitraria basada en el render
BOTON_VOLVER_RECT = pygame.Rect(10, ALTO - 80, 80, 80) # De cargar_boton_volver