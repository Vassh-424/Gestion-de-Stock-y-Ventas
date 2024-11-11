import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def connect(self):
        """Conecta a la base de datos SQLite."""
        return sqlite3.connect(self.db_name)

######METODOS PARA STOCK########
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
        
    def eliminar_producto(self, nombre_producto):
        """Elimina un producto de la base de datos."""
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre_producto,))
            producto = cursor.fetchone()
            
            if producto:
                cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre_producto,))
                db.commit()
                return True
            return False

######METODOS PARA NUEVA VENTA###############
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
            
    def registrar_venta(self, detalle, total):
        with self.connect() as db:
            cursor = db.cursor()
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")
            cursor.execute("INSERT INTO historial_ventas (detalle, fecha, hora, total) VALUES (?, ?, ?, ?)", (detalle, fecha, hora, total))
            db.commit()
            
    def buscar_productos(self,nombre_producto): #Ventas
        """
        Función que busca productos que coincidan con el nombre proporcionado. no confundir con buscar_producto_por_nombre ni obtener_producto por nombre
        """
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute("SELECT nombre FROM productos WHERE nombre LIKE ?", ('%' + nombre_producto + '%',))
        productos = c.fetchall()
        db.close()
        return productos
    
    def buscar_producto_por_nombre(self, nombre_producto): #Ventas
        """
        #Función que busca un producto por nombre y devuelve su id, nombre, precio y cantidad. No confundir con buscar_productos
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, cantidad FROM productos WHERE nombre = ?", (nombre_producto,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    def insertar_venta(self, fecha, hora, total): #Ventas
        """
        Inserta una nueva venta en la tabla historial_ventas y devuelve el ID de la venta recién creada.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historial_ventas (fecha, hora, total) VALUES (?, ?, ?)", (fecha, hora, total))
        id_venta = cursor.lastrowid
        conn.commit()
        conn.close()
        return id_venta

    def insertar_detalle_venta(self, venta_id, producto_id, cantidad, precio_unitario, total): #Ventas
        """
        Inserta un detalle de venta en la tabla detalle_venta.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_un, total) VALUES (?, ?, ?, ?, ?)", 
                       (venta_id, producto_id, cantidad, precio_unitario, total))
        conn.commit()
        conn.close()
        
    def actualizar_cantidad_producto(self, producto_id, cantidad_vendida): #Ventas
        """
        Actualiza la cantidad disponible de un producto en la tabla productos.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?", (cantidad_vendida, producto_id))
        conn.commit()
        conn.close()

#######METODOS PARA HISTORIAL###############

    def obtener_historial_ventas(self):
        with self.connect() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM historial_ventas")
            historial = cursor.fetchall()
            return historial
   
    def buscar_ventas_por_fecha(self, dia=None, mes=None, anio=None):
        query = "SELECT id, fecha, hora, total FROM historial_ventas"
        conditions = []
        parameters = []

        if dia:
            conditions.append("DAY(fecha) = ?")
            parameters.append(dia)
        if mes:
            conditions.append("MONTH(fecha) = ?")
            parameters.append(mes)
        if anio:
            conditions.append("YEAR(fecha) = ?")
            parameters.append(anio)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Ordenar por fecha y hora descendente
        query += " ORDER BY strftime('%Y-%m-%d %H:%M:%S', fecha) DESC"

        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, tuple(parameters))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
            
    def obtener_ventas():
        db = sqlite3.connect("database.db")
        c = db.cursor()
        c.execute("SELECT id, fecha, hora, total FROM ventas ORDER BY fecha DESC")
        ventas = c.fetchall()
        db.close()
        return ventas

    def obtener_detalles_venta(self, venta_id):
        try:
            db = sqlite3.connect("database.db")  # Conectar manualmente
            c = db.cursor()

            query = """
            SELECT productos.nombre, detalle_venta.cantidad, detalle_venta.precio_un
            FROM detalle_venta
            JOIN productos ON productos.id = detalle_venta.producto_id
            WHERE detalle_venta.venta_id = ?
            """
            c.execute(query, (venta_id,))
            detalles = c.fetchall()
            return detalles
        except sqlite3.Error as e:
            print(f"Error al consultar detalles de venta: {e}")
            return []
        finally:
            if c:
                c.close()  # Asegurarse de cerrar el cursor
            if db:
                db.close()  # Asegurarse de cerrar la conexión