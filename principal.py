import tkinter as tk

class TiendaElectronicos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tienda Electrónica")
        self.geometry("1200x800")  # Pantalla completa
        self.attributes("-fullscreen", True)  # Pantalla completa no resizable

        # Inicializar variables para el control de categorías
        self.index_categorias = 0
        self.categorias_por_slide = 5

        # Lista de categorías con placeholders para imágenes
        self.categorias = [
            ("PC", "Imagen1"), ("Accesorios", "Imagen2"), 
            ("Componentes de PC", "Imagen3"), ("Laptops", "Imagen4"), 
            ("Monitores", "Imagen5"), ("Teclados", "Imagen6"), 
            ("Ratones", "Imagen7"), ("Impresoras", "Imagen8"),
            ("Sillas", "Imagen9"), ("Cables", "Imagen10")
        ]

        # Frame para la barra de búsqueda y el título
        frame_superior = tk.Frame(self)
        frame_superior.pack(fill="x", pady=10)

        # Título de la tienda alineado a la izquierda
        lbl_titulo = tk.Label(frame_superior, text="Tienda Electrónica", font=("Helvetica", 20, "bold"))
        lbl_titulo.pack(side="left", padx=(10, 5))  # Pequeño espacio entre el título y la barra de búsqueda

        # Barra de búsqueda alineada a la izquierda, cerca del título
        self.entry_busqueda = tk.Entry(frame_superior, width=80, font=("Helvetica", 14))
        self.entry_busqueda.pack(side="left", padx=(100, 10))  # Pequeño espacio entre la barra de búsqueda y el borde

        self.entry_busqueda.bind("<Return>", self.buscar_producto)  # Asigna la tecla Enter para activar la búsqueda

        # Frame principal para las categorías con botones de navegación
        self.frame_principal = tk.Frame(self)
        self.frame_principal.pack(pady=10)
        
        # Botón de navegación izquierda
        self.btn_left = tk.Button(self.frame_principal, text="◀", command=self.mover_izquierda)
        self.btn_left.grid(row=0, column=0)
        self.btn_left.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Frame para mostrar las categorías
        self.frame_categorias = tk.Frame(self.frame_principal)
        self.frame_categorias.grid(row=0, column=1)

        # Botón de navegación derecha
        self.btn_right = tk.Button(self.frame_principal, text="▶", command=self.mover_derecha)
        self.btn_right.grid(row=0, column=2)

        # Footer o área para otros elementos
        lbl_footer = tk.Label(self, text="© 2024 Tienda Electrónica", font=("Helvetica", 10))
        lbl_footer.pack(side="bottom", pady=10)

        # Botón de cerrar programa
        btn_cerrar = tk.Button(self, text="Cerrar Programa", command=self.cerrar_programa, font=("Helvetica", 12))
        btn_cerrar.pack(side="bottom", pady=10)

        # Mostrar las categorías iniciales
        self.mostrar_categorias()

    def mostrar_categorias(self):
        # Limpiar categorías previas
        for widget in self.frame_categorias.winfo_children():
            widget.destroy()

        # Calcular las categorías a mostrar
        categorias_a_mostrar = self.categorias[self.index_categorias:self.index_categorias + self.categorias_por_slide]
        
        for categoria, imagen in categorias_a_mostrar:
            frame = tk.Frame(self.frame_categorias, bd=2, relief="groove", width=200, height=200)
            frame.pack(side="left", padx=20)
            
            # Placeholder para la imagen
            lbl_imagen = tk.Label(frame, text="Imagen Aquí", width=20, height=10, bg="lightgray")
            lbl_imagen.pack(pady=10)
            
            # Nombre de la categoría
            lbl_categoria = tk.Label(frame, text=categoria, font=("Helvetica", 14))
            lbl_categoria.pack(pady=5)
        
        # Deshabilitar botones si no hay más categorías a la izquierda o derecha
        self.btn_left.config(state=tk.DISABLED if self.index_categorias == 0 else tk.NORMAL)
        self.btn_right.config(state=tk.DISABLED if self.index_categorias + self.categorias_por_slide >= len(self.categorias) else tk.NORMAL)

    def mover_derecha(self):
        if self.index_categorias + self.categorias_por_slide < len(self.categorias):
            self.index_categorias += self.categorias_por_slide
            self.mostrar_categorias()

    def mover_izquierda(self):
        if self.index_categorias - self.categorias_por_slide >= 0:
            self.index_categorias -= self.categorias_por_slide
            self.mostrar_categorias()

    def buscar_producto(self, event=None):
        # Obtener el término de búsqueda
        query = self.entry_busqueda.get()
        print(f"Buscando: {query}")
        # Mostrar los resultados de búsqueda en la pantalla principal
        self.mostrar_resultados_busqueda(query)

    def mostrar_resultados_busqueda(self, query):
        # Limpiar el frame principal y mostrar resultados de búsqueda
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        # Título de los resultados
        lbl_resultados = tk.Label(self.frame_principal, text=f"Mostrando resultados para: {query}", font=("Helvetica", 14))
        lbl_resultados.grid(row=0, column=0, columnspan=3, pady=20)

        # Placeholder para los resultados
        lbl_placeholder = tk.Label(self.frame_principal, text="Productos encontrados se mostrarán aquí", font=("Helvetica", 12))
        lbl_placeholder.grid(row=1, column=0, columnspan=3)

        # Botón para volver a la vista de categorías
        btn_volver = tk.Button(self.frame_principal, text="Volver", command=self.mostrar_categorias)
        btn_volver.grid(row=2, column=1, pady=10)

    def cerrar_programa(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = TiendaElectronicos()
    app.mainloop()











"""import tkinter as tk
from tkinter import ttk

class TiendaElectronica(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Tienda de Componentes Electrónicos")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.cerrar_programa)
        
        # Lista de categorías
        self.categorias = [
            ("PCs", "ruta/de/la/imagen_pc.png"),
            ("Accesorios", "ruta/de/la/imagen_accesorios.png"),
            ("Componentes de PC", "ruta/de/la/imagen_componentes.png"),
            ("Laptops", "ruta/de/la/imagen_laptops.png"),
            ("Monitores", "ruta/de/la/imagen_monitores.png"),
            ("Impresoras", "ruta/de/la/imagen_impresoras.png"),
            ("Teclados", "ruta/de/la/imagen_teclados.png"),
            ("Mouses", "ruta/de/la/imagen_mouses.png"),
            ("Auriculares", "ruta/de/la/imagen_auriculares.png"),
            ("Almacenamiento", "ruta/de/la/imagen_almacenamiento.png")
        ]
        
        self.index_categorias = 0
        self.categorias_por_slide = 5

        # Título de la tienda
        lbl_titulo = tk.Label(self, text="Tienda Electrónica", font=("Helvetica", 24, "bold"))
        lbl_titulo.pack(pady=20)
        
        # Frame principal para las categorías con scroll
        frame_principal = tk.Frame(self)
        frame_principal.pack(pady=10)
        
        # Botón de navegación izquierda
        self.btn_left = tk.Button(frame_principal, text="◀", command=self.mover_izquierda)
        self.btn_left.grid(row=0, column=0)
        self.btn_left.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Frame para mostrar las categorías
        self.frame_categorias = tk.Frame(frame_principal)
        self.frame_categorias.grid(row=0, column=1)

        # Botón de navegación derecha
        self.btn_right = tk.Button(frame_principal, text="▶", command=self.mover_derecha)
        self.btn_right.grid(row=0, column=2)

        # Footer o área para otros elementos
        lbl_footer = tk.Label(self, text="© 2024 Tienda Electrónica", font=("Helvetica", 10))
        lbl_footer.pack(side="bottom", pady=10)

        # Botón de cerrar programa
        btn_cerrar = tk.Button(self, text="Cerrar Programa", command=self.cerrar_programa, font=("Helvetica", 12))
        btn_cerrar.pack(side="bottom", pady=10)

        self.mostrar_categorias()

    def mostrar_categorias(self):
        for widget in self.frame_categorias.winfo_children():
            widget.destroy()

        categorias_a_mostrar = self.categorias[self.index_categorias:self.index_categorias + self.categorias_por_slide]
        
        for categoria, imagen in categorias_a_mostrar:
            frame = tk.Frame(self.frame_categorias, bd=2, relief="groove")
            frame.pack(side="left", padx=20)
            
            # Placeholder para la imagen
            lbl_imagen = tk.Label(frame, text="Imagen Aquí", width=20, height=10, bg="lightgray")
            lbl_imagen.pack(pady=10)
            
            # Nombre de la categoría
            lbl_categoria = tk.Label(frame, text=categoria, font=("Helvetica", 14))
            lbl_categoria.pack(pady=5)
        
        # Deshabilitar botones si no hay más categorías a la izquierda o derecha
        if self.index_categorias == 0:
            self.btn_left.config(state=tk.DISABLED)
        else:
            self.btn_left.config(state=tk.NORMAL)

        if self.index_categorias + self.categorias_por_slide >= len(self.categorias):
            self.btn_right.config(state=tk.DISABLED)
        else:
            self.btn_right.config(state=tk.NORMAL)

    def mover_derecha(self):
        if self.index_categorias + self.categorias_por_slide < len(self.categorias):
            self.index_categorias += self.categorias_por_slide
            self.mostrar_categorias()

    def mover_izquierda(self):
        if self.index_categorias - self.categorias_por_slide >= 0:
            self.index_categorias -= self.categorias_por_slide
            self.mostrar_categorias()

    def cerrar_programa(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = TiendaElectronica()
    app.mainloop()"""


