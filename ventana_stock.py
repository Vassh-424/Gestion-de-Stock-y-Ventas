from tkinter import *
from tkinter import Listbox, END
import backend

db= backend.Database()

def stock():
    stock = Tk()
    stock.state("zoomed")
    stock.title("Gestion de Stock")
    stock.resizable(0, 0)


    marcos = Frame(stock)
    marcos.grid(row=0, column=0, padx=20, pady=20)  # Ajustar el marco
    marcos.config(width=1500, height=800)


    agregar = Button(marcos, text="AGREGAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_agregar())
    agregar.grid(row=0, column=0, padx=10, pady=20, sticky="w")


    buscar = Button(marcos, text="BUSCAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_ver(db))
    buscar.grid(row=2, column=0, padx=10, pady=20, sticky="w")  # Ajuste del padding


    modificar = Button(marcos, text="MODIFICAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:modificar_producto())
    modificar.grid(row=3, column=0, padx=10, pady=40, sticky="w")  # Espacio adicional


    eliminar = Button(marcos, text="ELIMINAR PRODUCTO", fg="blue", font=("arial", 25), cursor="hand2", relief="raised", command= lambda:ventana_eliminar())
    eliminar.grid(row=4, column=0, padx=10, pady=20, sticky="w")


    menu = Button(marcos, text="Volver", fg="red", font=("arial", 20), cursor="hand2", relief="raised", command=lambda:[cerrar_stock()])
    menu.grid(row=5, column=0, padx=10, pady=20, sticky="w")



    def cerrar_stock():
        stock.destroy()
        
    ########AGREGAR PRODUCTO############

    def ventana_agregar():
        window = Toplevel()
        window.state("zoomed")
        window.title("Agregar Productos")
        window.resizable(0, 0)

        # Etiqueta de título
        Label(window, text="AGREGAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)

        # Variables para entradas
        entryproducto = StringVar()
        entryprecio = StringVar()
        entrycantidad = StringVar()

        # Entradas de texto
        Entry(window, textvariable=entryproducto).place(x=50, y=150)
        Entry(window, textvariable=entryprecio).place(x=50, y=230)
        Entry(window, textvariable=entrycantidad).place(x=50, y=310)

        # Etiquetas
        Label(window, text="INGRESE EL NOMBRE DEL PRODUCTO.", padx=10).place(x=30, y=115)
        Label(window, text="INGRESE LA CANTIDAD DEL PRODUCTO", padx=10).place(x=30, y=200)
        Label(window, text="INGRESE EL PRECIO DEL PRODUCTO", padx=10).place(x=30, y=280)

        # Etiquetas para mensajes
        success_label = Label(window, text="", fg="green")
        success_label.place(x=50, y=400)

        error_label = Label(window, text="", fg="red")
        error_label.place(x=50, y=420)

        #### FUNCION PARA AGREGAR LOS PRODUCTOS
        def guarda():
            nombre = entryproducto.get()
            precio = entryprecio.get()
            cantidad = entrycantidad.get()

            # Limpiar etiquetas de error y éxito
            error_label.config(text="")
            success_label.config(text="")

            if not nombre or not precio or not cantidad:
                error_label.config(text="Todos los campos son obligatorios")
                return

            try:
                precio = float(precio)
                cantidad = int(cantidad)
            except ValueError:
                error_label.config(text="Precio debe ser un número y cantidad debe ser un entero")
                return

            # Conectar a la base de datos y agregar el artículo
            db.agregar_producto(nombre, cantidad, precio)
            success_label.config(text="ARTICULO INGRESADO CORRECTAMENTE")
            
            # Limpiar campos
            entryproducto.set("")
            entryprecio.set("")
            entrycantidad.set("")

        # Botón GUARDAR
        guardarb = Button(window, text="GUARDAR", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=guarda)
        guardarb.place(x=40, y=350)

        # Botón para regresar al MENU
        menu = Button(window, text="MENU", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
        menu.place(x=50, y=450)

    #############BUSCAR PRODUCTO#############

    def ventana_ver(db):
        def mostrar_productos(filtro=""):
            # Clear existing widgets in the productos_frame
            for widget in productos_frame.winfo_children():
                widget.destroy()

            # Retrieve products from the database using the provided filter
            productos = db.obtener_productos(filtro)

            # Header row styling
            Label(productos_frame, text="NOMBRE", bg="lightgray", width=30, anchor="w", font=("Arial", 12, "bold"), relief="solid").grid(row=0, column=0, padx=10, pady=5)
            Label(productos_frame, text="PRECIO", bg="lightgray", width=15, anchor="w", font=("Arial", 12, "bold"), relief="solid").grid(row=0, column=1, padx=10, pady=5)
            Label(productos_frame, text="CANTIDAD", bg="lightgray", width=10, anchor="w", font=("Arial", 12, "bold"), relief="solid").grid(row=0, column=2, padx=10, pady=5)

            if productos:
                for i, (nombre, precio, cantidad) in enumerate(productos, start=1):
                    color_fondo = "lightcoral" if cantidad < 10 else "white"
                    Label(productos_frame, text=nombre, bg=color_fondo, anchor="w", font=("Arial", 10), relief="solid").grid(row=i, column=0, padx=10, pady=5, sticky="w")
                    Label(productos_frame, text=f"${precio:.2f}", bg=color_fondo, anchor="w", font=("Arial", 10), relief="solid").grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    Label(productos_frame, text=cantidad, bg=color_fondo, anchor="w", font=("Arial", 10), relief="solid").grid(row=i, column=2, padx=10, pady=5, sticky="w")
            else:
                Label(productos_frame, text="No se encontraron productos.", bg="white", font=("Arial", 10)).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        def filtrar_productos(event=None):
            # Fetch text from the search bar and use it as a filter
            filtro = entry_busqueda.get().strip()
            mostrar_productos(filtro)

        # Main window setup
        window = Toplevel()
        window.state("zoomed")
        window.title("Busqueda")
        window.resizable(0,0)

        frame = Frame(window, bg="white")
        frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        # Search bar
        entry_busqueda = Entry(frame, font=("Arial", 14))
        entry_busqueda.grid(row=0, column=0, columnspan=4, padx=40, pady=10, sticky="nsew")
        entry_busqueda.bind("<KeyRelease>", filtrar_productos)

        # Products frame
        productos_frame = Frame(frame, bg="white")
        productos_frame.grid(row=1, column=0, columnspan=4, padx=50, pady=20, sticky="nsew")

        # Grid configuration for adaptive resizing
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Menu button
        menu = Button(frame, text="MENU", fg="red", font=("Arial", 12), cursor="hand2", relief="raised", command=window.destroy)
        menu.grid(row=2, column=0, columnspan=4, pady=10)

        # Initial product display
        mostrar_productos()


    ########MODIFICAR PRODUCTO############

    def modificar_producto():
        window = Toplevel()
        window.state("zoomed")
        window.title("Modificar producto")
        window.resizable(0, 0)

        # Título de la ventana
        Label(window, text="MODIFICAR PRODUCTOS:", bg="white", fg="black").place(x=50, y=50)

        # Variable para el nombre del producto
        entry_nombre = StringVar()
        entry_widget = Entry(window, textvariable=entry_nombre)
        entry_widget.place(x=50, y=150)

        # Etiqueta para el nombre del producto
        Label(window, text="Nombre del producto:", font=("Arial", 12), padx=10).place(x=30, y=100)

        # Listbox para autocompletar
        lista_sugerencias = Listbox(window, width=30, height=5, font=("Arial", 10))
        lista_sugerencias.place(x=50, y=180)  # Colocar justo debajo del Entry
        lista_sugerencias.place_forget()  # Ocultarla inicialmente

        # Frame para los inputs de modificar producto (oculto inicialmente)
        frame_modificar = Frame(window)
        frame_modificar.place(x=400, y=100)
        frame_modificar.place_forget()

        # Variables para los nuevos valores
        entry_nuevo_nombre = StringVar()
        entry_nueva_cantidad = StringVar()
        entry_nuevo_precio = StringVar()

        # Etiquetas e Inputs en el frame
        Label(frame_modificar, text="Nuevo Nombre:", padx=10, font=("Arial", 12)).grid(row=0, column=0, pady=5)
        Entry(frame_modificar, textvariable=entry_nuevo_nombre).grid(row=0, column=1, pady=5)

        Label(frame_modificar, text="Nueva Cantidad:", padx=10).grid(row=1, column=0, pady=5)
        Entry(frame_modificar, textvariable=entry_nueva_cantidad).grid(row=1, column=1, pady=5)

        Label(frame_modificar, text="Nuevo Precio:", padx=10).grid(row=2, column=0, pady=5)
        Entry(frame_modificar, textvariable=entry_nuevo_precio).grid(row=2, column=1, pady=5)

        warning_label = Label(frame_modificar, text="", fg="red")
        warning_label.grid(row=5, column=4)

        success_label = Label(frame_modificar, text="", fg="green")
        success_label.grid(row=5, column=4)

        error_label = Label(frame_modificar, text="", fg="red")
        error_label.grid(row=5, column=4)

        def actualizar_sugerencias(event=None):
            """
            Función que busca productos que coincidan con el texto ingresado y actualiza la lista de sugerencias.
            """
            nombre_producto = entry_nombre.get()
            
            # Si no hay texto, ocultamos la lista de sugerencias
            if not nombre_producto:
                lista_sugerencias.place_forget()
                return

            # Llamar a la función del backend para obtener los productos
            productos = db.buscar_productos(nombre_producto)

            # Limpiar la lista de sugerencias antes de agregar los nuevos resultados
            lista_sugerencias.delete(0, END)

            if productos:
                # Si hay productos, agregarlos a la lista de sugerencias
                for producto in productos:
                    lista_sugerencias.insert(END, producto[0])

                # Mostrar la Listbox si hay resultados
                lista_sugerencias.place(x=50, y=180)
            else:
                # Si no hay coincidencias, ocultar la lista
                lista_sugerencias.place_forget()

        def seleccionar_sugerencia(event=None):
            """
            Función que se ejecuta al seleccionar un producto de la lista de sugerencias.
            """
            seleccion = lista_sugerencias.get(lista_sugerencias.curselection())  # Obtener el producto seleccionado
            entry_nombre.set(seleccion)  # Establecer el nombre en el Entry
            lista_sugerencias.place_forget()  # Ocultar la lista de sugerencias

            # Mostrar el frame para modificar el producto
            frame_modificar.place(x=400, y=100)

        # Vincular el evento de actualización de sugerencias al campo de texto
        entry_widget.bind("<KeyRelease>", actualizar_sugerencias)

        # Vincular el evento de selección de sugerencia
        lista_sugerencias.bind("<ButtonRelease-1>", seleccionar_sugerencia)

        # Cuando se hace clic en el Entry, ocultar el frame de modificación si no se ha seleccionado nada
        entry_widget.bind("<Button-1>", lambda event: frame_modificar.place_forget())

        def ocultar_modificar(event=None):
            """
            Función que oculta el frame de modificación y resetea los campos.
            """
            frame_modificar.place_forget()
            entry_nuevo_nombre.set("")
            entry_nueva_cantidad.set("")
            entry_nuevo_precio.set("")


        def validar_nombre(nombre_producto):
            print(f"Validando nombre: {nombre_producto}")  # Para depuración
            if not nombre_producto.strip():  # Verifica si está vacío o solo espacios
                return "El nombre del producto no puede estar vacío"
            return None

        def validar_cantidad(nueva_cantidad):
            print(f"Validando cantidad: {nueva_cantidad}")  # Para depuración
            if not nueva_cantidad.isdigit() or int(nueva_cantidad) <= 0:
                return "La cantidad debe ser un número entero positivo"
            return None

        def validar_precio(nuevo_precio):
            print(f"Validando precio: {nuevo_precio}")  # Para depuración
            try:
                nuevo_precio_float = float(nuevo_precio)
                if nuevo_precio_float <= 0:
                    return "El precio debe ser mayor que 0"
            except ValueError:
                return "El precio debe ser un número positivo"
            return None
        
        def actualizar_cantidad():
            nueva_cantidad = entry_nueva_cantidad.get()
            nombre_producto = entry_nombre.get()  # Obtener el nombre del producto
            error = validar_cantidad(nueva_cantidad)
            if error:
                error_label.config(text=error)  # Mostrar mensaje de error
                success_label.config(text="")  # Limpiar mensaje de éxito
            else:
                error_label.config(text="")  # Limpiar mensaje de error
                if db.actualizar_cantidad(nombre_producto, int(nueva_cantidad)):
                    success_label.config(text="Cantidad actualizada correctamente.")
                else:
                    error_label.config(text="No se pudo actualizar la cantidad.")  # Mensaje de error

        def actualizar_precio():
            nuevo_precio = entry_nuevo_precio.get()
            nombre_producto = entry_nombre.get()  # Obtener el nombre del producto
            error = validar_precio(nuevo_precio)
            if error:
                error_label.config(text=error)  # Mostrar mensaje de error
                success_label.config(text="")  # Limpiar mensaje de éxito
            else:
                error_label.config(text="")  # Limpiar mensaje de error
                if db.actualizar_precio(nombre_producto, float(nuevo_precio)):
                    success_label.config(text="Precio actualizado correctamente.")
                else:
                    error_label.config(text="No se pudo actualizar el precio.")  # Mensaje de error

        def actualizar_nombre():
            nuevo_nombre = entry_nuevo_nombre.get()  # Obtener el nuevo nombre del producto
            nombre_producto = entry_nombre.get()  # Obtener el nombre actual del producto
            error = validar_nombre(nuevo_nombre)
            if error:
                error_label.config(text=error)  # Mostrar mensaje de error
                success_label.config(text="")  # Limpiar mensaje de éxito
            else:
                error_label.config(text="")  # Limpiar mensaje de error
                if db.actualizar_nombre(nombre_producto, nuevo_nombre):
                    success_label.config(text="Se actualizo correctamente.")
                else:
                    error_label.config(text="No se pudo actualizar el nombre.") 

        # Botones para confirmar cambios individuales
        bt_actualizar_cantidad = Button(frame_modificar, text="Actualizar Cantidad", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=actualizar_cantidad)
        bt_actualizar_cantidad.grid(row=1, column=2, pady=5)

        bt_actualizar_precio = Button(frame_modificar, text="Actualizar Precio", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=actualizar_precio)
        bt_actualizar_precio.grid(row=2, column=2, padx=5)

        # Botón para confirmar cambios del nombre
        bt_modificar = Button(frame_modificar, text="Actualizar nombre", fg="blue", font=("arial", 12), cursor="hand2", relief="raised", command=actualizar_nombre)
        bt_modificar.grid(row=0, column=2, pady=5)

        bt_cancelar = Button(frame_modificar, text="CANCELAR", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=ocultar_modificar)
        bt_cancelar.grid(row=5, column=1, pady=10)


        # Botón para Volver
        menu = Button(window, text="Volver", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
        menu.pack()
        menu.place(x=50, y=350)


        ########ELIMINAR PRODUCTO##########
    def ventana_eliminar():
        window = Toplevel()
        window.state("zoomed")
        window.title("ELIMINAR PRODUCTOS")
        window.resizable(0, 0)

        Label(window, text=" ELIMINAR PRODUCTOS :", bg="white", fg="black").place(x=50, y=50)

        # Variable para el nombre del producto
        nombre_producto = StringVar()
        entry_widget = Entry(window, textvariable=nombre_producto, font=("Arial", 12), width=30)
        entry_widget.place(x=50, y=150)

        # Etiqueta para el nombre
        Label(window, text="Ingrese el nombre del producto a eliminar:", font=("Arial", 12), padx=10).place(x=30, y=115)

        # Listbox para autocompletar
        lista_sugerencias = Listbox(window, width=30, height=5, font=("Arial", 10))
        lista_sugerencias.place(x=50, y=180)  # Colocar justo debajo del Entry
        lista_sugerencias.place_forget()  # Ocultarla inicialmente

        # Etiquetas para mensajes de éxito y error
        success_label = Label(window, text="", fg="green", font=("Arial", 12))
        success_label.place(x=50, y=400)

        error_label = Label(window, text="", fg="red", font=("Arial", 12))
        error_label.place(x=50, y=430)


        def actualizar_sugerencias(event=None):
            texto_ingresado = nombre_producto.get()
            if not texto_ingresado:
                lista_sugerencias.place_forget()
                return

            # Llamar al método del backend para obtener los productos
            productos = db.buscar_productos(texto_ingresado)

            # Actualizar la Listbox con las sugerencias
            lista_sugerencias.delete(0, END)

            if productos:
                for producto in productos:
                    lista_sugerencias.insert(END, producto[0])
                lista_sugerencias.place(x=50, y=180)  # Mostrar la Listbox si hay resultados
            else:
                lista_sugerencias.place_forget()  # Ocultar la Listbox si no hay coincidencias

        def seleccionar_sugerencia(event=None):
            seleccion = lista_sugerencias.get(lista_sugerencias.curselection())
            nombre_producto.set(seleccion)
            lista_sugerencias.place_forget()

        def eliminar():
            # Limpiar etiquetas de mensajes
            success_label.config(text="")
            error_label.config(text="")

            nombre = nombre_producto.get()

            # Verificar si se ingresó un nombre
            if not nombre:
                error_label.config(text="Debe ingresar un nombre de producto.")
                return

            # Llamar al método del backend para eliminar el producto
            if db.eliminar_producto(nombre):
                success_label.config(text=f"Producto '{nombre}' eliminado correctamente.")
            else:
                error_label.config(text=f"No se encontró el producto '{nombre}'.")

        # Botón ELIMINAR
        eliminar_btn = Button(window, text="ELIMINAR", fg="blue", font=("Arial", 12), cursor="hand2", relief="raised", command=eliminar)
        eliminar_btn.place(x=50, y=350)
        
        menu = Button(window, text="Cancelar", fg="red", font=("arial", 12), cursor="hand2", relief="raised", command=window.destroy)
        menu.pack()
        menu.place(x=50, y=460)

        # Evento de selección en la lista de sugerencias
        lista_sugerencias.bind("<<ListboxSelect>>", seleccionar_sugerencia)

        # Evento de actualización de sugerencias al escribir en el Entry
        entry_widget.bind("<KeyRelease>", actualizar_sugerencias)
