import pygame
from .constantes import *

# ---------- ÍCONOS DE SONIDO ----------

def cargar_iconos_sonido():
    """
    Carga y escala los íconos de sonido y silencio. 
    También devuelve el rectángulo interactivo para el botón de sonido.

    Returns:
        tuple: (icono_sonido, icono_silencio, boton_sonido_rect)
    """
    icono_sonido = pygame.image.load("sonidos/sonido.png")
    icono_silencio = pygame.image.load("sonidos/silencio.png")
    icono_sonido = pygame.transform.scale(icono_sonido, (40, 40))
    icono_silencio = pygame.transform.scale(icono_silencio, (40, 40))
    boton_sonido_rect = icono_sonido.get_rect(topright=(ANCHO - 10, 10))
    return icono_sonido, icono_silencio, boton_sonido_rect

# ---------- BOTÓN VOLVER ----------

def cargar_boton_volver():
    """
    Carga y escala la imagen del botón 'Volver' y devuelve su superficie y rectángulo.

    Returns:
        tuple: (imagen, rect) del botón 'Volver'
    """
    imagen = pygame.image.load("imagenes/volver.png")
    imagen = pygame.transform.scale(imagen, (80, 80))
    rect = imagen.get_rect(topleft=(10, ALTO - 80))
    return imagen, rect

# ---------- BOTÓN SIGUIENTE ----------

def cargar_boton_siguiente():
    """
    Carga y escala la imagen del botón 'Siguiente'.

    Returns:
        pygame.Surface: Imagen escalada del botón 'Siguiente'
    """
    imagen = pygame.image.load("imagenes/siguiente.png")
    imagen = pygame.transform.scale(imagen, (80, 80))
    return imagen
