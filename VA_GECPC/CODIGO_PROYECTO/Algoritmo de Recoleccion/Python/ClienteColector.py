import picamera
import socket
import struct
import time
import io


class ClienteColector(object):
    # Se define el constructor de la clase ClienteColector, que recibe
    # los siguientes parametros:
    # 	* resolucion: es una tupla que contiene la resolucion de la
    #     camara en pixeles.
    # 	* tiempo_captura: tiempo (segundos) que va a durar el streaming.
    # 	* direccion_servidor: es una tupla que contiene la direccion IP
    #     del servidor al cual se va a enlazar el cliente y el puerto
    #     que se va a usar en formato (IP_SERVIDOR, PUERTO).
    #   * framerate: velocidad (frames por segundo) de la camara.
    def __init__(self, resolucion, tiempo_captura, direccion_servidor, framerate):

        # Se definen las variables globales resolucion, tiempo_captura y framerate.
        self.framerate = framerate
        self.resolucion = resolucion
        self.tiempo_captura = tiempo_captura

        # Conectamos el cliente.
        self.conectar_cliente(direccion_servidor)

    def conectar_cliente(self, direccion):

        # Creamos un cliente y lo enlazamos a la direccion deseada.
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(direccion)

        # Creamos un archivo asociado a la conexion.
        self.conexion = cliente.makefile('wb')

    def iniciar_streaming(self):

        try:
            with picamera.PiCamera() as camara:
                # Ajustamos la resolucion de la camara.
                camara.resolution = self.resolucion

                # La velocidad por defecto sera de 10fps (frames por segundo)
                camara.framerate = self.framerate

                # Hacemos una pausa de 2 segundos para que la camara
                # se prepare y guardamos el tiempo de inicio.
                time.sleep(2)
                tiempo_inicial = time.time()

                # Se reserva un stream para almacenar las imagenes de
                # manera temporal y poder acceder a sus propiedades.
                stream = io.BytesIO()

                # Para capturar imagenes de manera continua usamos un ciclo
                # infinito que se ejecuta con el metodo capture_continous().

                # Las capturas se almacenan en la variable stream en formato JPEG y
                # habilitamos el puerto de video porque es mas veloz que el de la camara.
                for img in camara.capture_continuous(stream, 'jpeg', use_video_port=True):

                    # Escribimos el tamano de la captura en formato Little Endian y ejecutamos
                    # el metodo flush() para asegurarnos de que la captura ha sido enviada.
                    self.conexion.write(struct.pack('<L', stream.tell()))
                    self.conexion.flush()

                    # Nos movemos al inicio del objeto stream y enviamos la captura a
                    # traves de la conexion.
                    stream.seek(0)
                    self.conexion.write(stream.read())

                    # Si el tiempo de captura se ha excedido, se detiene el streaming.
                    if time.time() - tiempo_inicial > self.tiempo_captura:
                        break

                    # Regresamos al inicio del stream, ya que al llamar el metodo
                    # read() se mueve el apuntador hasta la ultima posicion; y
                    # finalmente, limpiamos la variable para escribir la siguiente
                    # captura generada por la camara.
                    stream.seek(0)
                    stream.truncate()

            # Cuando el tiempo de captura se ha alcanzado, le enviamos un 0 al servidor
            # para indicarle que terminaron las capturas.
            self.conexion.write(struct.pack('<L', 0))
        finally:
            self.conexion.close()
            self.cliente.close()


if __name__ == '__main__':
    colector = ClienteColector((320, 240), 600, ('192.168.0.100', 8000), 10)
    colector.iniciar_streaming()
