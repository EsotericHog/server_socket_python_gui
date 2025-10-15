#Integrantes de servidor:Poleth Casanga Rojas,Juan Castillo Lizama,Guilliano Punulaf,Kassandra Ramos
#Fecha de creación:03/10/2025
#Fecha de modificación:14/10/2025
#Descripcion: Servidor TCP multihilo que escucha en un host/puerto, acepta clientes y por conexión recibe 
# un flujo de bytes hasta EOF, lo decodifica como JSON, registra eventos (callback_log), entrega los datos 
# a la app (callback_datos) y envía un acuse de recibo. Incluye métodos para iniciar y detener limpiamente 
# (SO_REUSEADDR + desbloqueo de accept()).

import socket
import threading
import json
from config import TAMANO_BUFFER


def manejar_cliente(conexion_cliente, direccion, callback_log, callback_datos):
    """
    Maneja la conexión de un cliente:
    - Recibe bytes hasta que la conexión se cierre.
    - Decodifica los bytes a JSON y llama al callback de datos.
    - Envía confirmación al cliente y cierra la conexión.
    """
    # Notificar nueva conexión
    callback_log(f"Log: [NUEVA CONEXIÓN] {direccion} conectado.")

    # Acumular los datos recibidos en bytes
    datos_completos = b""
    while True:
        datos = conexion_cliente.recv(TAMANO_BUFFER)
        # Romper si no llegan más datos (cliente cerró envío)
        if not datos:
            break
        datos_completos += datos

    try:
        # Decodificar y cargar JSON desde los bytes recibidos
        datos_json = json.loads(datos_completos.decode('utf-8'))
        callback_log(f"Log: -> Datos recibidos de {direccion}: {len(datos_completos)} bytes.")

        # Llamar al callback para procesar los datos (por ejemplo, actualizar GUI)
        callback_datos(datos_json)

        # Enviar acuse de recibo al cliente
        conexion_cliente.sendall(b"Datos recibidos por el servidor. Listos para ser guardados.")
    except json.JSONDecodeError as e:
        # Loguear error si el payload no es un JSON válido
        callback_log(f"Log: [ERROR] Datos de {direccion} no son un JSON válido. Error: {e}")
    except Exception as e:
        # Loguear cualquier excepción inesperada
        callback_log(f"Log: [ERROR] Inesperado en manejar_cliente: {e}")
    finally:
        # Asegurar cierre de la conexión y notificar
        conexion_cliente.close()
        callback_log(f"Log: [CONEXIÓN CERRADA] {direccion}")


class Servidor:
    """
    Clase para manejar el socket servidor en un hilo separado.
    - Iniciar: crear hilo y comenzar a escuchar conexiones.
    - Detener: marcar como no corriendo, cerrar socket y despertar accept.
    """

    def __init__(self, callback_log, callback_datos):
        # Guardar callbacks para logging y procesamiento de datos
        self.callback_log = callback_log
        self.callback_datos = callback_datos
        # Inicializar estado del servidor
        self.socket_servidor = None
        self.corriendo = False
        self.hilo_servidor = None
        self.host = ""
        self.puerto = 0

    def iniciar(self, host, puerto):
        # Iniciar servidor solo si no está corriendo
        if not self.corriendo:
            self.host = host
            self.puerto = puerto
            self.corriendo = True
            # Crear y arrancar hilo que escucha conexiones
            self.hilo_servidor = threading.Thread(target=self._escuchar_conexiones)
            self.hilo_servidor.start()
            self.callback_log(f"Log: [INICIANDO] Servidor escuchando en {self.host}:{self.puerto}")

    def detener(self):
        # Detener servidor si está corriendo
        if self.corriendo:
            self.corriendo = False
            try:
                # Intentar conectar para desbloquear accept() si está esperando
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.puerto))
            except:
                pass
            # Cerrar socket servidor si existe
            if self.socket_servidor:
                self.socket_servidor.close()
            self.callback_log("Log: [DETENIDO] El servidor ha sido detenido.")

    def _escuchar_conexiones(self):
        # Crear socket, configurar opciones y enlazar dirección
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_servidor.bind((self.host, self.puerto))
        self.socket_servidor.listen()

        # Bucle principal para aceptar conexiones mientras esté corriendo
        while self.corriendo:
            try:
                conexion_cliente, direccion = self.socket_servidor.accept()
                # Si aún se debe procesar la conexión, crear hilo para el cliente
                if self.corriendo:
                    hilo_cliente = threading.Thread(
                        target=manejar_cliente,
                        args=(conexion_cliente, direccion, self.callback_log, self.callback_datos)
                    )
                    hilo_cliente.start()
            except OSError:
                # Salir si socket fue cerrado desde fuera
                break