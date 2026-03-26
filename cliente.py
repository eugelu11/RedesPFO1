import socket


HEADER = 64
PORT = 5050
SERVER =socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
MENSAJE_DESCONEXION = "!DESCONECTAR"
ADDR=(SERVER,PORT)

cliente=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(ADDR)

def mandar(mensaje):
    mensaje=mensaje.encode(FORMAT)
    len_mensaje=len(mensaje)
    mandar_len=str(len_mensaje).encode(FORMAT)
    mandar_len += b' ' * (HEADER - len(mandar_len))
    cliente.send(mandar_len)
    cliente.send(mensaje)
