from pygame.locals import *
import pygame, sys

pygame.init()

ventana = pygame.display.set_mode((500, 500))
pygame.display.set_caption("04_Dibujando poligonos")

# Se crea un circulo con el metodo
# circle(ventana, color, centro, radio)
pygame.draw.circle(ventana, (0, 0, 255), (100, 100), 40)

# Se crea un rectangulo con el metodo
# rect(ventana, color, (vx, vy, largo, ancho))
pygame.draw.rect(ventana, (0, 255, 0), (200, 50, 250, 100))

# Se crea un poligono (triangulo) con el metodo
# polygon(ventana, color, ((x0, y0), (x1, y1), ... , (xn, yn)))

vertices = ((100, 200), (150, 250), (50, 250))
pygame.draw.polygon(ventana, (255, 0, 0), vertices)

while True:

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
