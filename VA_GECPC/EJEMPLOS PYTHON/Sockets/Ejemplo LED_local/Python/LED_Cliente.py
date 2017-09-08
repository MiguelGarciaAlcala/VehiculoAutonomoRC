import socket

# Se define un objeto de tipo socket(), que sera el cliente. La direccion
# IP debe hacer referencia al servidor local y el puerto debe ser el mismo.
cliente = socket.socket()
HOST = 'localhost'
PUERTO = 9999

# Intentamos conectarnos con el servidor.
try:
    cliente.connect((HOST, PUERTO))
except socket.error:
    print("Error al conectarse con el servidor...")

while True:
    # Se lee el mensaje desde el cliente y se envia al servidor.
    msj = raw_input("> ")
    cliente.send(msj)
    if msj == "q":
        break

print("Cerrando la conexion...")
cliente.close()