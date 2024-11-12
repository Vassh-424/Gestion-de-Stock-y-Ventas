
import sqlite3
from tkinter import *
from tkinter import messagebox
import backend

db= backend.Database()

def historial(): 
    def validar_dia(event):
        try:
            dia = int(dia_entry.get())
            if dia < 1 or dia > max_dias():
                dia_entry.delete(0, END)
        except ValueError:
            pass

    def validar_mes(event):
        try:
            mes = int(mes_entry.get())
            if mes < 1 or mes > 12:
                mes_entry.delete(0, END)
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
        dia = dia_entry.get()  # Asegúrate de que el valor obtenido sea el correcto
        mes = mes_entry.get()  # Formatea mes a dos dígitos
        anio = anio_entry.get()  # El año generalmente es de cuatro dígitos, así que no se formatea

        print(f"Buscando ventas para - Día: {dia}, Mes: {mes}, Año: {anio}")

        # Si no se especifica nada, no hacer nada
        if not dia and not mes and not anio:
            ventas_frame.place_forget()
            detalles_frame.place_forget()
            return

        # Asegúrate de que los valores de mes, día y año sean los esperados
        print(f"Valores recibidos: Día = {dia}, Mes = {mes}, Año = {anio}")

        # Llamar al método del backend usando la instancia db
        resultados = db.buscar_ventas_por_fecha(dia, mes, anio)
        print(f"Resultados obtenidos: {resultados}")  # Imprime los resultados
        mostrar_ventas(resultados if resultados else [])

    def mostrar_ventas(query=None):
        for widget in ventas_frame.winfo_children():
            widget.destroy()

        if query is None:
            ventas_frame.place_forget()
            detalles_frame.place_forget()
            return
  # Llama al método para obtener todas las ventas
            # Mostrar el frame de ventas solo si hay resultados
        ventas_frame.place(relx=0.5, rely=0.15, anchor="n", width=900, height=210)  # Aumentar la altura
        ventas_frame.config(borderwidth=1)

        # Crear un frame para los encabezados
        header_frame = Frame(ventas_frame, bg="grey")  # Color para encabezados
        header_frame.place(relx=0.5, rely=0, anchor="n", width=900, height=40)

        # Encabezados
        Label(header_frame, text="Venta", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        Label(header_frame, text="Fecha", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        Label(header_frame, text="Total", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        Label(header_frame, text="Hora", font=("Arial", 12, "bold"), bg="grey", fg="white", width=20).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # Configurar canvas para las ventas
        canvas_ventas = Canvas(ventas_frame, bg="white", width=900, height= 300)  # Ajustar la altura a automático
        canvas_ventas.place(relx=0.5, rely=0.10, anchor="n")

        # Frame que va dentro del canvas
        frame_in_canvas_ventas = Frame(canvas_ventas, bg="white", height=300)

        # Agregar frame al canvas
        canvas_ventas.create_window((0, 0), window=frame_in_canvas_ventas, anchor="nw")

        # Agregar contenido de ventas
        for idx, venta in enumerate(query, 1):
            venta_id, fecha, hora, total = venta  # Asumimos que el total ya se está enviando correctamente

            Button(frame_in_canvas_ventas, text=f"{idx}", font=("Arial", 12), width=20,
    command=lambda vid=venta_id: mostrar_detalles(vid)).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            Label(frame_in_canvas_ventas, text=fecha, font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            Label(frame_in_canvas_ventas, text=f"${total:.2f}", font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=2, padx=10, pady=5, sticky="w")
            Label(frame_in_canvas_ventas, text=hora, font=("Arial", 12), anchor="w", width=20).grid(row=idx, column=3, padx=10, pady=5, sticky="w")

        # Actualizar scroll region
        frame_in_canvas_ventas.update_idletasks()

        # Ajustar la altura del canvas según la cantidad de filas
        num_filas = len(query)
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

        def mostrar_detalles(venta_id):
            # Limpiar cualquier widget existente en el frame de detalles
            for widget in detalles_frame.winfo_children():
                widget.destroy()

            try:
                # Llamar al método del backend para obtener los detalles de la venta
                detalles = db.obtener_detalles_venta(venta_id)

                if detalles:
                    # Mostrar el frame de detalles solo si hay resultados
                    detalles_frame.place(relx=0.5, rely=0.45, anchor="n", width=900, height=220)

                    # Crear un frame para los encabezados
                    header_frame = Frame(detalles_frame, bg="grey")
                    header_frame.place(relx=0.5, rely=0, anchor="n", width=900, height=40)

                    # Encabezados
                    Label(header_frame, text="Producto", font=("Arial", 12, "bold"), bg="grey", fg="white", width=30, borderwidth=0, relief="flat").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                    Label(header_frame, text="Cantidad", font=("Arial", 12, "bold"), bg="grey", fg="white", width=15, borderwidth=0, relief="flat").grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
                    Label(header_frame, text="Precio", font=("Arial", 12, "bold"), bg="grey", fg="white", width=15, borderwidth=0, relief="flat").grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

                    # Configurar canvas para los detalles
                    canvas_detalles = Canvas(detalles_frame, bg="white", width=900, height=200)  # Altura mínima de 200
                    canvas_detalles.place(relx=0.5, rely=0.10, anchor="n")

                    # Frame que va dentro del canvas
                    frame_in_canvas_detalles = Frame(canvas_detalles, bg="white")

                    # Agregar frame al canvas
                    canvas_detalles.create_window((0, 0), window=frame_in_canvas_detalles, anchor="nw")

                    # Agregar contenido de detalles
                    for idx, detalle in enumerate(detalles, 1):
                        nombre, cantidad, precio_un = detalle

                        Label(frame_in_canvas_detalles, text=nombre, font=("Arial", 12), anchor="w", width=30).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
                        Label(frame_in_canvas_detalles, text=f"{cantidad}u", font=("Arial", 12), anchor="w", width=15).grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                        Label(frame_in_canvas_detalles, text=f"${precio_un:.2f} c/u", font=("Arial", 12), anchor="w", width=15).grid(row=idx, column=2, padx=10, pady=5, sticky="w")

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

    ventana = Toplevel()
    ventana.title("Historial de Ventas")
    ventana.state("zoomed")
    ventana.resizable(0, 0)
    
    instrucciones_frame = Frame(ventana)
    instrucciones_frame.place(relx=0.5, rely=0.15, anchor="n")  # Ajusta la posición

    # Contenedor principal
    contenedor = Frame(ventana)
    contenedor.pack(fill="both", expand=True)
    
    Label(contenedor, text="Por favor, utilizar el año completo (Ejemplo: 2024, no 24)", font=("Arial", 10)).pack()

    # Contenedores de entradas y filtros
    entradas_frame = Frame(contenedor)
    entradas_frame.place(relx=0.5, rely=0.05, anchor="n")

    Label(entradas_frame, text="Día:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    dia_entry = Entry(entradas_frame, font=("Arial", 12), width=10, validate="focusout")
    dia_entry.grid(row=0, column=1, padx=10, pady=5)
    dia_entry.bind("<FocusOut>", validar_dia)

    Label(entradas_frame, text="Mes:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
    mes_entry = Entry(entradas_frame, font=("Arial", 12), width=10)
    mes_entry.grid(row=0, column=3, padx=10, pady=5)
    mes_entry.bind("<FocusOut>", validar_mes)

    Label(entradas_frame, text="Año:", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=5)
    anio_entry = Entry(entradas_frame, font=("Arial", 12), width=10)
    anio_entry.grid(row=0, column=5, padx=10, pady=5)
    


    # Botón de búsqueda
    buscar_btn = Button(entradas_frame, text="Buscar", font=("Arial", 12), command=buscar_por_fecha)
    buscar_btn.grid(row=0, column=6, padx=10, pady=5)

    # Frame para mostrar las ventas
    ventas_frame = Frame(contenedor, bg="white")

    # Frame para mostrar los detalles
    detalles_frame = Frame(contenedor, bg="white")

    menu_btn= Button(ventana, text="VOLVER", font=("Arial", 12), fg="red", command=ventana.destroy)
    menu_btn.pack()
    menu_btn.place(x=50, y=700)

    ventas_frame.place_forget()
    detalles_frame.place_forget()

#Cambios, separar las funciones backend del frontend