from pygame.locals import *
import pygame, sys

pygame.init()

ventana = pygame.display.set_mode((900, 500))
pygame.display.set_caption("07_AnimacionesBasicas")

# Cargamos una imagen y definimos su posicion inicial.
img = pygame.image.load("imagenes/freezer.png")
px = 5
py = 50

# Las variables velocidad y derecha sirven para controlar
# la posicion de la imagen img.
velocidad = 1
derecha = True

while True:
    # La ventana sera de color blanco y la imagen se dibuja
    # en cada iteracion para actualizar su posicion.
    ventana.fill((255, 255, 255))
    ventana.blit(img, (px, py))

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # Si la imagen toca alguno de los bordes de la ventana,
    # cambia su direccion y avanza en sentido opuesto.
    if derecha:
        if px < 700:
            px += velocidad
        else:
            derecha = False
    else:
        if px > 5:
            px -= velocidad
        else:
            derecha = True

    pygame.display.update()
