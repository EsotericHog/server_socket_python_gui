# Servidor de Datos de Deforestación

## Descripción del Proyecto

Proyecto universitario que implementa la parte del **servidor** de una aplicación cliente-servidor. Está desarrollado en Python y es capaz de recibir datasets sobre la deforestación global.

La aplicación utiliza sockets para la comunicación, una base de datos SQLite para la persistencia de datos y una interfaz gráfica de usuario (GUI) construida con Tkinter para la gestión y visualización.

### Entorno de Operación
Actualmente, el proyecto está diseñado para operar de forma local, es decir, el cliente y el servidor deben ejecutarse en la misma computadora.

### Flujo de Trabajo

1.  El servidor se inicia desde la GUI y queda a la espera de conexiones.
2.  Un cliente se conecta y envía un *payload* en formato JSON.
3.  El servidor recibe los datos y los muestra en una tabla dentro de la GUI para su revisión.
4.  El usuario puede visualizar los datos y, mediante un botón, guardarlos permanentemente en la base de datos local.

## Instrucciones de Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el servidor en tu máquina local.

### Prerrequisitos

-   Tener instalado [Python 3](https://www.python.org/downloads/).

### Pasos de Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_CARPETA_PROYECTO>
    ```

2.  **Ejecutar el Servidor:**
    Para iniciar la aplicación, ejecuta el programa principal. Se abrirá la ventana de la interfaz gráfica.
    ```bash
    py main.py
    ```
    Una vez abierta la ventana, ingresa el `Host` y `Puerto` deseados y presiona **"Iniciar Servidor"**.

## Protocolo de Comunicación (Guía para el Equipo Cliente)
Esta sección detalla todo lo necesario para que el software cliente pueda comunicarse exitosamente con este servidor.

### 1. Conexión (Host y Puerto)
El servidor no utiliza un host o puerto fijos. El operador del servidor los ingresará manualmente en la interfaz gráfica al momento de iniciarlo. Sin embargo, los valores por defecto son los siguientes:

- Host: 127.0.0.1
- Puerto: 65432

### 2. Formato de Datos

El servidor espera recibir una única cadena de texto (string) codificada en `UTF-8` que contenga un **JSON válido**.

El JSON debe ser una **lista de objetos**, donde cada objeto representa un registro y debe contener las siguientes claves:

-   `pais` (string)
-   `codigo` (string)
-   `año` (integer)
-   `perdida_de_bosques_en_hectareas` (float/integer)

#### Ejemplo de JSON Válido:

```json
[
  {
    "pais": "Brazil",
    "codigo": "BRA",
    "año": 2021,
    "perdida_de_bosques_en_hectareas": 150000.75
  },
  {
    "pais": "Bolivia",
    "codigo": "BOL",
    "año": 2021,
    "perdida_de_bosques_en_hectareas": 290000.50
  },
  {
    "pais": "Democratic Republic of the Congo",
    "codigo": "COD",
    "año": 2022,
    "perdida_de_bosques_en_hectareas": 500000.0
  }
]
```

### 3. Protocolo de Control de Transmisión
El protocolo es simple y se basa en el comportamiento estándar de los sockets.

- **Establecer Conexión**: El cliente inicia una conexión **TCP** con el host y puerto especificados por el servidor.

- **Enviar Datos**: Una vez conectado, el cliente debe enviar el *payload* completo (toda la cadena JSON codificada en UTF-8) de una sola vez. Se recomienda usar `socket.sendall()` para asegurar que todos los datos se envíen.

- **Finalizar Envío y Esperar Respuesta**: Después de enviar todos los datos, el cliente no debe cerrar la conexión inmediatamente. Debe esperar a recibir una respuesta del servidor.

- **Recepción de Confirmación**: El servidor procesará los datos y enviará de vuelta un mensaje de confirmación (ej: `b"Datos recibidos por el servidor..."`). La recepción de este mensaje confirma que el envío fue exitoso.

- **Cierre de Conexión**: Una vez recibida la confirmación, el cliente puede cerrar la conexión de forma segura. El servidor detecta el fin de la comunicación cuando el cliente cierra su lado del socket, terminando así el ciclo para esa transacción.