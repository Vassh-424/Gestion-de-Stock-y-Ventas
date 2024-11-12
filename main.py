from tkinter import *
import ventana_stock
import ventana_historial
import ventana_ventas

###############VENTANA PRINCIPAL#################

##Asegurarse de poner imagen de portada despues. Si no es posible no importa

def ventana_principal():
    principal = Tk()
    principal.state("zoomed")
    principal.title("Gestion de Stock y Ventas")
    principal.resizable(0, 0)


    titulo= Label(text="GESTION DE STOCK Y VENTAS V1",padx=10, font=("Arial", 40, "bold"))
    titulo.pack()
    titulo.place(x=60,y=50)
    
    image = PhotoImage(file="patroclo.png")

    # Crear un widget Label que mostrará la imagen
    label = Label(principal, image=image)
    label.pack()
    label.place(x=120,y=130)

    stockb=Button(principal,text="Stock", fg="blue", font=("arial", 35), borderwidth=5, cursor = "hand2",relief = "raised",  command = lambda:ventana_stock.stock())
    stockb.pack()
    stockb.place(x=900,y=150)


    ventasb=Button(principal,text="Nueva Venta", fg="blue", font=("arial", 35), state= "normal", borderwidth=5, cursor = "hand2",relief = "raised", command = lambda:ventana_ventas.ventas())
    ventasb.pack()
    ventasb.place(x=900,y=350)


    detalle_ventasb= Button(principal, text="Historial de Ventas", fg="blue", font=("arial", 35), borderwidth=5, cursor = "hand2",relief = "raised", command= lambda:ventana_historial.historial())
    detalle_ventasb.pack()
    detalle_ventasb.place(x=900,y=550)
    
    salir=Button(principal,text="Salir", fg="red", font=("arial", 20), borderwidth=5, cursor = "hand2",relief = "raised", command = principal.quit)
    salir.pack()
    salir.place(x=1500,y=800)

#########FIN DE PRORGAMA PRINCIPAL#################
    principal.mainloop()

"""
LISTA DE COSAS POR TERMINAR
*Agregar si es que se encuentra un error o se quiere agregar una nueva funcion
"""
   
if __name__ == '__main__':
    ventana_principal()