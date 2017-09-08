from pygame.locals import *
import numpy as np
import pygame
import serial
import socket
import time
import cv2

class ServidorColector(object):
    
    def __init__(self, direccion):

        # Se inicializan los modulos de Pygame.
        pygame.init()

        # Las variables globales tienen las siguientes funciones:
        #   * direcciones: es una matriz identidad. Cada uno de sus
        #     renglones representa una direccion para el vehiculo.
        #   * etiquetas: es un arreglo que servira para almacenar
        #     patrones de direccion y entrenar a la RNA.
        #   * imagenes: servira para almacenar los frames que se
        #     usaran para entrenar a la RNA.
        #   * imagen_real: es una variable temporal que servira para
        #     guardar las imagenes ya procesadas.
        #   * cont_frames: almacena las capturas que se han guardado.
        #   * fin: controla la duracion de captura.
        self.direcciones = np.identity(3, 'float')
        self.etiquetas = np.zeros((1, 3), 'float')
        self.imagenes = np.zeros((1, 320*120))
        self.imagen_real = None
        self.cont_frames = 0
        self.fin = False

        # Se crea un servidor y se enlaza a la direccion deseada.
        self.crear_servidor(direccion)

        # Declaramos un objeto Serial para comunicarnos con Arduino.
        self.arduino= serial.Serial('COM5', 115200)

        # Interfaz grafica de Pygame para trabajar con el teclado.
        self.ventana = pygame.display.set_mode((320, 240))
        pygame.display.set_caption("Algoritmo de recoleccion de imagenes")

    def crear_servidor(self, direccion):
        # Se crea un socket para comunicar la PC con Raspberry Pi.
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(direccion)
        self.servidor.listen(0)

        # Se acepta una conexion unica y se crea un archivo-objeto 
        # asociado a la conexion.
        self.conexion, self.ip = self.servidor.accept()
        self.conexion = self.conexion.makefile('rb')

    def guardar_patron(self, i):
        # Se apila el contenido de la variable imagen_real en la matriz
        # de imagenes y el patron i en la matriz de etiquetas. Por ultimo
        # se incrementa el contador de frames guardados.
        self.imagenes = np.vstack((self.imagenes, self.imagen_real))
        self.etiquetas = np.vstack((self.etiquetas, self.direcciones[i]))
        self.cont_frames += 1

    def iniciar(self):

        try:
            recibido = ''
            while not self.fin:
                # Leemos la informacion que ha escrito el cliente y buscamos
                # los delimitadores de la imagen JPG.
                # NOTA: cualquier imagen en formato JPG inicia con \xff\xd8 y
                # termina con \xff\xd9.
                recibido += self.conexion.read(1024)
                inicio = recibido.find('\xff\xd8')
                final = recibido.find('\xff\xd9')

                # Mientras el cliente este activo y envie capturas, se debe cumplir
                # la condicion inicio != -1 and final != -1, ya que si inicio = final = -1
                # significa que el cliente ha dejado de enviar informacion.
                if inicio != -1 and final != -1:

                    # Se extrae la imagen en formato JPG de la variable recibido y se 
                    # actualiza su contenido. 
                    jpg = recibido[inicio:final + 2]
                    recibido = recibido[final + 2:]

                    # Se decodifica la imagen recibida y se extrae la mitad que se 
                    # va a utilizar para entrenar a la RNA.
                    imagen = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    self.imagen_real = imagen[120:240, :].reshape(1, 320*120).astype(np.float32)

                    # Mostramos las capturas conforme van llegando.
                    cv2.imshow('imagen', imagen)

                    for evento in pygame.event.get():
                        if evento.type == KEYDOWN:

                            # Si se presiona una tecla se guarda la captura y la tecla presionada.
                            cv2.imwrite('img_entrenamiento/img{}.jpg'.format(self.cont_frames + 1), imagen)
                            tecla = pygame.key.get_pressed()

                            # Se compara la tecla presionada para comunicarnos con Arduino y 
                            # controlar al vehiculo. Los patrones se eligieron de la forma siguiente:
                            # 1 0 0 -> Izquierda
                            # 0 1 0 -> Adelante
                            # 0 0 1 -> Derecha
                            if tecla[pygame.K_UP] and tecla[pygame.K_RIGHT]:
                                self.guardar_patron(2)
                                self.arduino.write('6')
                                
                            elif tecla[pygame.K_UP] and tecla[pygame.K_LEFT]:
                                self.guardar_patron(0)
                                self.arduino.write('7')

                            elif tecla[pygame.K_UP]:
                                self.guardar_patron(1)
                                self.arduino.write('1')

                            elif tecla[pygame.K_DOWN]:
                                self.arduino.write('2')
                            
                            elif tecla[pygame.K_RIGHT]:
                                self.guardar_patron(2)
                                self.arduino.write('3')

                            elif tecla[pygame.K_LEFT]:
                                self.guardar_patron(0)
                                self.arduino.write('4')

                            elif tecla[pygame.K_q]:
                                self.arduino.write('0')
                                self.arduino.close()
                                self.fin = True
                                break
                        
                        # Si se libera una tecla, le mandamos el caracter '0' a Arduino
                        # para que el vehiculo se detenga.            
                        elif evento.type == pygame.KEYUP:
                            self.arduino.write('0')

                elif alfa == -1 and omega == -1:
                    self.arduino.write('0')
                    self.arduino.close()
                    break

            # Extraemos las imagenes y las etiquetas guardadas.
            self.imagenes = self.imagenes[1:, :]
            self.etiquetas = self.etiquetas[1:, :]

            # El nombre del archivo npz va a depender del tiempo del sistema y
            # se guardara en la ruta datos_entrenamiento/archivo.npz
            archivo = str(int(time.time()))
            ruta = "datos_entrenamiento/" + archivo + ".npz"
            guardar = raw_input('Guardar[s/n]: ')

            try:
                if guardar == 's':
                    # Intentamos guardar los arreglos de imagenes y etiquetas.
                    np.savez(ruta, imagenes=self.imagenes, etiquetas=self.etiquetas)
                    print "Datos de entrenamiento guardados en: \n" + ruta + "\n"
                    print "Total patrones: ", str(self.cont_frames)
            except IOError:
                print "Error al guardar los datos"

        finally:
            self.conexion.close()
            self.servidor.close()

if __name__ == '__main__':
    colector = ServidorColector(('192.168.0.100', 8000))
    colector.iniciar()