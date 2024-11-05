from tkinter import *
from tkinter import messagebox
import ventana_stock
import ventana_historial
import ventana_ventas

###############VENTANA PRINCIPAL#################


def ventana_principal():
    principal = Tk()
    principal.state("zoomed")
    principal.title("Gestion de Stock y Ventas")
    principal.resizable(0, 0)


    titulo= Label(text="GESTION DE STOCK Y VENTAS V1",padx=10, font=("Arial", 40, "bold"))
    titulo.pack()
    titulo.place(x=60,y=50)



    stockb=Button(principal,text="Stock", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised",  command = lambda:ventana_stock.stock())
    stockb.pack()
    stockb.place(x=900,y=150)


    ventasb=Button(principal,text="Nueva Venta", fg="blue", font=("arial", 30), state= "normal", borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_ventas.ventas())
    ventasb.pack()
    ventasb.place(x=900,y=300)


    detalle_ventasb= Button(principal, text="Historial de Ventas", fg="blue", font=("arial", 30), borderwidth=5, cursor = "hand2",relief = "raised", command= lambda:ventana_historial.historial())
    detalle_ventasb.pack()
    detalle_ventasb.place(x=900,y=450)
    
    btn_manual = Button(principal, text="Manual",  fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:manual())
    btn_manual.pack()
    btn_manual.place(x=1000,y=620)


    salir=Button(principal,text="Salir", fg="red", font=("arial", 15), borderwidth=5, cursor = "hand2",relief = "raised", command = principal.quit)
    salir.pack()
    salir.place(x=900,y=620)
    
    def cerrar():
        principal.destroy()
    
    def manual():
        try:
            # Leer el archivo del manual
            with open("manual.txt", "r", encoding="utf-8") as f:
                contenido = f.read()

            # Crear una ventana para el manual
            ventana_manual = Toplevel()
            ventana_manual.title("Manual de Usuario")
            ventana_manual.state("zoomed")  # Tamaño de la ventana

            # Crear un Text widget para mostrar el contenido del manual
            text_widget = Text(ventana_manual, wrap=WORD, font=("Arial", 12))
            text_widget.pack(expand=True, fill=BOTH)

            # Insertar el contenido del archivo en el Text widget
            text_widget.insert(END, contenido)

            # Deshabilitar la edición del contenido
            text_widget.config(state=DISABLED)

            # Agregar un botón para cerrar la ventana
            btn_cerrar = Button(ventana_manual, text="Cerrar", command=ventana_manual.destroy)
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