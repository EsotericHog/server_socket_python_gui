import tkinter as tk
from tkinter import ttk, messagebox
from database import gestor_db
from config import HOST, PUERTO


class InterfazGrafica(tk.Tk):
    """Interfaz gráfica principal para controlar el servidor y visualizar datos.

    - Mostrar controles para host/puerto.
    - Mostrar tabla con los registros recibidos.
    - Permitir guardar los datos en la base de datos.
    """

    def __init__(self, servidor):
        super().__init__()
        # Asociar servidor (puede ser None inicialmente)
        self.servidor = servidor
        # Almacenar temporalmente los datos recibidos antes de guardarlos
        self.datos_recibidos_temporalmente = []

        # Configurar ventana
        self.title("Panel de Control del Servidor")
        self.geometry("900x600")
        self.minsize(700, 500)

        # --- Marco Superior para Controles ---
        marco_controles = ttk.Frame(self, padding="10")
        marco_controles.pack(fill=tk.X)

        # Host
        ttk.Label(marco_controles, text="Host:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.host_var = tk.StringVar(value=HOST)
        ttk.Entry(marco_controles, textvariable=self.host_var, width=15).grid(row=0, column=1, padx=(0, 10))

        # Puerto
        ttk.Label(marco_controles, text="Puerto:").grid(row=0, column=2, padx=(0, 5), sticky="w")
        self.puerto_var = tk.StringVar(value=PUERTO)
        ttk.Entry(marco_controles, textvariable=self.puerto_var, width=7).grid(row=0, column=3, padx=(0, 20))

        # Botones iniciar/detener
        self.boton_iniciar = ttk.Button(marco_controles, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.boton_iniciar.grid(row=0, column=4, padx=5)
        self.boton_detener = ttk.Button(marco_controles, text="Detener Servidor", command=self.detener_servidor, state="disabled")
        self.boton_detener.grid(row=0, column=5, padx=5)

        # --- Tabla para Visualización de Datos ---
        marco_tabla = ttk.Frame(self, padding="10")
        marco_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ('pais', 'codigo', 'año', 'perdida_hectareas')
        self.tabla_vista = ttk.Treeview(marco_tabla, columns=columnas, show='headings')

        # Definir encabezados
        self.tabla_vista.heading('pais', text='País')
        self.tabla_vista.heading('codigo', text='Código ISO3')
        self.tabla_vista.heading('año', text='Año')
        self.tabla_vista.heading('perdida_hectareas', text='Pérdida (Hectáreas)')

        # Ajustar ancho de columnas
        self.tabla_vista.column('pais', anchor=tk.W, width=250)
        self.tabla_vista.column('codigo', anchor=tk.CENTER, width=100)
        self.tabla_vista.column('año', anchor=tk.CENTER, width=100)
        self.tabla_vista.column('perdida_hectareas', anchor=tk.E, width=180)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.tabla_vista.yview)
        self.tabla_vista.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla_vista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Marco Inferior para Acciones y Estado ---
        marco_acciones = ttk.Frame(self, padding="10")
        marco_acciones.pack(fill=tk.X)
        
        # Botón para guardar datos en BD (inicialmente deshabilitado)
        self.boton_guardar = ttk.Button(marco_acciones, text="Guardar Datos en BD", command=self.guardar_datos_recibidos, state="disabled")
        self.boton_guardar.pack(side="left", padx=5)
        # Botón para limpiar la tabla
        self.boton_limpiar = ttk.Button(marco_acciones, text="Limpiar Tabla", command=self.limpiar_tabla, state="disabled")
        self.boton_limpiar.pack(side="left", padx=5)

        # Etiqueta de estado del servidor
        self.etiqueta_estado = ttk.Label(marco_acciones, text="Servidor Detenido", anchor="w")
        self.etiqueta_estado.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        # Manejar cierre de ventana para detener servidor correctamente
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def limpiar_tabla(self):
        # Borrar todas las filas de la vista de la tabla
        for item in self.tabla_vista.get_children():
            self.tabla_vista.delete(item)
        # Limpiar datos temporales en memoria
        self.datos_recibidos_temporalmente = []
        # Deshabilitar botones de acción hasta que haya nuevos datos
        self.boton_guardar.config(state="disabled")
        self.boton_limpiar.config(state="disabled")
        print("Log: Tabla y datos temporales limpiados.")

    def manejar_datos_recibidos(self, datos_brutos):
        # Limpiar la tabla antes de mostrar nuevos datos
        self.limpiar_tabla()

        if not datos_brutos:
            messagebox.showwarning("Datos Vacíos", "Se ha recibido una petición sin datos.")
            return
        
        # Nombres de columna que nuestro sistema usa internamente.
        nombres_internos = {'pais', 'codigo', 'año', 'perdida_de_bosques_en_hectareas'}
        
        # Nombres de columna que conocemos del cliente.
        nombres_cliente_original = {'zona_pais', 'iso3', 'anio', 'perdida_ha'}

        # Tomamos el primer registro para inspeccionar sus claves (nombres de columna).
        primer_registro = datos_brutos[0]
        claves_recibidas = set(primer_registro.keys())

        datos_mapeados = []

        # Estrategia 1: ¿Los datos ya vienen en nuestro formato interno?
        if nombres_internos.issubset(claves_recibidas):
            print("Log: Detectado formato interno. Procesando directamente.")
            for registro in datos_brutos:
                try:
                    registro['año'] = int(registro['año'])
                    registro['perdida_de_bosques_en_hectareas'] = float(registro['perdida_de_bosques_en_hectareas'])
                    datos_mapeados.append(registro)
                except (ValueError, KeyError) as e:
                    print(f"Log: Se omitió un registro (formato interno) por error de tipo/clave: {e}")

        # Estrategia 2: ¿Los datos vienen en el formato original del cliente?
        elif nombres_cliente_original.issubset(claves_recibidas):
            print("Log: Detectado formato del cliente. Realizando traducción.")
            for registro in datos_brutos:
                try:
                    registro_mapeado = {
                        'pais': registro['zona_pais'],
                        'codigo': registro['iso3'],
                        'año': int(registro['anio']),
                        'perdida_de_bosques_en_hectareas': float(registro['perdida_ha'])
                    }
                    datos_mapeados.append(registro_mapeado)
                except (ValueError, KeyError) as e:
                    print(f"Log: Se omitió un registro (formato cliente) por error de tipo/clave: {e}")
        
        # Estrategia 3: Formato desconocido.
        else:
            messagebox.showerror("Error de Formato", 
                "El formato de los datos recibidos es desconocido.\n\n"
                "Formatos aceptados:\n"
                f"1. {nombres_internos}\n"
                f"2. {nombres_cliente_original}")
            return

        # --- Fin de la lógica de mapeo ---

        if not datos_mapeados:
            messagebox.showerror("Error de Procesamiento", "Se recibieron datos, pero no se pudo procesar ningún registro válido.")
            return

        # Guardar los datos recibidos temporalmente
        self.datos_recibidos_temporalmente = datos_mapeados
        
        # Poblar la tabla con los registros recibidos
        for registro in self.datos_recibidos_temporalmente:
            # Asegurar orden correcto de columnas
            valores = (
                registro.get('pais', ''),
                registro.get('codigo', ''),
                registro.get('año', ''),
                registro.get('perdida_de_bosques_en_hectareas', '')
            )
            self.tabla_vista.insert('', tk.END, values=valores)
        
        # Informar al usuario y habilitar botones de acción
        messagebox.showinfo("Datos Recibidos", f"Se han recibido {len(datos_mapeados)} registros y se muestran en la tabla. \nPresione 'Guardar Datos en BD' para almacenarlos.")
        self.boton_guardar.config(state="normal")
        self.boton_limpiar.config(state="normal")

    def guardar_datos_recibidos(self):
        # Validar que existan datos para guardar
        if not self.datos_recibidos_temporalmente:
            messagebox.showwarning("Sin datos", "No hay datos nuevos para guardar.")
            return

        # Intentar insertar masivamente y notificar resultado
        if gestor_db.insertar_datos_masivos(self.datos_recibidos_temporalmente):
            messagebox.showinfo("Éxito", f"{len(self.datos_recibidos_temporalmente)} registros han sido guardados en la base de datos.")
            # Limpiar tabla después de guardar
            self.limpiar_tabla()
        else:
            messagebox.showerror("Error", "Ocurrió un error al guardar los datos en la base de datos.")

    def iniciar_servidor(self):
        # Obtener host y validar puerto
        host = self.host_var.get()
        try:
            puerto = int(self.puerto_var.get())
            if not (1024 <= puerto <= 65535): raise ValueError
        except ValueError:
            messagebox.showerror("Puerto Inválido", "Por favor, ingrese un número de puerto entre 1024 y 65535.")
            return

        # Llamar al servidor para iniciar escucha
        self.servidor.iniciar(host, puerto)
        # Actualizar estado de botones y etiqueta
        self.boton_iniciar.config(state="disabled")
        self.boton_detener.config(state="normal")
        self.etiqueta_estado.config(text=f"Servidor escuchando en {host}:{puerto}")

    def detener_servidor(self):
        # Llamar a detener y actualizar UI
        self.servidor.detener()
        self.boton_iniciar.config(state="normal")
        self.boton_detener.config(state="disabled")
        self.etiqueta_estado.config(text="Servidor Detenido")

    def cerrar_aplicacion(self):
        # Detener servidor antes de cerrar la aplicación
        self.servidor.detener()
        self.destroy()
