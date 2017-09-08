import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()

ventana = pygame.display.set_mode((900, 600))
pygame.display.set_caption("06_Metodo Random")

# Cargamos una imagen arbitraria.
img = pygame.image.load("imagenes/luffy2.png")

# Con el metodo randint() generamos una posicion 
# aleatoria para mostrar la imagen.
posicion = (randint(0, 900), randint(0, 600))
ventana.blit(img, posicion)

while True:

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
