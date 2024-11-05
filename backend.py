import sqlite3
from datetime import datetime

# Conectar a la base de datos
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def connect(self):
        """Conecta a la base de datos SQLite."""
        return sqlite3.connect(self.db_name)

    # Métodos para la tabla productos
    def obtener_producto_por_nombre(self, nombre):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
            producto = cursor.fetchone()
            return producto

    def actualizar_stock_producto(self, id_producto, cantidad):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id_producto))
            db.commit()

    def agregar_producto(self, nombre, cantidad, precio):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
            db.commit()

    def actualizar_cantidad(self, nombre_producto, nueva_cantidad):
        """Actualiza la cantidad de un producto en la base de datos."""
        try:
            with self.connect() as db:
                cursor = db.cursor()
                cursor.execute("UPDATE productos SET cantidad = cantidad + ? WHERE nombre = ?", (nueva_cantidad, nombre_producto))
                db.commit()
                return True  # Indica que la actualización fue exitosa
        except Exception as e:
            print(f"Error al actualizar la cantidad: {e}")
            return False  # Indica que hubo un error

    def actualizar_precio(self, nombre_producto, nuevo_precio):
        """Actualiza el precio de un producto en la base de datos."""
        try:
            with self.connect() as db:
                cursor = db.cursor()
                cursor.execute("UPDATE productos SET precio = ? WHERE nombre = ?", (nuevo_precio, nombre_producto))
                db.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar el precio: {e}")
            return False

    def actualizar_nombre(self, nombre_producto, nuevo_nombre):
        """Actualiza el nombre de un producto en la base de datos."""
        try:
            with self.connect() as db:
                cursor = db.cursor()
                cursor.execute("UPDATE productos SET nombre = ? WHERE nombre = ?", (nuevo_nombre, nombre_producto))
                db.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar el nombre: {e}")
            return False

    # Métodos para la tabla carrito
    def agregar_al_carrito(self, id_producto, cantidad, precio):
        with self.connect() as db:
            cursor = db.cursor()
            total = cantidad * precio
            cursor.execute("INSERT INTO carrito (id_producto, cantidad, precio, total) VALUES (?, ?, ?, ?)", (id_producto, cantidad, precio, total))
            db.commit()

    def obtener_carrito(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM carrito")
            carrito = cursor.fetchall()
            return carrito

    def limpiar_carrito(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM carrito")
            db.commit()

    # Métodos para la tabla historial ventas
    def registrar_venta(self, detalle, total):
        with self.connect() as db:
            cursor = db.cursor()
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")
            cursor.execute("INSERT INTO historial_ventas (detalle, fecha, hora, total) VALUES (?, ?, ?, ?)", (detalle, fecha, hora, total))
            db.commit()

    def obtener_historial_ventas(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM historial_ventas")
            historial = cursor.fetchall()
            return historial
        
    def obtener_detalles_venta(self,venta_id):
        with self.connect as db:
            c = db.cursor()

            c.execute("""
            SELECT productos.nombre, detalle_venta.cantidad, detalle_venta.precio_un
            FROM detalle_venta
            JOIN productos ON productos.id = detalle_venta.producto_id
            WHERE detalle_venta.venta_id = ?
            """, (venta_id,))
            detalles = c.fetchall()
            db.close()
            return detalles

