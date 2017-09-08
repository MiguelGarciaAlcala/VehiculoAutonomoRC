import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[1] Servidor creado"

address = ('localhost', 9999)
try:
    server.bind(address)
    print "[2] Servidor enlazado a ", address, "\nEsperando conexion..."
except socket.error:
    print "INFO: Error al enlazar el servidor a la direccion ", address

server.listen(0)

client, ip = server.accept()
print "[3] Conectado con ", ip[0], "\n"

client = client.makefile('r', bufsize=0)

while 1:
    rec = client.readline(10)
    client.flush()
    if rec[len(rec) - 1] == 'q':
        break
    print "Recibido: ", rec, " de ", ip[0]

client.flush()
print "\n[4] Cerrando la conexion"

client.close()
print "[5] Cliente desconectado"

server.close()
print "[6] Servidor desconectado"
