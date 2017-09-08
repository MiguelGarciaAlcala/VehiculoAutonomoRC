import socket

# Se crea un nuevo socket.
servidor = socket.socket()
print "[1] Servidor creado"

# Se especifica el puerto en el que se va a mantener la escucha del servidor.
direccion = ('localhost', 9999)
try:
    servidor.bind(direccion)
    print "[2] Servidor enlazado a ", direccion, "\nEsperando conexion..."
except socket.error:
    print "INFO: Error al enlazar el servidor a la direccion ", direccion

# El servidor aceptara un cliente como maximo.
servidor.listen(0)

cliente, ip = servidor.accept()
print "[3] Conectado con ", ip[0], "\n"

while True:
    rec = cliente.recv(1024)
    if rec == 'q':
        break
    print "Recibido: ", rec, " de ", ip[0]

print "\n[4] Cerrando la conexion"

cliente.close()
print "[5] Cliente desconectado"

servidor.close()
print "[6] Servidor desconectado"
