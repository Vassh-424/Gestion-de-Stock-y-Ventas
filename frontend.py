import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import backend


###############VENTANA PRINCIPAL#################


def ventana_principal():
    principal = tk.Tk()
    principal.state("zoomed")
    principal.title("Gestion de Stock y Ventas")
    principal.resizable(0, 0)


    titulo= tk.Label(text="GESTION DE STOCK Y VENTAS V1",padx=10, font=("Arial", 40, "bold"))
    titulo.pack()
    titulo.place(x=60,y=50)


    stockb=tk.Button(principal,text="Stock", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised",  command = lambda:ventana_stock())
    stockb.pack()
    stockb.place(x=900,y=150)


    ventasb=tk.Button(principal,text="Nueva Venta", fg="blue", font=("arial", 30), state= "normal", borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_crear_compra())
    ventasb.pack()
    ventasb.place(x=900,y=300)


    detalle_ventasb= tk.Button(principal, text="Historial de Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command= lambda:ventana_historial())
    detalle_ventasb.pack()
    detalle_ventasb.place(x=900,y=450)
    
    btn_manual = tk.Button(principal, text="Manual",  fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:manual())
    btn_manual.pack()
    btn_manual.place(x=1000,y=620)


    salir=tk.Button(principal,text="Salir", fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:cerrar_programa())
    salir.pack()
    salir.place(x=900,y=620)


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


        agregar = tk.Button(marcos, text="AGREGAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_agregar())
        agregar.grid(row=0, column=0, padx=10, pady=20, sticky="w")


        buscar = tk.Button(marcos, text="BUSCAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_ver())
        buscar.grid(row=2, column=0, padx=10, pady=20, sticky="w")  # Ajuste del padding


        modificar = tk.Button(marcos, text="MODIFICAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:modificar_producto())
        modificar.grid(row=3, column=0, padx=10, pady=40, sticky="w")  # Espacio adicional


        eliminar = tk.Button(marcos, text="ELIMINAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_eliminar())
        eliminar.grid(row=4, column=0, padx=10, pady=20, sticky="w")


        menu = tk.Button(marcos, text="Volver", fg="red", font=("arial", 20), cursor="hand2", relief="raised", command=stock.destroy)
        menu.grid(row=5, column=0, padx=10, pady=20, sticky="w")




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
            menu = tk.Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=lambda:[ventana_stock(),window.destroy])
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

        #############BUSCAR PRODUCTO#############

        def ventana_ver():
            def filtrar_productos(event=None):
                """Filtrar productos según el texto ingresado en la barra de búsqueda."""
                filtro = entry_busqueda.get().strip().lower()
                for widget in productos_frame.winfo_children():
                    widget.destroy()  # Limpiar los productos antes de mostrar los filtrados

                mostrar_productos(filtro)

            def mostrar_productos(filtro=""):
                """Mostrar los productos en el frame, aplicando el filtro si es necesario."""
                try:
                    db = sqlite3.connect("database.db")
                    c = db.cursor()
                    consulta = 'SELECT nombre, precio, cantidad FROM productos WHERE nombre LIKE ? ORDER BY id DESC'
                    c.execute(consulta, (f"%{filtro}%",))
                    productos = c.fetchall()

                    if productos:
                        # Encabezados
                        tk.Label(productos_frame, text="NOMBRE", bg="lightgray", width=30, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
                        tk.Label(productos_frame, text="PRECIO", bg="lightgray", width=15, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
                        tk.Label(productos_frame, text="CANTIDAD", bg="lightgray", width=10, anchor="w", borderwidth=1, relief="solid").grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

                        # Mostrar los productos
                        for i, (nombre, precio, cantidad) in enumerate(productos):
                            color_fondo = "lightcoral" if cantidad < 10 else "white"
                            tk.Label(productos_frame, text=nombre, bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=0, padx=10, pady=5, sticky="nsew")
                            tk.Label(productos_frame, text=f"${precio:.2f}", bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=1, padx=10, pady=5, sticky="nsew")
                            tk.Label(productos_frame, text=cantidad, bg=color_fondo, anchor="w", borderwidth=1, relief="solid").grid(row=i+1, column=2, padx=10, pady=5, sticky="nsew")

                        # Configurar las columnas para que se expandan
                        productos_frame.grid_columnconfigure(0, weight=1)
                        productos_frame.grid_columnconfigure(1, weight=1)
                        productos_frame.grid_columnconfigure(2, weight=1)
                    else:
                        tk.Label(productos_frame, text="No se encontraron productos.", bg="white").grid(row=1, column=0, columnspan=3, padx=10, pady=10)

                except sqlite3.Error as e:
                    print(f"Error al conectar con la base de datos: {e}")
                    tk.Label(productos_frame, text="Error al conectar con la base de datos.", bg="white").grid(row=1, column=0, columnspan=3, padx=10, pady=10)
                finally:
                    if c:
                        c.close()
                    if db:
                        db.close()

            # Ventana principal
            window = tk.Toplevel()
            window.state("zoomed")
            window.title("Busqueda(Modificar)")

            # Frame principal
            frame = tk.Frame(window, bg="white")
            frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            # Barra de búsqueda
            entry_busqueda = tk.Entry(frame, font=("Arial", 14))
            entry_busqueda.grid(row=0, column=0, columnspan=4, padx=40, pady=10, sticky="nsew")
            entry_busqueda.bind("<KeyRelease>", filtrar_productos)  # Evento para búsqueda en tiempo real

            # Frame para los productos
            productos_frame = tk.Frame(frame, bg="white")
            productos_frame.grid(row=1, column=0, columnspan=4, padx=50, pady=20, sticky="nsew")

            # Configuración de expansión
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            # Botón de menú
            menu = tk.Button(frame, text="MENU", fg="red", font=("Arial", 12), cursor="hand2", relief="raised", command=lambda:[ventana_stock(),window.destroy])
            menu.grid(row=2, column=0, columnspan=4, pady=10)

            # Mostrar los productos al iniciar
            mostrar_productos()











        ########MODIFICAR PRODUCTO############


        def modificar_producto():
            window = tk.Toplevel()
            window.state("zoomed")
            window.title("Modificar producto")
            window.resizable(0, 0)


            e1 = tk.Label(window, text=" MODIFICAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)


            # Variable para el nombre del producto
            entry_nombre = tk.StringVar()
            entry_widget = tk.Entry(window, textvariable=entry_nombre)
            entry_widget.place(x=50, y=150)


            # Etiqueta para el nombre del producto
            etiquetanombre = tk.Label(window, text="Nombre del producto :",font=("Arial",12), padx=10).place(x=30, y=100)


            # Listbox para autocompletar
            lista_sugerencias = tk.Listbox(window, width=30, height=5, font=("Arial", 10))
            lista_sugerencias.place(x=50, y=180)  # Colocar justo debajo del Entry
            lista_sugerencias.place_forget()  # Ocultarla inicialmente


            # Frame para los inputs de modi5ficar producto (oculto inicialmente)
            frame_modificar = tk.Frame(window)
            frame_modificar.place(x=400, y=100)
            frame_modificar.place_forget()


            # Variables para los nuevos valores
            entry_nuevo_nombre = tk.StringVar()
            entry_nueva_cantidad = tk.StringVar()
            entry_nuevo_precio = tk.StringVar()


            # Etiquetas e Inputs en el frame
            tk.Label(frame_modificar, text="Nuevo Nombre:", padx=10, font=("Arial",12)).grid(row=0, column=0, pady=5)
            tk.Entry(frame_modificar, textvariable=entry_nuevo_nombre).grid(row=0, column=1, pady=5)


            tk.Label(frame_modificar, text="Nueva Cantidad:", padx=10).grid(row=1, column=0, pady=5)
            tk.Entry(frame_modificar, textvariable=entry_nueva_cantidad).grid(row=1, column=1, pady=5)


            tk.Label(frame_modificar, text="Nuevo Precio:", padx=10).grid(row=2, column=0, pady=5)
            tk.Entry(frame_modificar, textvariable=entry_nuevo_precio).grid(row=2, column=1, pady=5)


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
                frame_modificar.place(x=400, y=100)  # Mostrar el frame para modificar producto


            # Ocultar el frame y resetear inputs cuando se vuelve a hacer clic en el campo de búsqueda o se presiona el botón cancelar
            def ocultar_modificar(event=None):
                frame_modificar.place_forget()
                entry_nuevo_nombre.set("")
                entry_nueva_cantidad.set("")
                entry_nuevo_precio.set("")


            # Vincular eventos
            lista_sugerencias.bind("<<ListboxSelect>>", seleccionar_sugerencia)
            entry_widget.bind("<Button-1>", ocultar_modificar)
            entry_widget.bind("<KeyRelease>", actualizar_sugerencias)


            def modificar():
                db = sqlite3.connect("database.db")
                c = db.cursor()

                nombre_producto = entry_nombre.get()
                nuevo_nombre = entry_nuevo_nombre.get()
                nueva_cantidad = entry_nueva_cantidad.get()
                nuevo_precio = entry_nuevo_precio.get()
                warning= tk.Label(frame_modificar, text="La cantidad debe ser un numero entero positivo")
                warning.grid(row=2, column=2, pady=5)
                warning.place_forget()

                # Actualizar nombre si no está vacío
                if nuevo_nombre:
                    c.execute("UPDATE productos SET nombre = ? WHERE nombre = ?", (nuevo_nombre, nombre_producto))

                # Verificar si la nueva cantidad es válida, si no da error
                if nueva_cantidad.isdigit():
                    c.execute("SELECT cantidad FROM productos WHERE nombre = ?", (nombre_producto,))
                    cantidad_actual = c.fetchone()[0]  # Obtener la cantidad actual

                    cantidad_final = cantidad_actual + int(nueva_cantidad)  # Sumar la nueva cantidad
                    c.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (cantidad_final, nombre_producto))
                else:
                    messagebox.showwarning("Error", "La cantidad debe ser un número positivo entero.")              
                    return #Corregir. La ventana de error se muestra pero la ventana original se va para atras.

                # Actualizar precio si no está vacío
                if nuevo_precio:
                    c.execute("UPDATE productos SET precio = ? WHERE nombre = ?", (nuevo_precio, nombre_producto))

                db.commit()
                c.close()
                db.close()

                messagebox.showinfo("MODIFICACIÓN", "ARTÍCULO MODIFICADO") # Cerrar la ventana de modificación una vez confirmados los cambios

                modificar_producto()  # Volver a la ventana de modificación




            # Botón para confirmar los cambios
            bt_modificar = tk.Button(frame_modificar, text="CONFIRMAR CAMBIOS", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=modificar)
            bt_modificar.grid(row=3, columnspan=2, pady=10)


            # Botón "Cancelar" para ocultar el frame de modificación
            bt_cancelar = tk.Button(frame_modificar, text="CANCELAR", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=ocultar_modificar)
            bt_cancelar.grid(row=4, columnspan=2, pady=10)


            # Botón para Volver
            menu = tk.Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
            menu.pack()
            menu.place(x=50, y=350)






        ########ELIMINAR PRODUCTO##########
    def ventana_eliminar():
        window = tk.Toplevel()
        window.state("zoomed")
        window.title("ELIMINAR PRODUCTOS")
        window.resizable(0, 0)


        e1 = tk.Label(window, text=" ELIMINAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)


        # Variable para el nombre del producto
        nombre_producto = tk.StringVar()
        entry_widget = tk.Entry(window, textvariable=nombre_producto, font=("Arial", 12), width=30)
        entry_widget.place(x=50, y=150)


        # Etiqueta para el nombre
        etiquetanombre = tk.Label(window, text="Ingrese el nombre del producto a terminar:", font=("Arial", 12), padx=10).place(x=30, y=115)


        # Listbox para autocompletar
        lista_sugerencias = tk.Listbox(window, width=30, height=5, font=("Arial", 10))
        lista_sugerencias.place(x=50, y=180)  # Colocar justo debajo del Entry
        lista_sugerencias.place_forget()  # Ocultarla inicialmente


        def actualizar_sugerencias(event=None):
            """
            Función que busca productos que coincidan con el texto ingresado y actualiza la lista de sugerencias.
            """
            texto_ingresado = nombre_producto.get()
            if not texto_ingresado:
                lista_sugerencias.place_forget()
                return


            # Conectar a la base de datos y buscar coincidencias
            db = sqlite3.connect("database.db")
            c = db.cursor()


            c.execute("SELECT nombre FROM productos WHERE nombre LIKE ?", ('%' + texto_ingresado + '%',))
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
            nombre_producto.set(seleccion)  # Establecer el nombre en el Entry
            lista_sugerencias.place_forget()  # Ocultar la lista de sugerencias


        ##### FUNCION PARA ELIMINAR EL PRODUCTO POR NOMBRE
        def eliminar():
            db = sqlite3.connect("database.db")
            c = db.cursor()


            nombre = nombre_producto.get()


            # Verificar si existe un producto con el nombre ingresado
            c.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
            producto = c.fetchone()


            if producto:
                # Eliminar el producto
                c.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
                db.commit()
                messagebox.showinfo("MODIFICACION", f"Producto '{nombre}' eliminado.")
            else:
                messagebox.showwarning("No encontrado", "No se encontró ningún producto con ese nombre.")


            c.close()
            db.close()
            window.destroy()
            ventana_eliminar()


        # Vincular eventos para autocompletado
        lista_sugerencias.bind("<<ListboxSelect>>", seleccionar_sugerencia)
        entry_widget.bind("<KeyRelease>", actualizar_sugerencias)


        # Botón para volver al menú
        menu = tk.Button(window, text="Cancelar", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=lambda:[ventana_stock(),window.destroy])
        menu.pack()
        menu.place(x=50, y=350)


        # Botón para eliminar productos
        bt_eliminar = tk.Button(window, text="ELIMINAR PRODUCTO", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=eliminar)
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
                pass

        def validar_mes(event):
            try:
                mes = int(mes_entry.get())
                if mes < 1 or mes > 12:
                    mes_entry.delete(0, tk.END)
            except ValueError:
                pass

        def max_dias():
            mes = mes_entry.get()
            if mes in ['4', '6', '9', '11']:
                return 30
            elif mes == '2':
                return 28
            else:
                return 31

        def buscar_por_fecha():
            dia = dia_entry.get()
            mes = mes_entry.get()
            anio = anio_entry.get()

            if not dia and not mes and not anio:
                ventas_frame.place_forget()
                detalles_frame.place_forget()
                return

            query = """
            SELECT id, fecha, hora, total FROM historial_ventas WHERE 1=1
            """
            if dia:
                query += f" AND SUBSTR(fecha, 1, 2) = '{dia.zfill(2)}'"
            if mes:
                query += f" AND SUBSTR(fecha, 4, 2) = '{mes.zfill(2)}'"
            if anio:
                query += f" AND SUBSTR(fecha, 7, 2) = '{anio.zfill(2)}'"
            query += " ORDER BY fecha DESC, hora DESC"  # Ordenar en orden descendente por fecha y hora

            mostrar_ventas(query)

        def mostrar_ventas(query=None):
            for widget in ventas_frame.winfo_children():
                widget.destroy()

            try:
                db = sqlite3.connect("database.db")
                c = db.cursor()

                if query is None:
                    ventas_frame.place_forget()
                    detalles_frame.place_forget()
                    return

                c.execute(query)
                ventas = c.fetchall()
                if ventas:
                    # Mostrar el frame de ventas solo si hay resultados
                    ventas_frame.place(relx=0.5, rely=0.15, anchor="n", width=900, height=210)  # Aumentar la altura
                    ventas_frame.config(borderwidth=1)

                    # Crear un frame para los encabezados
                    header_frame = tk.Frame(ventas_frame, bg="grey")  # Color para encabezados
                    header_frame.place(relx=0.5, rely=0, anchor="n", width=900, height=40)

                    # Encabezados
                    tk.Label(header_frame, text="Venta", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                    tk.Label(header_frame, text="Fecha", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
                    tk.Label(header_frame, text="Total", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
                    tk.Label(header_frame, text="Hora", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

                    # Configurar canvas para las ventas
                    canvas_ventas = tk.Canvas(ventas_frame, bg="white", width=900, height= 300)  # Ajustar la altura a automático
                    canvas_ventas.place(relx=0.5, rely=0.10, anchor="n")

                    # Frame que va dentro del canvas
                    frame_in_canvas_ventas = tk.Frame(canvas_ventas, bg="white", height=300)

                    # Agregar frame al canvas
                    canvas_ventas.create_window((0, 0), window=frame_in_canvas_ventas, anchor="nw")

                    # Agregar contenido de ventas
                    for idx, venta in enumerate(ventas, 1):
                        venta_id, fecha, hora, total = venta  # Asumimos que el total ya se está enviando correctamente

                        tk.Button(frame_in_canvas_ventas, text=f"{idx}", font=("Arial", 12), width=20,
                                command=lambda vid=venta_id: mostrar_detalles(vid)).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
                        tk.Label(frame_in_canvas_ventas, text=fecha, font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                        tk.Label(frame_in_canvas_ventas, text=f"${total:.2f}", font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=2, padx=10, pady=5, sticky="w")
                        tk.Label(frame_in_canvas_ventas, text=hora, font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=3, padx=10, pady=5, sticky="w")

                    # Actualizar scroll region
                    frame_in_canvas_ventas.update_idletasks()

                    # Ajustar la altura del canvas según la cantidad de filas
                    num_filas = len(ventas)
                    altura_fila = 30  # Ajustar este valor si la altura de cada fila cambia
                    canvas_ventas_height = min(num_filas, 5) * altura_fila + 40  # +40 para los encabezados
                    canvas_ventas.config(height=canvas_ventas_height)

                    # Configurar scrollregion
                    canvas_ventas.config(scrollregion=(0, 0, 900, canvas_ventas.bbox("all")[3]))  # Solo ajustar en altura, no en ancho

                    # Habilitar scroll solo si hay más de 5 filas
                    if num_filas > 5:
                        # Vincular el scroll solo cuando el ratón esté sobre el canvas de ventas
                        canvas_ventas.bind("<Enter>", lambda e: canvas_ventas.bind_all("<MouseWheel>", lambda event: canvas_ventas.yview_scroll(int(-1 * (event.delta / 120)), "units")))
                        canvas_ventas.bind("<Leave>", lambda e: canvas_ventas.unbind_all("<MouseWheel>"))
                    else:
                        canvas_ventas.unbind("<MouseWheel>")  # Desactivar scroll si hay 5 o menos filas

                else:
                    ventas_frame.place_forget()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
            finally:
                if c:
                    c.close()
                if db:
                    db.close()

            def mostrar_detalles(venta_id):
                for widget in detalles_frame.winfo_children():
                    widget.destroy()

                try:
                    db = sqlite3.connect("database.db")
                    c = db.cursor()

                    c.execute("""
                    SELECT productos.nombre, detalle_venta.cantidad, detalle_venta.precio_un
                    FROM detalle_venta
                    JOIN productos ON productos.id = detalle_venta.producto_id
                    WHERE detalle_venta.venta_id = ?
                    """, (venta_id,))
                    detalles = c.fetchall()

                    if detalles:
                        # Mostrar el frame de detalles solo si hay resultados
                        detalles_frame.place(relx=0.5, rely=0.45, anchor="n", width=900, height=220)

                        # Crear un frame para los encabezados
                        header_frame = tk.Frame(detalles_frame, bg="grey")
                        header_frame.place(relx=0.5, rely=0, anchor="n", width=900, height=40)

                        # Encabezados
                        tk.Label(header_frame, text="Producto", font=("Arial", 12, "bold"), bg="grey", fg="white", width=30, borderwidth=0, relief="flat").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                        tk.Label(header_frame, text="Cantidad", font=("Arial", 12, "bold"), bg="grey", fg="white", width=15, borderwidth=0, relief="flat").grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
                        tk.Label(header_frame, text="Precio", font=("Arial", 12, "bold"), bg="grey", fg="white", width=15, borderwidth=0, relief="flat").grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

                        # Configurar canvas para los detalles
                        canvas_detalles = tk.Canvas(detalles_frame, bg="white", width=900, height=200)  # Altura mínima de 200
                        canvas_detalles.place(relx=0.5, rely=0.10, anchor="n")

                        # Frame que va dentro del canvas
                        frame_in_canvas_detalles = tk.Frame(canvas_detalles, bg="white")

                        # Agregar frame al canvas
                        canvas_detalles.create_window((0, 0), window=frame_in_canvas_detalles, anchor="nw")

                        # Agregar contenido de detalles
                        for idx, detalle in enumerate(detalles, 1):
                            nombre, cantidad, precio_un = detalle

                            tk.Label(frame_in_canvas_detalles, text=nombre, font=("Arial", 12), anchor="w", width=30).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
                            tk.Label(frame_in_canvas_detalles, text=f"{cantidad}u", font=("Arial", 12), anchor="w", width=15).grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                            tk.Label(frame_in_canvas_detalles, text=f"${precio_un:.2f} c/u", font=("Arial", 12), anchor="w", width=15).grid(row=idx, column=2, padx=10, pady=5, sticky="w")

                        # Actualizar scroll region
                        frame_in_canvas_detalles.update_idletasks()

                        # Ajustar la altura del canvas según la cantidad de filas
                        num_filas = len(detalles)
                        altura_fila = 30
                        altura_canvas = min(num_filas, 5) * altura_fila + 40  # +40 para los encabezados

                        # Asegurarse de que el canvas tenga la altura mínima de 200, y ajuste la scrollregion
                        canvas_detalles.config(height=max(altura_canvas, 200))
                        canvas_detalles.config(scrollregion=canvas_detalles.bbox("all"))

                        # Habilitar scroll solo si hay más de 5 filas
                        if num_filas > 5:
                            # Vincular el scroll solo cuando el ratón esté sobre el canvas de detalles
                            canvas_detalles.bind("<Enter>", lambda e: canvas_detalles.bind_all("<MouseWheel>", lambda event: canvas_detalles.yview_scroll(int(-1 * (event.delta / 120)), "units")))
                            canvas_detalles.bind("<Leave>", lambda e: canvas_detalles.unbind_all("<MouseWheel>"))
                        else:
                            canvas_detalles.unbind("<MouseWheel>")  # Desactivar scroll si hay 5 o menos filas

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
                finally:
                    if c:
                        c.close()
                    if db:
                        db.close()


        ventana = tk.Toplevel()
        ventana.title("Historial de Ventas")
        ventana.state("zoomed")
        ventana.resizable(False, False)

        # Contenedor principal
        contenedor = tk.Frame(ventana)
        contenedor.pack(fill="both", expand=True)

        # Contenedores de entradas y filtros
        entradas_frame = tk.Frame(contenedor)
        entradas_frame.place(relx=0.5, rely=0.05, anchor="n")

        tk.Label(entradas_frame, text="Día:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        dia_entry = tk.Entry(entradas_frame, font=("Arial", 12), width=10, validate="focusout")
        dia_entry.grid(row=0, column=1, padx=10, pady=5)
        dia_entry.bind("<FocusOut>", validar_dia)

        tk.Label(entradas_frame, text="Mes:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
        mes_entry = tk.Entry(entradas_frame, font=("Arial", 12), width=10)
        mes_entry.grid(row=0, column=3, padx=10, pady=5)
        mes_entry.bind("<FocusOut>", validar_mes)

        tk.Label(entradas_frame, text="Año:", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5)
        anio_entry = tk.Entry(entradas_frame, font=("Arial", 12), width=10)
        anio_entry.grid(row=0, column=5, padx=10, pady=5)

        # Botón de búsqueda
        buscar_btn = tk.Button(entradas_frame, text="Buscar", font=("Arial", 12), command=buscar_por_fecha)
        buscar_btn.grid(row=0, column=6, padx=10, pady=5)

        # Frame para mostrar las ventas
        ventas_frame = tk.Frame(contenedor, bg="white")

        # Frame para mostrar los detalles
        detalles_frame = tk.Frame(contenedor, bg="white")

        menu_btn= tk.Button(ventana, text="VOLVER", font=("Arial", 12), fg="red", command=lambda:[ventana_principal(),ventana.destroy])
        menu_btn.pack()
        menu_btn.place(x=50, y=700)

        ventas_frame.place_forget()
        detalles_frame.place_forget()



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


        tk.Button(window, text="Volver", fg="red", font=("arial", 12), borderwidth=5, cursor = "hand2",relief = "raised", command=lambda:[ventana_principal(),window.destroy]).place(x=50, y=620)
       
        # Evento de teclado para actualizar las sugerencias cuando se escribe en el Entry
        entry_widget.bind("<KeyRelease>", actualizar_sugerencias)


        # Evento para seleccionar el producto cuando se presiona una tecla en la Listbox
        lista_sugerencias.bind("<Return>", seleccionar_sugerencia)
    
    def manual():
        """Abre una ventana que muestra el contenido del archivo del manual."""
        try:
            # Leer el archivo del manual
            with open("manual.txt", "r", encoding="utf-8") as f:
                contenido = f.read()

            # Crear una ventana para el manual
            ventana_manual = tk.Toplevel()
            ventana_manual.title("Manual de Usuario")
            ventana_manual.state("zoomed")  # Tamaño de la ventana

            # Crear un Text widget para mostrar el contenido del manual
            text_widget = tk.Text(ventana_manual, wrap=tk.WORD, font=("Arial", 12))
            text_widget.pack(expand=True, fill=tk.BOTH)

            # Insertar el contenido del archivo en el Text widget
            text_widget.insert(tk.END, contenido)

            # Deshabilitar la edición del contenido
            text_widget.config(state=tk.DISABLED)

            # Agregar un botón para cerrar la ventana
            btn_cerrar = tk.Button(ventana_manual, text="Cerrar", command=ventana_manual.destroy)
            btn_cerrar.pack(pady=10)

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo del manual no se encontró.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error: {str(e)}")
    

#########FIN DE PRORGAMA PRINCIPAL#################
    principal.mainloop()

"""
LISTA DE COSAS POR TERMINAR
*Agregar si es que se encuentra un error o se quiere agregar una nueva funcion
"""
   
if __name__ == '__main__':
    ventana_principal()
