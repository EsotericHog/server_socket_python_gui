#Integrantes de servidor:Polett Casanga Rojas,Juan Castillo Lizama,Guilliano Punulaf,Kassandra Ramos
#Fecha de creación:03/10/2025
#Fecha de modificación:14/10/2025
#Descripcion:Define la configuración base del sistema: el servidor TCP escucha en HOST:PUERTO 
# y recibe datos en bloques de tamaño TAMANO_BUFFER; luego esos datos se almacenan en una base 
# SQLite cuyo archivo es NOMBRE_DB y cuya tabla objetivo es NOMBRE_TABLA.

# Configuración de red
HOST = '127.0.0.1'  # IP del servidor por defecto
PUERTO = 65432      # Puerto por defecto para escuchar conexiones
TAMANO_BUFFER = 4096  # Definir el tamaño del buffer para recibir datos


# Configuración de la base de datos MySQL
# ATENCIÓN: Ajusta estos valores a tu servidor MySQL local
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # Coloca tu contraseña de root si tienes una
    'database': 'deforestacion_db' # Nombre de la base de datos a usar/crear
}

# Nombre de la tabla a usar
NOMBRE_TABLA = 'registros_deforestacion'