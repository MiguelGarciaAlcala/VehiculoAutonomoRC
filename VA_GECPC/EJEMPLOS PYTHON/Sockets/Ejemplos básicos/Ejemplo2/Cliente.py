import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[1] Cliente creado exitosamente"

direccion = ("localhost", 9999)
cliente.connect(direccion)
print "[2] Conectado con ", direccion

archivo_cliente = cliente.makefile('w', bufsize=0)

while not False:
    msj = raw_input("> ")
    archivo_cliente.write(msj)
    archivo_cliente.flush()
    if msj == 'q':
        break

print "Finalizando la conexion..."
cliente.close()
print "Conexion cerrada"
archivo_cliente.close()