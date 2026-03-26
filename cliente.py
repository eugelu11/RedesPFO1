import socket

HEADER = 64
PORT = 5000
SERVER = "127.0.0.1"
FORMAT = 'utf-8'
MENSAJE_DESCONEXION = "exito"

ADDR = (SERVER, PORT)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(ADDR)

def mandar(mensaje):
    mensaje_bytes = mensaje.encode(FORMAT)
    len_mensaje = len(mensaje_bytes)

    mandar_len = str(len_mensaje).encode(FORMAT)
    mandar_len += b' ' * (HEADER - len(mandar_len))

    cliente.sendall(mandar_len)
    cliente.sendall(mensaje_bytes)

    if mensaje == MENSAJE_DESCONEXION:
        return

    len_respuesta = cliente.recv(HEADER).decode(FORMAT)
    if not len_respuesta:
        return

    len_respuesta = int(len_respuesta.strip())
    respuesta = cliente.recv(len_respuesta).decode(FORMAT)

    print(respuesta)

while True:
    mensaje = input(">> ")
    mandar(mensaje)

    if mensaje == MENSAJE_DESCONEXION:
        break

cliente.close()
