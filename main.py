from api.servidor import Servidor
from gui.interfaz_usuario import InterfazGrafica
from database.inicializar_db import crear_base_de_datos

if __name__ == '__main__':
    # Instanciar la interfaz gráfica sin servidor aún
    app = InterfazGrafica(servidor=None)

    # Inicializar la base de datos y crear tablas si no existen
    crear_base_de_datos()
    
    # Definir callback para loguear mensajes (conexiones, errores, info)
    # Usar la función print para mostrar en consola
    callback_log = print

    # Definir callback para procesar datos recibidos desde el servidor
    # Utilizar 'after' para asegurarse de ejecutar en el hilo de la GUI
    callback_datos = lambda datos: app.after(0, app.manejar_datos_recibidos, datos)

    # Instanciar el servidor con los callbacks definidos
    servidor = Servidor(callback_log, callback_datos)
    # Asociar el servidor a la interfaz para controlar inicio/detención
    app.servidor = servidor

    # Mostrar instrucción inicial al usuario en consola
    print("Bienvenido. Ingrese Host/Puerto y presione 'Iniciar Servidor' en la ventana.")

    # Iniciar el loop principal de la interfaz gráfica
    app.mainloop()