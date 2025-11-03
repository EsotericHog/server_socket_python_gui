#Integrantes de servidor:Polett Casanga Rojas,Juan Castillo Lizama,Guilliano Punulaf,Kassandra Ramos
#Fecha de creación:03/10/2025
#Fecha de modificación:14/10/2025
# Descripcion: DAO MySQL (PyMySQL): se conecta a la DB; inserta masivo (executemany) y obtiene todas las filas; 
# maneja errores y cierra conexiones.


import pymysql
from config import MYSQL_CONFIG, NOMBRE_TABLA


def _obtener_conexion():
    """
    Función helper para obtener una conexión a la base de datos MySQL.
    """
    try:
        conexion = pymysql.connect(**MYSQL_CONFIG)
        return conexion
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos PyMySQL: {e}")
        return None

def insertar_datos_masivos(lista_de_registros):
    """Insertar una lista de registros en la base de datos MySQL.

    - Convertir cada registro al tuple esperado por la tabla.
    - Ejecutar un executemany para insertar en bloque.
    - Manejar errores y cerrar la conexión.
    """
    conexion = _obtener_conexion()
    if not conexion:
        return False

    # Preparar tuplas con el orden de columnas de la tabla
    registros_a_insertar = [
        (r['pais'], r['codigo'], r['año'], r['perdida_de_bosques_en_hectareas'])
        for r in lista_de_registros
    ]

    try:
        # Usar 'with' para asegurar que el cursor se cierre
        with conexion.cursor() as cursor:
            # Insertar todos los registros en una única operación
            # PyMySQL usa %s como placeholder
            cursor.executemany(f'''
                INSERT INTO {NOMBRE_TABLA} (pais, codigo, año, perdida_hectareas)
                VALUES (%s, %s, %s, %s)
            ''', registros_a_insertar)
        
        conexion.commit()
        print(f"Se insertaron {len(registros_a_insertar)} registros en MySQL (PyMySQL).")
        return True
    except pymysql.Error as e:
        # Informar error y devolver False
        print(f"Error al insertar datos masivos en PyMySQL: {e}")
        conexion.rollback() # Revertir cambios en caso de error
        return False
    finally:
        # Asegurar cierre de la conexión
        if conexion:
            conexion.close()


def obtener_todos_los_datos():
    """Recuperar todos los registros de la base de datos MySQL.

    - Ejecutar SELECT para obtener filas completas.
    - Manejar excepciones y cerrar la conexión.
    """
    conexion = _obtener_conexion()
    if not conexion:
        return []

    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"SELECT id, pais, codigo, año, perdida_hectareas FROM {NOMBRE_TABLA}")
            return cursor.fetchall()
    except pymysql.Error as e:
        print(f"Error al obtener datos de PyMySQL: {e}")
        return []
    finally:
        if conexion:
            conexion.close()