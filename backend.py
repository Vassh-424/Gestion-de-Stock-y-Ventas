import sqlite3
from datetime import datetime

# Conectar a la base de datos
def connect_db():
    return sqlite3.connect('database.db')

# Funciones para la tabla productos
def obtener_producto_por_nombre(nombre):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
    producto = cursor.fetchone()
    db.close()
    return producto

def actualizar_stock_producto(id_producto, cantidad):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id_producto))
    db.commit()
    db.close()

def agregar_producto(nombre, cantidad, precio):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
    db.commit()
    db.close()

# Funciones para la tabla carrito
def agregar_al_carrito(id_producto, cantidad, precio):
    db = connect_db()
    cursor = db.cursor()
    total = cantidad * precio
    cursor.execute("INSERT INTO carrito (id_producto, cantidad, precio, total) VALUES (?, ?, ?, ?)", (id_producto, cantidad, precio, total))
    db.commit()
    db.close()

def obtener_carrito():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM carrito")
    carrito = cursor.fetchall()
    db.close()
    return carrito

def limpiar_carrito():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carrito")
    db.commit()
    db.close()

# Funciones para la tabla historial ventas
def registrar_venta(detalle, total):
    db = connect_db()
    cursor = db.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO historial_ventas (detalle, fecha, hora, total) VALUES (?, ?, ?, ?)", (detalle, fecha, hora, total))
    db.commit()
    db.close()

def obtener_historial_ventas():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM historial_ventas")
    historial = cursor.fetchall()
    db.close()
    return historial
