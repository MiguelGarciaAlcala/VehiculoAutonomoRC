import socket

# Creamos un objeto de tipo socket() que va a ser el cliente.
cliente = socket.socket()
print "[1] Cliente creado exitosamente"

# La direccion debe ser la misma que en el servidor.
direccion = ("localhost", 9999)

try:
    cliente.connect(direccion)
    print "[2] Conectado con ", direccion
except socket.error:
    print "Error al conectarse con el servidor"

# El cliente va a estar activo hasta que el usuario ingrese 
# la letra q, con esto se rompe la conexion.
while True:
    msj = raw_input("> ")
    cliente.send(msj)
    if msj == "q":
        break

print "Finalizando la conexion..."
cliente.close()
print("Conexion cerrada")
