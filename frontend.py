import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime

###############VENTANA PRINCIPAL#################

def ventana_principal():
    principal = tk.Tk()
    principal.geometry("1600x900")
    principal.title("Gestion de Stock y Ventas")
    principal.resizable(0, 0)

    titulo= tk.Label(text="GESTION DE STOCK Y VENTAS",padx=10, font=("Arial", 30))
    titulo.pack()
    titulo.place(x=470,y=50)


    img= tk.PhotoImage(file="D:\Mis Documentos\Documentos\Programacion 4\ProyectoF\currents.png")
    label= tk.Label(image=img)
    label.pack()
    label.place(x=500,y=200)

    stockb=tk.Button(principal,text="Stock y Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_stock())
    stockb.pack()
    stockb.place(x=150,y=650)

    ventasb=tk.Button(principal,text="Nueva Venta", fg="blue", font=("arial", 30), state= "normal", borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_ventas())
    ventasb.pack()
    ventasb.place(x=660,y=650)

    detalle_ventasb= tk.Button(principal, text="Historial de Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command= lambda:ventana_historial())
    detalle_ventasb.pack()
    detalle_ventasb.place(x=1100,y=650)

    salir=tk.Button(principal,text="Salir", fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:cerrar_programa())
    salir.pack()
    salir.place(x=770,y=750)

    ###########CERRAR PROGRAMA##############
    def cerrar_programa():
        principal.destroy()  # O también puedes usar windows.quit(

    ###########STOCK##############
    def ventana_stock():
        stock = tk.Tk()
        stock.geometry("1600x900")
        stock.title("Gestion de Stock")
        stock.resizable(0, 0)

        marcos = tk.Frame(stock)
        marcos.grid(row=0, column=0, padx=20, pady=20)  # Ajustar el marco
        marcos.config(width=1500, height=800)

        buscar = tk.Button(marcos, text="BUSCAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised")
        buscar.grid(row=0, column=0, padx=10, pady=20, sticky="w")  # Ajuste del padding

        modificar = tk.Button(marcos, text="MODIFICAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised")
        modificar.grid(row=1, column=0, padx=10, pady=40, sticky="w")  # Espacio adicional

        eliminar = tk.Button(marcos, text="ELIMINAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised")
        eliminar.grid(row=2, column=0, padx=10, pady=20, sticky="w")




        






    ###########HISTORIAL DE VENTAS##############

    def ventana_historial():
        historial = tk.Tk()
        historial.geometry("1600x900")
        historial.title("Historial de Ventas")
        historial.resizable(0, 0)



    ###########NUEVA VENTA##############
    def ventana_ventas():
        ventas = tk.Toplevel()
        ventas.geometry("1600x900")
        ventas.title("Nueva Venta")
        ventas.resizable(0, 0)

        # Crear un frame para contener todos los widgets
        frame = tk.Frame(ventas)
        frame.place(x=0, y=0, width=1000, height=650)
        frame.grid(rowspan=7, columnspan=7)  # Aumentar el alto del frame

        tk.Label(frame, text="NUEVA VENTA :", bg="white", fg="black", font=("Arial", 20)).grid(row=0, column=0, padx=50, pady=20, sticky="w")

        # Variable para el nombre del producto
        entry_nombre = tk.StringVar()
        tk.Entry(frame, textvariable=entry_nombre, font=("Arial", 16)).grid(row=2, column=0, padx=50, pady=10, sticky="w")

        # Etiqueta para el nombre del producto
        tk.Label(frame, text="INGRESE NOMBRE DEL PRODUCTO", padx=10, font=("Arial", 16)).grid(row=1, column=0, padx=30, pady=5, sticky="w")

        # Variable para cantidad
        entry_cantidad = tk.StringVar()
        tk.Entry(frame, textvariable=entry_cantidad, font=("Arial", 16)).grid(row=4, column=0, padx=50, pady=10, sticky="w")

        # Etiqueta para cantidad
        tk.Label(frame, text="CANTIDAD", padx=10, font=("Arial", 16)).grid(row=3, column=0, padx=30, pady=5, sticky="w")

        # Lista para los productos de la compra
        lista_compra = tk.Listbox(frame, width=100, height=25, font=("Arial", 14))  # Ajustar altura
        lista_compra.grid(row=1, column=1, rowspan=5, padx=20, pady=20, sticky="n")

        # Etiqueta para el total de la compra
        total_label = tk.Label(frame, text="Total: $0.00", font=("Arial", 16))
        total_label.grid(row=6, column=1, padx=20, pady=(10, 20), sticky="w")

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

            nombre_producto = entry_nombre.get()
            cantidad = int(entry_cantidad.get())

            # Obtener el precio unitario y cantidad disponible del producto por nombre
            c.execute("SELECT nombre, precio, cantidad FROM articulos WHERE nombre = ?", (nombre_producto,))
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
            productos_compra.append((nombre_producto, cantidad, precio_unitario))
            lista_compra.insert(tk.END, f"{nombre_producto} - Cantidad: {cantidad} - Precio: ${monto_producto:.2f}")

            # Actualizar el total de la compra
            global total_compra
            total_compra += monto_producto
            total_label.config(text=f"Total: ${total_compra:.2f}")

            db.close()

        bt_agregar_producto = tk.Button(frame, text="AÑADIR A LA COMPRA", fg="blue", font=("Arial", 16), cursor="hand2", relief="raised", command=agregar_producto)
        bt_agregar_producto.grid(row=5, column=0, padx=50, pady=10, sticky="w")

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
            for nombre_producto, cantidad, precio_unitario in productos_compra:
                # Obtener el código del producto para registrar en el detalle de venta
                c.execute("SELECT codigo FROM articulos WHERE nombre = ?", (nombre_producto,))
                codigo_producto = c.fetchone()[0]
                
                c.execute("INSERT INTO ventas_detalle (venta_id, codigo_producto, cantidad) VALUES (?, ?, ?)",
                        (id_venta, codigo_producto, cantidad))
                c.execute("UPDATE articulos SET cantidad = cantidad - ? WHERE codigo = ?", (cantidad, codigo_producto))

            db.commit()
            db.close()

            messagebox.showinfo("VENTA REALIZADA", f"Venta realizada por un monto total de ${total_compra:.2f}")
            ventas.destroy()

        # Botón para realizar la venta
        bt_vender = tk.Button(frame, text="REALIZAR VENTA", fg="blue", font=("Arial", 16), cursor="hand2", relief="raised", command=realizar_venta)
        bt_vender.grid(row=6, column=0, padx=50, pady=20, sticky="w")

            # Botón para gestión de stock a la derecha
        volver= tk.Button(ventas, text="Volver", fg="red", font=("Arial", 12), cursor="hand2", relief="raised")
        volver.grid(row=7,column=0)

    #########FIN DE PRORGAMA PRINCIPAL#################
    principal.mainloop()



""" 
LISTA DE COSAS POR TERMINAR
- Conectar con la base de datos
- Modificar la ventana de historial de ventas para que las ventas se puedan ver y buscar por fecha
- Terminar ventana de stock y sus funciones
"""
    
if __name__ == '__main__':
    ventana_principal()
