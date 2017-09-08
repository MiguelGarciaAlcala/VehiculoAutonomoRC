import pygame, sys, serial
from pygame.locals import *


class ControlTeclado(object):

    def __init__(self, titulo, tamanio):
        pygame.init()

        self.fuente = pygame.font.SysFont("Arial Black", 30)
        self.titulo = self.fuente.render(titulo, 0, (0, 10, 20))
        self.ventana = pygame.display.set_mode(tamanio)

        self.arduino = serial.Serial('COM5', 115200)
        self.flechas = []

    def cargar_imagenes(self):
        for img in range(1, 9):
            self.flechas.append(pygame.image.load("flechas/flecha_0" + str(img) + ".png"))

    def dibujar_flechas(self):
        self.ventana.blit(self.flechas[3], (210, 100))
        self.ventana.blit(self.flechas[5], (90, 220))
        self.ventana.blit(self.flechas[7], (290, 220))
        self.ventana.blit(self.flechas[1], (210, 300))

    def direccion(self, tecla):

        if tecla[pygame.K_UP] and tecla[pygame.K_RIGHT]:
            self.ventana.blit(self.flechas[2], (210, 100))
            self.ventana.blit(self.flechas[6], (290, 220))
            self.arduino.write('6')
            print "VUELTA A LA DERECHA"

        elif tecla[pygame.K_UP] and tecla[pygame.K_LEFT]:
            self.ventana.blit(self.flechas[2], (210, 100))
            self.ventana.blit(self.flechas[4], (90, 220))
            self.arduino.write('7')
            print "VUELTA A LA IZQUIERDA"

        elif tecla[pygame.K_DOWN] and tecla[pygame.K_RIGHT]:
            self.ventana.blit(self.flechas[0], (210, 300))
            self.ventana.blit(self.flechas[6], (290, 220))
            self.arduino.write('8')
            print "REVERSA DERECHA"

        elif tecla[pygame.K_DOWN] and tecla[pygame.K_LEFT]:
            self.ventana.blit(self.flechas[0], (210, 300))
            self.ventana.blit(self.flechas[4], (90, 220))
            self.arduino.write('9')
            print "REVERSA IZQUIERDA"

        elif tecla[pygame.K_UP]:
            self.ventana.blit(self.flechas[2], (210, 100))
            self.arduino.write('1')
            print "ADELANTE"

        elif tecla[pygame.K_DOWN]:
            self.ventana.blit(self.flechas[0], (210, 300))
            self.arduino.write('2')
            print "REVERSA"

        elif tecla[pygame.K_RIGHT]:
            self.ventana.blit(self.flechas[6], (290, 220))
            self.arduino.write('3')
            print "DERECHA"

        elif tecla[pygame.K_LEFT]:
            self.ventana.blit(self.flechas[4], (90, 220))
            self.arduino.write('4')
            print "IZQUIERDA"

    def inicio(self):
        pygame.display.set_caption("RADIO CONTROL")
        self.ventana.fill((255, 255, 255))

        self.cargar_imagenes()
        self.dibujar_flechas()

        self.ventana.blit(self.titulo, (50, 40))

        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    print "Saliendo..."
                    self.arduino.write('0')
                    self.arduino.close()
                    pygame.quit()
                    sys.exit()
                elif evento.type == KEYDOWN:
                    tecla = pygame.key.get_pressed()
                    self.direccion(tecla)
                elif evento.type == KEYUP:
                    self.dibujar_flechas()
                    self.arduino.write('0')

            pygame.display.update()

if __name__ == '__main__':
    gui_control = ControlTeclado("CONTROL POR TECLADO", (500, 500))
    gui_control.inicio()