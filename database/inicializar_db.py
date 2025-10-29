#Integrantes de servidor:Polett Casanga Rojas,Juan Castillo Lizama,Guilliano Punulaf,Kassandra Ramos
#Fecha de creación:03/10/2025
#Fecha de modificación:14/10/2025
#Descripcion: Inicializa SQLite: crea/verifica la base y la tabla ({NOMBRE_TABLA}); maneja errores 
# y cierra conexión; ejecutable directo.

import sqlite3
import os
from config import NOMBRE_DB, NOMBRE_TABLA


def crear_base_de_datos():
    """
    Crear el archivo de la base de datos y la tabla si no existen.
    """
    directorio_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(directorio_proyecto, NOMBRE_DB)

    try:
        # Abrir conexión y obtener cursor
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        # Crear tabla con las columnas necesarias si no existe
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {NOMBRE_TABLA} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pais TEXT NOT NULL,
                codigo TEXT,
                año INTEGER NOT NULL,
                perdida_hectareas REAL NOT NULL
            )
        ''')

        # Confirmar cambios
        conexion.commit()
        print(f"Base de datos '{NOMBRE_DB}' y tabla '{NOMBRE_TABLA}' verificadas/creadas.")
    except sqlite3.Error as e:
        # Informar error de SQLite
        print(f"Error al crear la base de datos: {e}")
    finally:
        # Asegurar cierre de la conexión
        if conexion:
            conexion.close()


if __name__ == '__main__':
    # Ejecutar creación si se llama directamente
    crear_base_de_datos()