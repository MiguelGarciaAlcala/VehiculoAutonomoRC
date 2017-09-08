import numpy as np
import serial
import socket
import cv2


class ServidorControl(object):
    
    def __init__(self, direccion):

        self.imagen_real = None
        self.red_neuronal = cv2.ANN_MLP()
        self.capas = np.int32([320*120, 34, 3])

        self.red_neuronal.create(self.capas)
        self.red_neuronal.load('C:/Users/lluis/Desktop/XXII VICTP 2017/GENERADO/CODIGO/Algoritmo de Entrenamiento/red.xml')

        # Se crea un servidor y se enlaza a la direccion deseada.
        self.crear_servidor(direccion)

        # Declaramos un objeto Serial para comunicarnos con Arduino.
        self.arduino = serial.Serial('COM5', 115200)

    def avanzar(self, imagen):
        c, pred = self.red_neuronal.predict(imagen)

        p = pred.argmax(-1)

        if p == 1:
            self.arduino.write('1')
            return "Izquierda"
        elif p == 0:
            self.arduino.write('7')
            return "Adelante"
        elif p == 2:
            self.arduino.write('6')
            return "Derecha"

    def crear_servidor(self, direccion):
        # Se crea un socket para comunicar la PC con Raspberry Pi.
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(direccion)
        self.servidor.listen(0)

        # Se acepta una conexion unica y se crea un archivo-objeto 
        # asociado a la conexion.
        self.conexion, self.ip = self.servidor.accept()
        self.conexion = self.conexion.makefile('rb')

    def iniciar(self):

        try:
            font = cv2.FONT_HERSHEY_SIMPLEX
            recibido = ''
            while 1:
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

                    self.imagen_real = imagen[120:240, :].reshape(1, 320*120).astype('float32')

                    direc = self.avanzar(self.imagen_real)
                    cv2.putText(imagen, direc, (10, 60), font, 2, (255, 0, 255), 1)

                    # Mostramos las capturas conforme van llegando.
                    cv2.imshow('imagen', imagen)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.arduino.write('0')
                        break

                elif inicio == -1 and final == -1:
                    self.arduino.write('0')
                    break

            cv2.destroyAllWindows()

        finally:
            self.conexion.close()
            self.servidor.close()

if __name__ == '__main__':
    servidor_ctrl = ServidorControl(('192.168.0.100', 8000))
    servidor_ctrl.iniciar()