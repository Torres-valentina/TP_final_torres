import pygame
from .constantes import *
from .render_cartas import *
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