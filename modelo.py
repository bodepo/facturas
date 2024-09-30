import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Conexión a la base de datos
def conectar_db():
    conexion = sqlite3.connect("datos.db")
    cursor = conexion.cursor()
    
    # Crear tabla para los clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            edad INTEGER,
            telefono TEXT
        )
    ''')
    
    # Crear tabla para las facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            monto REAL,
            concepto TEXT,
            numero_factura TEXT,
            fecha TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    conexion.commit()
    return conexion

# Funciones del modelo para operar sobre la base de datos
def alta_cliente(nombre, edad, telefono):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute('''
        INSERT INTO clientes (nombre, edad, telefono)
        VALUES (?, ?, ?)
    ''', (nombre, edad, telefono))
    
    conexion.commit()
    conexion.close()

def modificar_cliente(id_cliente, nombre, edad, telefono):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute('''
        UPDATE clientes
        SET nombre = ?, edad = ?, telefono = ?
        WHERE id = ?
    ''', (nombre, edad, telefono, id_cliente))
    
    conexion.commit()
    conexion.close()

def baja_cliente(id_cliente):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute('''
        DELETE FROM clientes WHERE id = ?
    ''', (id_cliente,))
    
    conexion.commit()
    conexion.close()

def obtener_clientes():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre FROM clientes')
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

def obtener_datos_cliente(id_cliente):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT nombre, edad, telefono FROM clientes WHERE id = ?', (id_cliente,))
    datos_cliente = cursor.fetchone()
    
    conexion.close()
    
    return datos_cliente

def guardar_factura(cliente_id, monto, concepto, numero_factura):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    fecha = datetime.today().strftime('%Y-%m-%d')  # Cambié el formato a uno común de bases de datos
    cursor.execute('''
        INSERT INTO facturas (cliente_id, monto, concepto, numero_factura, fecha)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, monto, concepto, numero_factura, fecha))
    
    conexion.commit()
    conexion.close()

def obtener_facturas_cliente(id_cliente):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Seleccionar las facturas de un cliente específico
    cursor.execute('''
        SELECT id, numero_factura, monto, concepto, fecha
        FROM facturas
        WHERE cliente_id = ?
    ''', (id_cliente,))
    
    facturas = cursor.fetchall()
    conexion.close()
    return facturas

def generar_factura_pdf(nombre_cliente, monto, concepto, numero_factura):
    nombre_archivo = f"Factura_{numero_factura}.pdf"
    pdf = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(100, alto - 100, "Oficina")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, alto - 130, f"Fecha: {datetime.today().strftime('%d-%m-%Y')}")
    pdf.drawString(100, alto - 150, f"Factura N°: {numero_factura}")
    pdf.drawString(100, alto - 180, f"Nombre del cliente: {nombre_cliente}")
    pdf.drawString(100, alto - 200, f"Concepto: {concepto}")
    pdf.drawString(100, alto - 220, f"Monto: ${monto}")

    pdf.save()
