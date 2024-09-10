import sqlite3

def conectar():
    try:
        conn = sqlite3.connect('articulos.s3db')
        print("Base de datos conectada")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")

def crear_tablas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articulos (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER DEFAULT 0,
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas_temporales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_producto INTEGER,
                cantidad INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas_detalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                codigo_producto INTEGER,
                cantidad INTEGER,
                FOREIGN KEY(venta_id) REFERENCES ventas(id),
                FOREIGN KEY(codigo_producto) REFERENCES articulos(codigo)
            )
        ''')
        conn.commit()
        print("Tablas creadas exitosamente")
    except sqlite3.Error as e:
        print(f"Error al crear tablas: {e}")
    finally:
        conn.close()

def agregar_articulo(nombre, precio, cantidad, nombre_proveedor):
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO articulos (nombre, precio, cantidad) VALUES (?, ?, ?)', (nombre, precio, cantidad))
        conn.commit()
        print("Artículo agregado exitosamente")
    except sqlite3.Error as e:
        print(f"Error al agregar artículo: {e}")
    finally:
        conn.close()

    
def obtener_articulos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.codigo, a.nombre, a.precio, a.cantidad
            FROM articulos a  
            ORDER BY a.codigo DESC
        ''')
        articulos = cursor.fetchall()
        return articulos
    except sqlite3.Error as e:
        print(f"Error al obtener artículos: {e}")
    finally:
        conn.close()

def eliminar_articulo(codigo):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articulos WHERE codigo = ?', (codigo,))
        conn.commit()
        print("Artículo eliminado exitosamente")
    except sqlite3.Error as e:
        print(f"Error al eliminar artículo: {e}")
    finally:
        conn.close()

def modificar_articulo(codigo, nuevo_precio):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('UPDATE articulos SET precio = ? WHERE codigo = ?', (nuevo_precio, codigo))
        conn.commit()
        print("Artículo modificado exitosamente")
    except sqlite3.Error as e:
        print(f"Error al modificar artículo: {e}")
    finally:
        conn.close()

def agregar_venta_temporal(conn, codigo_producto, cantidad):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ventas_temporales (codigo_producto, cantidad) VALUES (?, ?)', (codigo_producto, cantidad))
        conn.commit()
        print("Venta temporal agregada exitosamente")
    except sqlite3.Error as e:
        print(f"Error al agregar venta temporal: {e}")

def confirmar_venta():
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Obtener los detalles de la venta temporal
        cursor.execute('SELECT * FROM ventas_temporales')
        ventas_temporales = cursor.fetchall()
        
        total_venta = 0.0
        
        # Calcular el total de la venta y transferir a la tabla 'ventas'
        for venta in ventas_temporales:
            cursor.execute('SELECT precio FROM articulos WHERE codigo = ?', (venta[1],))
            precio_unitario = cursor.fetchone()[0]
            total_producto = precio_unitario * venta[2]
            total_venta += total_producto
        
        # Insertar la venta en la tabla 'ventas'
        cursor.execute('INSERT INTO ventas (total) VALUES (?)', (total_venta,))
        venta_id = cursor.lastrowid
        
        # Transferir los detalles de la venta temporal a la tabla 'ventas'
        for venta in ventas_temporales:
            cursor.execute('INSERT INTO ventas_detalle (venta_id, codigo_producto, cantidad) VALUES (?, ?, ?)', (venta_id, venta[1], venta[2]))
        
        # Limpiar la tabla 'ventas_temporales'
        cursor.execute('DELETE FROM ventas_temporales')
        
        conn.commit()
        print(f"Venta confirmada exitosamente. Total: {total_venta}")
    except sqlite3.Error as e:
        print(f"Error al confirmar la venta: {e}")
    finally:
        conn.close()

def obtener_ventas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ventas')
        ventas = cursor.fetchall()
        return ventas
    except sqlite3.Error as e:
        print(f"Error al obtener ventas: {e}")
    finally:
        conn.close()

# Crear las tablas si no existen
crear_tablas()
