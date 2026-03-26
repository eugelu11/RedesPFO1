import socket
import threading
import sqlite3
from datetime import datetime

HEADER = 64
PORT = 5000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
MENSAJE_DESCONEXION = "exito"

def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contenido TEXT,
        fecha_envio TEXT,
        ip_cliente TEXT
    )
    """)
    conn.commit()
    conn.close()

def manejar_cliente(conn_socket, addr):
    db = sqlite3.connect("chat.db")
    cursor = db.cursor()

    while True:
        try:
            len_mensaje = conn_socket.recv(HEADER).decode(FORMAT)
            if not len_mensaje:
                break

            len_mensaje = int(len_mensaje.strip())
            mensaje = conn_socket.recv(len_mensaje).decode(FORMAT)

            if mensaje == MENSAJE_DESCONEXION:
                break

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO messages (contenido, fecha_envio, ip_cliente)
                VALUES (?, ?, ?)
            """, (mensaje, timestamp, addr[0]))

            db.commit()

            respuesta = f"Mensaje recibido: {timestamp}"
            respuesta_bytes = respuesta.encode(FORMAT)

            len_respuesta = str(len(respuesta_bytes)).encode(FORMAT)
            len_respuesta += b' ' * (HEADER - len(len_respuesta))

            conn_socket.sendall(len_respuesta)
            conn_socket.sendall(respuesta_bytes)

        except:
            break

    db.close()
    conn_socket.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
    except:
        return

    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

init_db()
iniciar_servidor()