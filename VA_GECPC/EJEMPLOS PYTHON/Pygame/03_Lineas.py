import pygame, sys, random
from pygame.locals import *

# Se inicializan los modulos de Pygame.
pygame.init()

# Creamos una ventana y definimos dos colores.
ventana = pygame.display.set_mode((500, 500))
pygame.display.set_caption("03_Dibujando lineas")

color1 = pygame.Color(255, 0, 0)
color2 = pygame.Color(0, 0, 255)

# Dibujamos dos lineas con el metodo 
# pygame.draw.line(ventana, color, (x1, y1), (x2, y2), ancho)
pygame.draw.line(ventana, color1, (0, 0), (500, 500), 5)
pygame.draw.line(ventana, color2, (0, 500), (500, 0), 10)

# Veamos como esta compuestos los colores de cada linea:
print "Los colores de las lineas en formato RGB son:"
print "Linea1\nR: ", color1.r, "\nG: ", color1.g, "\nB: ", color1.b
print "\nLinea2\nR: ", color2.r, "\nG: ", color2.g, "\nB: ", color2.b

while True:

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
