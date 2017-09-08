from pygame.locals import *
import pygame, sys

pygame.init()

ventana = pygame.display.set_mode((900, 600))
pygame.display.set_caption("05_Metodos load y blit")

# El metodo load(ruta) sirve para cargar imagenes.
img = pygame.image.load("imagenes/luffy2.png")

# Con el metodo blit(img, (px, py)) se dibuja la imagen 
# img en la posicion (px, py) sobre la ventana.
ventana.blit(img, (50, 50))

while True:

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
