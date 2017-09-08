from pygame.locals import *
import pygame, sys

# Inicializamos los modulos de pygame.
pygame.init()

color1 = (0, 140, 160)
color2 = pygame.Color(255, 120, 9)

# Creamos una ventana de 400x300 pixeles.
ventana = pygame.display.set_mode((400, 300))

# La ventana tendra el titulo entre comillas.
pygame.display.set_caption("02_Creacion de colores en Pygame")

# La ventana permanece activa hasta que el usuario decida salir.
while True:
    ventana.fill(color2)

    for evento in pygame.event.get():
        # Si presionamos el boton "Salir", se cierran los modulos
        # de pygame y cerramos la ventana.
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # Actualizamos el contenido de la ventana.
    pygame.display.update()
