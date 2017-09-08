from pygame.locals import *
import pygame, sys

# Sentencia obligatoria. 
# Inicializa todos los modulos de pygame.
pygame.init()

# Creamos una ventana con el metodo pygame.display.set_mode((WIDTH, HEIGHT)).
# Este retorna un objeto de tipo Surface.
ventana = pygame.display.set_mode((400, 300))

# La ventana tendra el titulo que esta entre comillas.
pygame.display.set_caption("01_Hola, mundo!")

# La ventana permanece activa hasta que el usuario decida salir.
while True:

    for evento in pygame.event.get():
        # Si presionamos el boton "Salir", se cierran los modulos
        # de pygame y cerramos la ventana.
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # El metodo pygame.display.update() actualiza el contenido
    # de la ventana generada.
    pygame.display.update()
