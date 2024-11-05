import main
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import backend

def ventas():
    window = tk.Toplevel()
    window.state("zoomed")
    window.title("Nueva Venta")
    window.resizable(0, 0)


    tk.Label(window, text="NUEVA VENTA :", bg="white", fg="black").place(x=50, y=50)


    # Variable para nombre del producto
    entry_nombre = tk.StringVar()
    entry_widget = tk.Entry(window, textvariable=entry_nombre)
    entry_widget.place(x=50, y=150)


    # Etiqueta para nombre del producto
    tk.Label(window, text="INGRESE NOMBRE DEL PRODUCTO", padx=10).place(x=30, y=115)


    # Variable para cantidad
    entry_cantidad = tk.StringVar()
    tk.Entry(window, textvariable=entry_cantidad).place(x=50, y=230)


    # Etiqueta para cantidad
    tk.Label(window, text="CANTIDAD", padx=10).place(x=30, y=200)


    # Frame para resaltar el carrito con fondo blanco y borde
    frame_carrito = tk.Frame(window, bg="white", relief="raised", bd=2)
    frame_carrito.place(x=300, y=100, width=800, height=500)


    # Crear el frame donde se mostrarán los productos de la compra
    frame_compra = tk.Frame(frame_carrito, bg="white")
    frame_compra.place(x=0, y=0, width=800, height=500)


    # Etiquetas de encabezado para las columnas
    tk.Label(frame_compra, text="Nombre", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame_compra, text="Cantidad", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame_compra, text="Precio Unitario", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=2, padx=10, pady=5)
    tk.Label(frame_compra, text="Total", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=3, padx=10, pady=5)


    # Variable para el total de la compra
    total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 14))
    total_label.place(x=300, y=600)


    # Variable global para el total
    global total_compra
    total_compra = 0.0


    # Variable para almacenar los productos añadidos
    productos_compra = []


    # Listbox para autocompletar
    lista_sugerencias = tk.Listbox(window, width=30, height=5, font=("Arial", 10))
    lista_sugerencias.place(x=50, y=180)  # Colocar justo debajo del Entry
    lista_sugerencias.place_forget()  # Ocultarla inicialmente


    def actualizar_sugerencias(event=None):
        """
        Función que busca productos que coincidan con el texto ingresado y actualiza la lista de sugerencias.
        """
        nombre_producto = entry_nombre.get()
        if not nombre_producto:
            lista_sugerencias.place_forget()
            return


        # Conectar a la base de datos y buscar coincidencias
        db = sqlite3.connect("database.db")
        c = db.cursor()


        c.execute("SELECT nombre FROM productos WHERE nombre LIKE ?", ('%' + nombre_producto + '%',))
        productos = c.fetchall()


        db.close()


        # Actualizar la Listbox con las sugerencias
        lista_sugerencias.delete(0, tk.END)  # Limpiar la lista previa


        if productos:
            for producto in productos:
                lista_sugerencias.insert(tk.END, producto[0])


            # Mostrar la Listbox si hay resultados
            lista_sugerencias.place(x=50, y=180)
        else:
            # Ocultar la Listbox si no hay coincidencias
            lista_sugerencias.place_forget()


    def seleccionar_sugerencia(event=None):
        """
        Función que se ejecuta al seleccionar un producto de la lista de sugerencias.
        """
        seleccion = lista_sugerencias.get(lista_sugerencias.curselection())  # Obtener el producto seleccionado
        entry_nombre.set(seleccion)  # Establecer el nombre en el Entry
        lista_sugerencias.place_forget()  # Ocultar la lista de sugerencias


    def eliminar_producto(row_index):
        """
        Función para eliminar un producto de la lista de compra.
        """
        global total_compra
        # Obtener el producto a eliminar
        producto = productos_compra.pop(row_index)


        # Restar el monto del producto al total
        total_compra -= producto[3]
        total_label.config(text=f"Total: ${total_compra:.2f}")


        # Eliminar el producto del frame
        for widget in frame_compra.grid_slaves():
            if int(widget.grid_info()["row"]) == row_index + 1:
                widget.grid_forget()


        # Reorganizar los productos restantes
        for idx, (producto_id, cantidad, precio_unitario, monto_producto) in enumerate(productos_compra):
            tk.Label(frame_compra, text=producto_id, font=("Arial", 10), bg="white").grid(row=idx + 1, column=0, padx=10, pady=5)
            tk.Label(frame_compra, text=str(cantidad), font=("Arial", 10), bg="white").grid(row=idx + 1, column=1, padx=10, pady=5)
            tk.Label(frame_compra, text=f"${precio_unitario:.2f}", font=("Arial", 10), bg="white").grid(row=idx + 1, column=2, padx=10, pady=5)
            tk.Label(frame_compra, text=f"${monto_producto:.2f}", font=("Arial", 10), bg="white").grid(row=idx + 1, column=3, padx=10, pady=5)
            tk.Button(frame_compra, text="X", font=("Arial", 10), fg="red", command=lambda idx=idx: eliminar_producto(idx)).grid(row=idx + 1, column=4, padx=10, pady=5)


    ##### FUNCION PARA AGREGAR PRODUCTO A LA COMPRA


    def agregar_producto():
        db = sqlite3.connect("database.db")
        c = db.cursor()


        nombre_producto = entry_nombre.get()
        cantidad = int(entry_cantidad.get())


        # Buscar el producto por nombre
        c.execute("SELECT id, nombre, precio, cantidad FROM productos WHERE nombre = ?", (nombre_producto,))
        resultado = c.fetchone()
        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado")
            db.close()
            return


        # Asignar resultados a variables separadas
        producto_id, nombre_producto, precio_unitario, cantidad_disponible = resultado


        # Verificar si la cantidad solicitada es mayor a la disponible
        if cantidad > cantidad_disponible:
            messagebox.showerror("Error", "Cantidad solicitada excede la cantidad disponible")
            db.close()
            return


        # Calcular el monto total del producto
        monto_producto = cantidad * precio_unitario


        # Añadir producto a la lista de compra
        productos_compra.append((producto_id, cantidad, precio_unitario, monto_producto))


        # Calcular el número de filas actuales en el frame de compra
        row_count = len(productos_compra)


        # Insertar los detalles del producto en el frame usando grid
        tk.Label(frame_compra, text=nombre_producto, font=("Arial", 10), bg="white").grid(row=row_count, column=0, padx=10, pady=5)
        tk.Label(frame_compra, text=str(cantidad), font=("Arial", 10), bg="white").grid(row=row_count, column=1, padx=10, pady=5)
        tk.Label(frame_compra, text=f"${precio_unitario:.2f}", font=("Arial", 10), bg="white").grid(row=row_count, column=2, padx=10, pady=5)
        tk.Label(frame_compra, text=f"${monto_producto:.2f}", font=("Arial", 10), bg="white").grid(row=row_count, column=3, padx=10, pady=5)
        tk.Button(frame_compra, text="X", font=("Arial", 10), fg="red", command=lambda idx=row_count-1: eliminar_producto(idx)).grid(row=row_count, column=4, padx=10, pady=5)


        # Actualizar el total de la compra
        global total_compra
        total_compra += monto_producto
        total_label.config(text=f"Total: ${total_compra:.2f}")


        db.close()


    def confirmar_compra():
        db = sqlite3.connect("database.db")
        c = db.cursor()


        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime("%d/%m/%y")
        hora_actual = datetime.now().strftime("%H:%M:%S")


        # Insertar una nueva venta en la tabla historial_ventas
        c.execute("INSERT INTO historial_ventas (fecha, hora, total) VALUES (?, ?, ?)", (fecha_actual, hora_actual, total_compra))
        id_venta = c.lastrowid  # Obtener el ID de la venta recién insertada


        # Insertar cada producto en la tabla detalle_venta
        for producto_id, cantidad, precio_unitario, monto_producto in productos_compra:
            c.execute("INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_un, total) VALUES (?, ?, ?, ?, ?)",
                    (id_venta, producto_id, cantidad, precio_unitario, monto_producto))


            # Actualizar la cantidad disponible del producto en la tabla productos
            c.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?", (cantidad, producto_id))


        # Confirmar los cambios y cerrar la base de datos
        db.commit()
        db.close()


        # Limpiar la lista de productos y el total de la compra
        productos_compra.clear()
        total_label.config(text="Total: $0.00")
        for widget in frame_compra.winfo_children():
            widget.grid_forget()


        messagebox.showinfo("Compra confirmada", "La compra ha sido registrada exitosamente.")


    # Botón para agregar productos
    tk.Button(window, text="Agregar producto", fg="blue", font=("arial", 12), borderwidth=5, cursor = "hand2",relief = "raised", command=agregar_producto).place(x=50, y=270)


    # Botón para confirmar la compra
    tk.Button(window, text="CONFIRMAR COMPRA", fg="blue", font=("arial", 12), borderwidth=5, cursor = "hand2",relief = "raised", command=confirmar_compra).place(x=915, y=620)


    tk.Button(window, text="Volver", fg="red", font=("arial", 12), borderwidth=5, cursor = "hand2",relief = "raised", command= window.destroy).place(x=50, y=620)
    
    # Evento de teclado para actualizar las sugerencias cuando se escribe en el Entry
    entry_widget.bind("<KeyRelease>", actualizar_sugerencias)


    # Evento para seleccionar el producto cuando se presiona una tecla en la Listbox
    lista_sugerencias.bind("<Return>", seleccionar_sugerencia)