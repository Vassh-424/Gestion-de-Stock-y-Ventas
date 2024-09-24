import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import backend

###############VENTANA PRINCIPAL#################

def ventana_principal():
    principal = tk.Tk()
    principal.state("zoomed")
    principal.title("Gestion de Stock y Ventas")
    principal.resizable(0, 0)

    titulo= tk.Label(text="GESTION DE STOCK Y VENTAS",padx=10, font=("Arial", 40, "bold"))
    titulo.pack()
    titulo.place(x=60,y=50)


    img= tk.PhotoImage(file="D:\Mis Documentos\Documentos\Programacion 4\ProyectoF\currents.png")
    label= tk.Label(image=img)
    label.pack()
    label.place(x=500,y=200)

    stockb=tk.Button(principal,text="Stock y Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_stock())
    stockb.pack()
    stockb.place(x=1100,y=150)

    ventasb=tk.Button(principal,text="Nueva Venta", fg="blue", font=("arial", 30), state= "normal", borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_crear_compra())
    ventasb.pack()
    ventasb.place(x=1100,y=350)

    detalle_ventasb= tk.Button(principal, text="Historial de Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command= lambda:ventana_historial())
    detalle_ventasb.pack()
    detalle_ventasb.place(x=1100,y=550)

    salir=tk.Button(principal,text="Salir", fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:cerrar_programa())
    salir.pack()
    salir.place(x=1100,y=700)

    ###########CERRAR PROGRAMA##############
    def cerrar_programa():
        principal.destroy()  # O también puedes usar windows.quit(

    ###########STOCK##############
    def ventana_stock():
        stock = tk.Tk()
        stock.state("zoomed")
        stock.title("Gestion de Stock")
        stock.resizable(0, 0)

        marcos = tk.Frame(stock)
        marcos.grid(row=0, column=0, padx=20, pady=20)  # Ajustar el marco
        marcos.config(width=1500, height=800)

        agregar = tk.Button(marcos, text="AGREGAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised", command= lambda:ventana_agregar())
        agregar.grid(row=0, column=0, padx=10, pady=20, sticky="w")

        buscar = tk.Button(marcos, text="BUSCAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised", command= lambda:ventana_ver())
        buscar.grid(row=2, column=0, padx=10, pady=20, sticky="w")  # Ajuste del padding

        modificar = tk.Button(marcos, text="MODIFICAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised", command= lambda:modificar_producto())
        modificar.grid(row=3, column=0, padx=10, pady=40, sticky="w")  # Espacio adicional

        eliminar = tk.Button(marcos, text="ELIMINAR PRODUCTO", fg="blue", font=("arial", 15), cursor="hand2", relief="raised", command= lambda:ventana_eliminar())
        eliminar.grid(row=4, column=0, padx=10, pady=20, sticky="w")

        ########AGREGAR PRODUCTO############

        def ventana_agregar():
            window = tk.Toplevel()
            window.state("zoomed")
            window.title("Agregar Productos")
            window.resizable(0, 0)

            # Etiqueta de título
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
            tk.Label(window, text="INGRESE EL NOMBRE DEL PRODUCTO.", padx=10).place(x=30, y=115)
            tk.Label(window, text="INGRESE LA CANTIDAD DEL PRODUCTO", padx=10).place(x=30, y=200)
            tk.Label(window, text="INGRESE EL PRECIO DEL PRODUCTO", padx=10).place(x=30, y=280)

            # Botón GUARDAR
            guardarb = tk.Button(window, text="GUARDAR", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=lambda:guarda())
            guardarb.place(x=40, y=350)

            # Botón para regresar al MENU
            menu = tk.Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
            menu.place(x=50, y=450)

            #### FUNCION PARA AGREGAR LOS PRODUCTOS
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
                backend.agregar_producto(nombre, precio, cantidad)
                messagebox.showinfo("MODIFICACION", "ARTICULO INGRESADO")
                window.destroy()
                ventana_agregar()  # Reabrir la ventana de agregar para continuar ingresando productos

        def ventana_ver():
            window = tk.Toplevel()
            window.state("zoomed")

            # Crear un Frame principal para organizar los widgets con grid
            frame = tk.Frame(window, bg="white")
            frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            # Frame para los productos
            productos_frame = tk.Frame(frame, bg="white")
            productos_frame.grid(row=1, column=0, columnspan=4, padx=50, pady=20, sticky="nsew")

            # Hacer que la columna y fila del frame principal se expandan
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            # Conectar a la base de datos
            try:
                db = sqlite3.connect("database.db")
                c = db.cursor()

                # Consulta para obtener los datos de los productos
                c.execute('SELECT nombre, precio, cantidad FROM productos ORDER BY id DESC')

                # Obtener todos los datos y verificar que hay resultados
                productos = c.fetchall()
                print("Productos encontrados:", productos)  # Imprimir los productos para depuración

                if productos:
                    # Encabezados en el frame para que estén alineados con los datos
                    tk.Label(productos_frame, text="NOMBRE", bg="lightgray", width=30, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
                    tk.Label(productos_frame, text="PRECIO", bg="lightgray", width=15, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
                    tk.Label(productos_frame, text="CANTIDAD", bg="lightgray", width=10, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

                    # Mostrar los productos
                    for i, row in enumerate(productos):
                        nombre_producto = row[0]
                        precio_producto = row[1]
                        cantidad_producto = row[2]

                        # Color de fondo en la fila si la cantidad es menor a 10
                        color_fondo = "lightcoral" if cantidad_producto < 10 else "white"

                        tk.Label(productos_frame, text=nombre_producto, bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=0, padx=10, pady=5, sticky="nsew")
                        tk.Label(productos_frame, text=f"${precio_producto:.2f}", bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=1, padx=10, pady=5, sticky="nsew")
                        tk.Label(productos_frame, text=f"{cantidad_producto}", bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=2, padx=10, pady=5, sticky="nsew")

                    # Configuración de las columnas para que se expandan equitativamente
                    productos_frame.grid_columnconfigure(0, weight=1)
                    productos_frame.grid_columnconfigure(1, weight=1)
                    productos_frame.grid_columnconfigure(2, weight=1)

                else:
                    tk.Label(productos_frame, text="No se encontraron productos.", bg="white").grid(row=1, column=0, columnspan=3, padx=10, pady=10)

            except sqlite3.Error as e:
                print(f"Error al conectar con la base de datos: {e}")
                tk.Label(productos_frame, text="Error al conectar con la base de datos.", bg="white").grid(row=1, column=0, columnspan=3, padx=10, pady=10)

            finally:
                # Cerrar la conexión y el cursor
                if c:
                    c.close()
                if db:
                    db.close()

            # Botón de menú al final del grid
            menu = tk.Button(frame, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
            menu.grid(row=2, column=0, columnspan=4, pady=10)








        ########MODIFICAR PRODUCTO############

        def modificar_producto(): ##Modificar de manera que se pueda buscar un producto y de ahi modificar su nombre y/o precio
            window = tk.Toplevel()
            window.state("zoomed")
            window.title("Modificar producto")
            window.resizable(0,0)

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
                db = sqlite3.connect("database.db")
                c = db.cursor()

                id_producto = entry_id.get()
                nuevo_precio = entry_valor.get()
            
                c.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto))
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




        ########ELIMINAR PRODUCTO##########
        def ventana_eliminar(): ##Modificar de manera en que sea mas facil encontrar y eliminar un producto
            window = tk.Toplevel()
            window.state("zoomed")
            window.title("ELIMINAR PRODUCTOS")
            window.resizable(0,0)
            e1 = tk.Label(window, text=" ELIMINAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)
            
            # Variable para ID
            entry_id = tk.StringVar()
            productotx = tk.Entry(window, textvariable=entry_id).place(x=50, y=150)

            # Etiqueta para ID
            etiquetanombre = tk.Label(window, text="INGRESE CODIGO DEL PRODUCTO", padx=10).place(x=30, y=115)

            ##### FUNCION PARA ELIMINAR EL PRODUCTO
            def eliminar():
                db = sqlite3.connect("database.db")
                c = db.cursor()

                id_producto = entry_id.get()
            
                c.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
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


    ###########HISTORIAL DE VENTAS##############

    def ventana_historial():
        def validar_dia(event):
            try:
                dia = int(dia_entry.get())
                if dia < 1 or dia > max_dias():
                    dia_entry.delete(0, tk.END)
            except ValueError:
                pass  # Ignore if it's not a number yet

        def validar_mes(event):
            try:
                mes = int(mes_entry.get())
                if mes < 1 or mes > 12:
                    mes_entry.delete(0, tk.END)
            except ValueError:
                pass

        def max_dias():
            mes = mes_entry.get()
            if mes in ['4', '6', '9', '11']:  # Meses con 30 días
                return 30
            elif mes == '2':  # Febrero con 28 días
                return 28
            else:
                return 31  # El resto de meses con 31 días

        def buscar_por_fecha():
            dia = dia_entry.get()
            mes = mes_entry.get()
            anio = anio_entry.get()

            # Formar la query basándonos en los valores proporcionados
            query = "SELECT id, detalle, fecha, hora, total FROM historial_ventas WHERE 1=1"
            if dia:
                query += f" AND SUBSTR(fecha, 1, 2) = '{dia.zfill(2)}'"
            if mes:
                query += f" AND SUBSTR(fecha, 4, 2) = '{mes.zfill(2)}'"
            if anio:
                query += f" AND SUBSTR(fecha, 7, 2) = '{anio.zfill(2)}'"
            
            mostrar_ventas(query)

        def mostrar_ventas(query=None):
            for widget in details_frame.winfo_children():
                widget.destroy()

            try:
                db = sqlite3.connect("database.db")
                c = db.cursor()

                if query is None:
                    query = "SELECT id, detalle, fecha, hora, total FROM historial_ventas ORDER BY fecha DESC, hora DESC"
                
                c.execute(query)
                ventas = c.fetchall()

                if ventas:
                    row_num = 1
                    for venta in ventas:
                        detalle, fecha, hora, total = venta[1], venta[2], venta[3], venta[4]

                        productos = detalle.split('\n')

                        for idx, producto in enumerate(productos):
                            if idx == 0:
                                tk.Label(details_frame, text=f"{producto}", bg="white", anchor="w", borderwidth=1, relief="solid", width=100, padx=5).grid(row=row_num, column=0, padx=5, pady=5, sticky="w")
                                tk.Label(details_frame, text=f"{fecha}", bg="white", anchor="w", borderwidth=1, relief="solid", width=20).grid(row=row_num, column=1, padx=5, pady=5)
                                tk.Label(details_frame, text=f"{hora}", bg="white", anchor="w", borderwidth=1, relief="solid", width=15).grid(row=row_num, column=2, padx=5, pady=5)
                                tk.Label(details_frame, text=f"${total:.2f}", bg="white", anchor="w", borderwidth=1, relief="solid", width=15).grid(row=row_num, column=3, padx=5, pady=5)
                            else:
                                tk.Label(details_frame, text=f"{producto}", bg="white", anchor="w", borderwidth=1, relief="solid", width=100, padx=5).grid(row=row_num, column=0, padx=5, pady=5, sticky="w")

                            row_num += 1

                        tk.Label(details_frame, text="", bg="white").grid(row=row_num, column=0, columnspan=4, padx=5, pady=5)
                        row_num += 1
                else:
                    tk.Label(details_frame, text="No se encontraron ventas.", bg="white").grid(row=1, column=0, columnspan=4, padx=5, pady=5)

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
            finally:
                if c:
                    c.close()
                if db:
                    db.close()

        historial = tk.Toplevel()
        historial.state("zoomed")
        historial.title("Historial de Ventas")
        historial.resizable(0, 0)

        tk.Label(historial, text="VENTAS REALIZADAS :", bg="white", fg="black", font=("Arial", 14)).place(x=50, y=50)

        # Campos de búsqueda por día, mes, año
        tk.Label(historial, text="Día:", font=("Arial", 12)).place(x=500, y=50)
        dia_entry = tk.Entry(historial, font=("Arial", 12), width=5)
        dia_entry.place(x=550, y=50)
        dia_entry.bind('<KeyRelease>', validar_dia)

        tk.Label(historial, text="Mes:", font=("Arial", 12)).place(x=600, y=50)
        mes_entry = tk.Entry(historial, font=("Arial", 12), width=5)
        mes_entry.place(x=650, y=50)
        mes_entry.bind('<KeyRelease>', validar_mes)

        tk.Label(historial, text="Año:", font=("Arial", 12)).place(x=700, y=50)
        anio_entry = tk.Entry(historial, font=("Arial", 12), width=5)
        anio_entry.place(x=850, y=50)

        # Botón para buscar
        buscar_button = tk.Button(historial, text="Buscar", command=buscar_por_fecha)
        buscar_button.place(x=900, y=50)

        main_frame = tk.Frame(historial, bg="white")
        main_frame.place(x=50, y=100, width=1500, height=600)

        # Encabezados de las columnas
        tk.Label(main_frame, text="DETALLE", bg="lightgray", width=100, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(main_frame, text="FECHA", bg="lightgray", width=20, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(main_frame, text="HORA", bg="lightgray", width=15, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(main_frame, text="TOTAL", bg="lightgray", width=15, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=3, padx=5, pady=5)

        details_frame = tk.Frame(main_frame, bg="white")
        details_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        menu_button = tk.Button(historial, fg= "red", text="Volver", font= ("arial", 16),command= historial.destroy)
        menu_button.place(x=40, y=800)

        mostrar_ventas()



    ###########NUEVA VENTA##############
    def ventana_crear_compra():
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
        frame_carrito.place(x=300, y=100, width=600, height=350)

        # Crear el frame donde se mostrarán los productos de la compra
        frame_compra = tk.Frame(frame_carrito, bg="white")
        frame_compra.place(x=0, y=0, width=600, height=350)

        # Etiquetas de encabezado para las columnas
        tk.Label(frame_compra, text="Nombre", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame_compra, text="Cantidad", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame_compra, text="Precio Unitario", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=2, padx=10, pady=5)
        tk.Label(frame_compra, text="Total", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=3, padx=10, pady=5)

        # Variable para el total de la compra
        total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 14))
        total_label.place(x=300, y=500)

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

        # Asociar eventos de entrada con la función de actualización de sugerencias
        entry_widget.bind("<KeyRelease>", actualizar_sugerencias)
        lista_sugerencias.bind("<ButtonRelease-1>", seleccionar_sugerencia)

        bt_agregar_producto = tk.Button(window, text="AÑADIR A LA COMPRA", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=agregar_producto)
        bt_agregar_producto.pack()
        bt_agregar_producto.place(x=50, y=300)

        def realizar_venta():
            if not productos_compra:
                messagebox.showerror("Error", "No hay productos en la compra")
                return

            db = sqlite3.connect("database.db")
            c = db.cursor()

            # Asegurarse de que el formato de la fecha sea dd/mm/yy
            fecha_actual = datetime.now().strftime("%d/%m/%y")
            hora_actual = datetime.now().strftime("%H:%M:%S")

            # Lista para almacenar el detalle de la venta
            detalle_venta = []

            # Registrar cada producto en la tabla 'carrito' y obtener el nombre desde la tabla 'productos'
            for id_producto, cantidad, precio_unitario, monto_producto in productos_compra:
                # Obtener el nombre del producto usando el ID del producto
                c.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
                nombre_producto = c.fetchone()[0]  # Obtenemos el nombre

                # Registrar el producto en la tabla 'carrito' con su nombre, cantidad, precio y total
                c.execute("INSERT INTO carrito (nombre_prod, cantidad, precio_un, total) VALUES (?, ?, ?, ?)",
                        (nombre_producto, cantidad, precio_unitario, monto_producto))

                # Actualizar la cantidad del producto en 'productos'
                c.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?", (cantidad, id_producto))

                # Formatear la información del producto para el detalle de la venta
                detalle_venta.append(f"{nombre_producto} (Cantidad: {cantidad}, Precio: ${precio_unitario:.2f})")

            # Convertir la lista de productos en un string para el campo 'detalle' de la tabla 'historial_ventas'
            detalle_venta_str = "; ".join(detalle_venta)

            # Registrar la venta en la tabla 'historial_ventas' con la fecha en formato dd/mm/yy
            c.execute("INSERT INTO historial_ventas (detalle, fecha, hora, total) VALUES (?, ?, ?, ?)",
                    (detalle_venta_str, fecha_actual, hora_actual, total_compra))

            # Vaciar la tabla 'carrito' después de registrar la venta
            c.execute("DELETE FROM carrito")

            db.commit()
            db.close()

            messagebox.showinfo("VENTA REALIZADA", f"Venta realizada por un monto total de ${total_compra:.2f}")

            # Reiniciar el estado de la ventana
            productos_compra.clear()  # Vaciar la lista de productos en la compra actual
            window.destroy()  # Cerrar la ventana de compra
                # Botón para realizar la venta
        bt_vender = tk.Button(window, text="REALIZAR VENTA", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=realizar_venta)
        bt_vender.pack()
        bt_vender.place(x=300, y=550)

        # Botón para volver al menú
        menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
        menu.pack()
        menu.place(x=50, y=550)




#########FIN DE PRORGAMA PRINCIPAL#################
    principal.mainloop()



""" 
LISTA DE COSAS POR TERMINAR
- Terminar ventana de stock y sus funciones
--- Modificar la ventana modificar, buscar y eliminar para que los productos se puedan buscar por nombre
-Modificar la ventana de historial de ventas para que las ventas se puedan ver y buscar por fecha
-Opcional: Agregar calculadora para que se pueda calcular el vuelto a dar despues de una compra
"""
    
if __name__ == '__main__':
    ventana_principal()
