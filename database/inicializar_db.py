#Integrantes de servidor:Polett Casanga Rojas,Juan Castillo Lizama,Guilliano Punulaf,Kassandra Ramos
#Fecha de creación:03/10/2025
#Fecha de modificación:14/10/2025
# Descripcion: Inicializa MySQL usando PyMySQL: crea/verifica la base de datos y la tabla ({NOMBRE_TABLA}); 
# maneja errores y cierra conexiones.

import pymysql
from pymysql.constants import ER
from config import MYSQL_CONFIG, NOMBRE_TABLA


def crear_base_de_datos():
    """
    Se conecta a MySQL, crea la base de datos si no existe
    y luego crea la tabla si no existe.
    """
    conexion = None
    db_name = MYSQL_CONFIG['database']
    
    # Preparamos una config para conectar *sin* la base de datos
    server_config = MYSQL_CONFIG.copy()
    del server_config['database']

    try:
        # 1. Conectar al servidor MySQL (sin la base de datos)
        conexion = pymysql.connect(**server_config)
        
        with conexion.cursor() as cursor:
            # 2. Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8")
            print(f"Base de datos '{db_name}' verificada/creada.")
            
            # 3. Seleccionar la base de datos para operar en ella
            conexion.select_db(db_name)
            
            # 4. Crear tabla con las columnas necesarias si no existe
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {NOMBRE_TABLA} (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    pais TEXT NOT NULL,
                    codigo VARCHAR(10),
                    año INTEGER NOT NULL,
                    perdida_hectareas DOUBLE NOT NULL
                )
            ''')
        
        conexion.commit()
        print(f"Tabla '{NOMBRE_TABLA}' verificada/creada.")
    
    except pymysql.err.OperationalError as e:
        # Manejar errores comunes de PyMySQL
        if e.args[0] == ER.ACCESS_DENIED_ERROR:
            print("Error: Credenciales de MySQL incorrectas (usuario/contraseña).")
        else:
            print(f"Error operacional de MySQL: {e}")
    except pymysql.Error as e:
        print(f"Error al conectar o crear la base de datos PyMySQL: {e}")
    finally:
        # Asegurar cierre de la conexión
        if conexion:
            conexion.close()


if __name__ == '__main__':
    # Ejecutar creación si se llama directamente
    crear_base_de_datos()


if __name__ == '__main__':
    # Ejecutar creación si se llama directamente
    crear_base_de_datos()