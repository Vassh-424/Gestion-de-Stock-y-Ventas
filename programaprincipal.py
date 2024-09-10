import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import database

database.crear_tablas()

######## FUNCIONES DE STOCK

#### VENTANA AGREGAR PRODUCTO
def ventana_agregar():
    window = tk.Toplevel()
    window.geometry("512x512")
    tk.Label(window, text="AGREGAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)
 
    # Variable producto
    entryproducto = tk.StringVar()
    tk.Entry(window, textvariable=entryproducto).place(x=50, y=150)

    # Variable precio
    entryprecio = tk.StringVar()
    tk.Entry(window, textvariable=entryprecio).place(x=50, y=230)
    
    # Variable cantidad
    entrycantidad = tk.StringVar()
    tk.Entry(window, textvariable=entrycantidad).place(x=50, y=310)
    
    # Etiquetas
    tk.Label(window, text="INGRESE NOMBRE DEL PRODUCTO.", padx=10).place(x=30, y=115)
    tk.Label(window, text="INGRESE PRECIO DEL PRODUCTO", padx=10).place(x=30, y=200)
    tk.Label(window, text="INGRESE CANTIDAD DEL PRODUCTO", padx=10).place(x=30, y=280)

    # Boton para regresar al MENU
    menu = tk.Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=450)

    ####FUNCION PARA AGREGAR LOS PRODUCTOS
    def guarda():
        nombre = entryproducto.get()
        precio = entryprecio.get()
        cantidad = entrycantidad.get()
        
        if not nombre or not precio or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser un número y cantidad debe ser un entero")
            return
        
        # Conectar a la base de datos y agregar el artículo
        database.agregar_articulo(nombre, precio, cantidad)
        messagebox.showinfo("MODIFICACION", "ARTICULO INGRESADO")
        window.destroy()
        ventana_agregar()  # Reabrir la ventana de agregar para continuar ingresando productos

    # Botón para guardar los datos ingresados
    btguardar = tk.Button(window, text="GUARDAR", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=guarda)
    btguardar.pack()
    btguardar.place(x=300, y=450)

#### VENTANA BUSCAR PRODUCTOS

def ventana_ver():
    window = tk.Toplevel()
    window.geometry("600x512")
    tk.Label(window, text="BUSCAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)
    tk.Label(window, text="CODIGO", bg="white", fg="black").place(x=50, y=70)
    tk.Label(window, text="NOMBRE", bg="white", fg="black").place(x=150, y=70)
    tk.Label(window, text="PRECIO", bg="white", fg="black").place(x=250, y=70)
    tk.Label(window, text="CANTIDAD", bg="white", fg="black").place(x=350, y=70)

    def mostrar():
        lista = tk.Listbox(window, width=80, font=("arial", 12), height=15)
        lista.pack()
        
        # Conectar a la base de datos
        db = sqlite3.connect("articulos.s3db")
        c = db.cursor()
        
        # Consulta para obtener los datos de los artículos
        c.execute('SELECT codigo, nombre, precio, cantidad FROM articulos ORDER BY codigo DESC')
        
        for row in c.fetchall():
            lista.insert(tk.END, f"{row[0]:<10} {row[1]:<20} {row[2]:<10} {row[3]:<10}")
        
        lista.place(x=50, y=100)
        
        # Cerrar la conexión y el cursor
        c.close()
        db.close()

    menu = tk.Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=450)
    mostrar()


##### VENTANA ELIMINAR PRODUCTOS
def ventana_eliminar():
    window = tk.Toplevel()
    window.geometry("512x512")
    e1 = tk.Label(window, text=" ELIMINAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)
    
    # Variable para ID
    entry_id = tk.StringVar()
    productotx = tk.Entry(window, textvariable=entry_id).place(x=50, y=150)

    # Etiqueta para ID
    etiquetanombre = tk.Label(window, text="INGRESE CODIGO DEL PRODUCTO", padx=10).place(x=30, y=115)

    ##### FUNCION PARA ELIMINAR EL PRODUCTO
    def eliminar():
        db = sqlite3.connect("articulos.s3db")
        c = db.cursor()

        id_producto = entry_id.get()
    
        c.execute("DELETE FROM articulos WHERE codigo = ?", (id_producto,))
        db.commit()
        c.close()
        db.close()
        messagebox.showinfo("MODIFICACION", "ARTICULO ELIMINADO")
        window.destroy()
        ventana_eliminar()
        
    # Boton para MENU
    menu = tk.Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=350)
    
    # Boton para ELIMINAR
    bt_eliminar = tk.Button(window, text="ELIMINAR PRODUCTOS", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=eliminar)
    bt_eliminar.pack()
    bt_eliminar.place(x=280, y=350)


##### VENTANA MODIFICAR PRODUCTO
def modificar_producto():
    window = tk.Toplevel()
    window.geometry("512x512")
    e1 = tk.Label(window, text=" MODIFICAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)
    
    # Variable para ID
    entry_id = tk.StringVar()
    productotx = tk.Entry(window, textvariable=entry_id).place(x=50, y=150)

    # Etiqueta para ID
    etiquetanombre = tk.Label(window, text="INGRESE CODIGO DEL PRODUCTO", padx=10).place(x=30, y=100)

    # Variable para nuevo valor
    entry_valor = tk.StringVar()
    valortx = tk.Entry(window, textvariable=entry_valor).place(x=50, y=250)

    # Etiqueta para nuevo valor
    etiquetanombre = tk.Label(window, text="INGRESE EL NUEVO PRECIO PARA EL PRODUCTO", padx=10).place(x=30, y=200)

    ####FUNCION PARA MODIFICAR EL PRODUCTO
    def modificar():
        db = sqlite3.connect("articulos.s3db")
        c = db.cursor()

        id_producto = entry_id.get()
        nuevo_precio = entry_valor.get()
    
        c.execute("UPDATE articulos SET precio = ? WHERE codigo = ?", (nuevo_precio, id_producto))
        db.commit()
        c.close()
        db.close()
        messagebox.showinfo("MODIFICACION", "ARTICULO MODIFICADO")
        window.destroy()
        modificar_producto()

    # Boton para MENU
    menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=350)
    
    # Boton para MODIFICAR
    bt_modificar = tk.Button(window, text="MODIFICAR PRODUCTO", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=modificar)
    bt_modificar.pack()
    bt_modificar.place(x=280, y=350)

def ventana_ver_ventas():
    window = tk.Toplevel()
    window.geometry("800x600")
    window.title("Ventas Realizadas")

    tk.Label(window, text="VENTAS REALIZADAS :", bg="white", fg="black").place(x=50, y=50)

    # Crear una lista para mostrar las ventas
    lista_ventas = tk.Listbox(window, width=100, height=25, font=("Arial", 12))
    lista_ventas.place(x=50, y=100)

    # Conectar a la base de datos y obtener las ventas
    db = sqlite3.connect("articulos.s3db")
    c = db.cursor()

    c.execute('''
        SELECT v.id, v.fecha, v.total, vd.codigo_producto, vd.cantidad, a.nombre
        FROM ventas v
        LEFT JOIN ventas_detalle vd ON v.id = vd.venta_id
        LEFT JOIN articulos a ON vd.codigo_producto = a.codigo
        ORDER BY v.fecha DESC
    ''')

    ventas = c.fetchall()
    db.close()

    # Mostrar las ventas en la lista
    for venta in ventas:
        lista_ventas.insert(tk.END, f"ID Venta: {venta[0]} | Fecha: {venta[1]} | Total: ${venta[2]:.2f} | Producto: {venta[5]} | Cantidad: {venta[4]}")

    # Botón para volver al menú
    menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=550)


####### VENTANA GESTION DE STOCK

def ventana_stock():
    window = tk.Toplevel()
    window.geometry("900x550")
    window.attributes("-fullscreen", True)  # Pantalla completa no resizable
    tk.Label(window, text="STOCK :", bg="white", fg="black").place(x=5, y=50)
    tk.Label(window, text="VENTAS :", bg="white", fg="black").place(x=800, y=50)

    b1 = tk.Button(window, text="Agregar Producto", fg="blue", font=("arial", 14), borderwidth=10, cursor="hand2", relief="raised", command=ventana_agregar)
    b1.pack()
    b1.place(x=5, y=100)

    b2 = tk.Button(window, text="Buscar Producto", fg="blue", font=("arial", 14), borderwidth=10, cursor="hand2", relief="raised", command=ventana_ver)
    b2.pack()
    b2.place(x=5, y=200)

    b3 = tk.Button(window, text="Eliminar Producto", fg="blue", font=("arial", 14), borderwidth=10, cursor="hand2", relief="raised", command=ventana_eliminar)
    b3.pack()
    b3.place(x=5, y=300)

    b4 = tk.Button(window, text="Modificar Producto", fg="blue", font=("arial", 14), borderwidth=10, cursor="hand2", relief="raised", command=modificar_producto)
    b4.pack()
    b4.place(x=5, y=400)

    b8 = tk.Button(window, text="Ver Ventas", fg="blue", font=("arial", 14), borderwidth=10, cursor="hand2", relief="raised", command=ventana_ver_ventas)
    b8.pack()
    b8.place(x=800, y=100)

    menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=5, y=550)


########## FIN SECCION DE GESTION DE STOCK #############

########## FUNCIONES DE NUEVA VENTA

####### VENTANA NUEVA VENTA

def ventana_crear_compra():
    window = tk.Toplevel()
    window.geometry("800x600")
    window.title("Nueva Venta")

    tk.Label(window, text="NUEVA VENTA :", bg="white", fg="black").place(x=50, y=50)

    # Variable para ID del producto
    entry_id = tk.StringVar()
    tk.Entry(window, textvariable=entry_id).place(x=50, y=150)

    # Etiqueta para ID del producto
    tk.Label(window, text="INGRESE CODIGO DEL PRODUCTO", padx=10).place(x=30, y=115)

    # Variable para cantidad
    entry_cantidad = tk.StringVar()
    tk.Entry(window, textvariable=entry_cantidad).place(x=50, y=230)

    # Etiqueta para cantidad
    tk.Label(window, text="CANTIDAD", padx=10).place(x=30, y=200)

    # Lista para los productos de la compra
    lista_compra = tk.Listbox(window, width=60, height=20, font=("Arial", 12))
    lista_compra.place(x=300, y=100)

    # Etiqueta para el total de la compra
    total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 14))
    total_label.place(x=300, y=500)

    # Variable para el total de la compra
    global total_compra
    total_compra = 0.0

    # Lista de productos en la compra
    global productos_compra
    productos_compra = []

    ##### FUNCION PARA AGREGAR PRODUCTO A LA COMPRA

    def agregar_producto():
        db = sqlite3.connect("articulos.s3db")
        c = db.cursor()

        id_producto = entry_id.get()
        cantidad = int(entry_cantidad.get())

        # Obtener el nombre, precio unitario y cantidad disponible del producto
        c.execute("SELECT nombre, precio, cantidad FROM articulos WHERE codigo = ?", (id_producto,))
        resultado = c.fetchone()
        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado")
            db.close()
            return
        nombre_producto, precio_unitario, cantidad_disponible = resultado

        # Verificar si la cantidad solicitada es mayor a la disponible
        if cantidad > cantidad_disponible:
            messagebox.showerror("Error", "Cantidad solicitada excede la cantidad disponible")
            db.close()
            return

        # Calcular el monto total del producto
        monto_producto = cantidad * precio_unitario

        # Añadir producto a la lista de compra
        productos_compra.append((id_producto, cantidad, precio_unitario))
        lista_compra.insert(tk.END, f"{nombre_producto} - Cantidad: {cantidad} - Precio: ${monto_producto:.2f}")

        # Actualizar el total de la compra
        global total_compra
        total_compra += monto_producto
        total_label.config(text=f"Total: ${total_compra:.2f}")

        db.close()

    bt_agregar_producto = tk.Button(window, text="AÑADIR A LA COMPRA", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=agregar_producto)
    bt_agregar_producto.pack()
    bt_agregar_producto.place(x=50, y=300)

    ##### FUNCION PARA REALIZAR LA VENTA

    def realizar_venta():
        if not productos_compra:
            messagebox.showerror("Error", "No hay productos en la compra")
            return

        db = sqlite3.connect("articulos.s3db")
        c = db.cursor()

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Registrar la venta en la tabla 'ventas'
        c.execute("INSERT INTO ventas (fecha, total) VALUES (?, ?)", (fecha_actual, total_compra))
        id_venta = c.lastrowid

        # Registrar los detalles de la venta y actualizar cantidades
        for id_producto, cantidad, precio_unitario in productos_compra:
            c.execute("INSERT INTO ventas_detalle (venta_id, codigo_producto, cantidad) VALUES (?, ?, ?)",
                      (id_venta, id_producto, cantidad))
            c.execute("UPDATE articulos SET cantidad = cantidad - ? WHERE codigo = ?", (cantidad, id_producto))

        db.commit()
        db.close()

        messagebox.showinfo("VENTA REALIZADA", f"Venta realizada por un monto total de ${total_compra:.2f}")
        window.destroy()

    # Botón para realizar la venta
    bt_vender = tk.Button(window, text="REALIZAR VENTA", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=realizar_venta)
    bt_vender.pack()
    bt_vender.place(x=300, y=550)

    # Botón para volver al menú
    menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
    menu.pack()
    menu.place(x=50, y=550)
#modificar

########### FIN SECCION NUEVA VENTA #############

######### VENTANA PRINCIPAL

def cerrar_programa():
    windows.destroy()  # O también puedes usar windows.quit()

windows=tk.Tk()
windows.title("Gestor De Ventas y Stock");
windows.geometry("1600x900")
windows.resizable(0,0)  # Pantalla completa no resizable

b7=tk.Button(windows,text="Stock y Ventas", fg="blue", font=("arial", 50), borderwidth=5, cursor = "hand2",relief = "raised", command = ventana_stock)
b7.pack()
b7.place(x=575,y=150)

b5=tk.Button(windows,text="Nueva Venta", fg="blue", font=("arial", 50), borderwidth=5, cursor = "hand2",relief = "raised", command = ventana_crear_compra)
b5.pack()
b5.place(x=600,y=400)

b5=tk.Button(windows,text="Salir", fg="red", font=("arial", 25), borderwidth=5, cursor = "hand2",relief = "raised", command = cerrar_programa)
b5.pack()
b5.place(x=770,y=650)


windows.mainloop()