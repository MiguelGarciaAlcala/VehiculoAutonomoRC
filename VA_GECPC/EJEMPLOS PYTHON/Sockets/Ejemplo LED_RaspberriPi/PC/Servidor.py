import socket
import serial

# Se crea un objeto de tipo socket() y se enlaza al 
# servidor usando el puerto 8000.
servidor = socket.socket()
HOST = '192.168.0.13'
PUERTO = 8000

try:
    servidor.bind((HOST, PUERTO))
except socket.error:
    print('Error en la conexion...')

# El servidor puede aceptar un cliente como maximo.
servidor.listen(0)

# El metodo accept() valida la conexion con el servidor y retorna 
# una tupla que contiene un objeto socket() y su direccion IP.
cliente, ip = servidor.accept()

# Creamos un objeto Serial() para comunicarnos con Arduino.
arduino = serial.Serial('COM5', 115200)

while True:
    # El ciclo infinito permite que el servidor este ectivo hasta que se cumpla una condicion de
    # salida. Mientras tanto, el cliente pueden mandar informacion que se guarda en la variable rec.
    # Por ultimo, el parametro 1024 es el limite de informacion que puede recibir el servidor.
    rec = cliente.recv(1024)

    # Los datos recibidos se evaluan. Si se recibe un caracter 'q', la conexion se cierra. De lo
    # contrario, los datos se envian a Arduino.
    if rec == "q":
        # Se envian los caracteres 'a' y 'b' al Arduino para apagar ambos LEDs.
        arduino.write('ab')
        break
    else:
        # Se envia el caracter recibido a Arduino y continua el ciclo.
        arduino.write(rec)

    # Se notifica que los datos enviados por el cliente se han recibido.
    print "Recibido: " + rec + " de " + ip[0]
    cliente.send(rec)

print "Cerrando la conexion..."
cliente.close()
servidor.close()
