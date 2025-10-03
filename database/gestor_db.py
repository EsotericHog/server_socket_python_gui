import sqlite3
import os
from config import NOMBRE_DB, NOMBRE_TABLA


# Calcular ruta absoluta del archivo de base de datos
directorio_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_db = os.path.join(directorio_proyecto, NOMBRE_DB)


def insertar_datos_masivos(lista_de_registros):
    """Insertar una lista de registros en la base de datos.

    - Convertir cada registro al tuple esperado por la tabla.
    - Ejecutar un executemany para insertar en bloque.
    - Manejar errores y cerrar la conexión.
    """
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    # Preparar tuplas con el orden de columnas de la tabla
    registros_a_insertar = [
        (r['pais'], r['codigo'], r['año'], r['perdida_de_bosques_en_hectareas'])
        for r in lista_de_registros
    ]

    try:
        # Insertar todos los registros en una única operación
        cursor.executemany(f'''
            INSERT INTO {NOMBRE_TABLA} (pais, codigo, año, perdida_hectareas)
            VALUES (?, ?, ?, ?)
        ''', registros_a_insertar)
        conexion.commit()
        print(f"Se insertaron {len(registros_a_insertar)} registros.")
        return True
    except sqlite3.Error as e:
        # Informar error y devolver False
        print(f"Error al insertar datos masivos: {e}")
        return False
    finally:
        # Asegurar cierre de la conexión
        conexion.close()


def obtener_todos_los_datos():
    """Recuperar todos los registros de la base de datos.

    - Ejecutar SELECT para obtener filas completas.
    - Manejar excepciones y cerrar la conexión.
    """
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    try:
        cursor.execute(f"SELECT id, pais, codigo, año, perdida_hectareas FROM {NOMBRE_TABLA}")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos: {e}")
        return []
    finally:
        conexion.close()