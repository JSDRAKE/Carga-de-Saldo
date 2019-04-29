from tkinter import *
from tkinter import messagebox
import sqlite3


root=Tk()
root.geometry("400x400")

#---------- Funciones ---------


#---------- Conexion BBDD -------

def conexionBBDD():

	miConexion=sqlite3.connect("Cargas")

	miCursor=miConexion.cursor()

	try:

		miCursor.execute(''' 
			CREATE TABLE CARGAS (
			NUMERO INTEGER,
			COMPAÑIA VARCHAR (20),
			MONTO INTEGER,
			CARGADA VARCHAR (10))
			''')

		messagebox.showinfo("BBDD", "Base de datos creada con éxito")

	except:

		messagebox.showwarning("Atención!!!", "La base de datos ya existe")

#--------- POP-UP --------


def infoAdicional():

	messagebox.showinfo("Gestión de cargas de saldo", "Programa para gestion de cargas de Saldo Virtual")

def avisoLicencia():

	messagebox.showwarning("Licencia", "producto bajo licencia GNU")


def salirAplicacion():

	#valor=messagebox.askquestion("Salir", "¿Deseas salir de la aplciacion?")
	valor=messagebox.askokcancel("Salir", "¿Deseas salir de la aplciacion?")


	if valor==True:

		root.destroy()

#--------- Ingreso a BBDD --------

def opcionEstado():

	if varOpcion.get()==1:


		printestadoCarga=("SI")

	else:

		estadoCarga="NO"



def ingresar():

	miConexion=sqlite3.connect("Cargas")

	miCursor=miConexion.cursor()

	datos=numero.get(), compañia.get(),monto.get(), varOpcion.get()

	miCursor.execute("INSERT INTO CARGAS VALUES (?,?,?,?)", (datos))

	miConexion.commit()

	messagebox.showinfo("Agregado correctamente", "Se agrego correctamente la carga")

def actualizar():

	pass

#---------- Seleccion de Empresa ----------



#---------- Frame ---------

miFrame=Frame(root, width=1200, height=800)
miFrame.pack()

#---------- Menus ----------

barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)

archivoMenu=Menu(barraMenu, tearoff=0)

archivoMenu.add_command(label="Nuevo", command=conexionBBDD)
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir", command=salirAplicacion)

archivoEdicion=Menu(barraMenu, tearoff=0)

archivoEdicion.add_command(label="Copiar")
archivoEdicion.add_command(label="Cortar")
archivoEdicion.add_command(label="Pegar")

archivoAyuda=Menu(barraMenu, tearoff=0)

archivoAyuda.add_command(label="Licencia", command=avisoLicencia)
archivoAyuda.add_command(label="Acerca de....", command=infoAdicional)


barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
	
barraMenu.add_cascade(label="Edicion", menu=archivoEdicion)

barraMenu.add_cascade(label="Ayuda", menu=archivoAyuda)

#--------- Entry's ---------
numero=StringVar()
monto=StringVar()
compañia=StringVar()
varOpcion=StringVar()


cuadroNumero=Entry(miFrame, textvariable=numero)
cuadroNumero.grid(row=0, column=1, padx=10,pady=10)

cuadroCompañia=Entry(miFrame, textvariable=compañia)
cuadroCompañia.grid(row=1, column=1, padx=10,pady=10)

cuadroMonto=Entry(miFrame, textvariable=monto)
cuadroMonto.grid(row=2, column=1, padx=10,pady=10)

Label(root, text="Listo?").pack()

Radiobutton(root, variable=varOpcion, text="Cargada", value="SI", command=opcionEstado).pack()

Radiobutton(root, variable=varOpcion, text="Falta Cargar", value="NO", command=opcionEstado).pack()

etiqueta=Label(root)
etiqueta.pack()




#---------- Etiquetas ---------

numeroLabel=Label(miFrame, text="Numero")
numeroLabel.grid(row=0, column=0, padx=10, pady=10, sticky="e")

companiaLabel=Label(miFrame, text="Compañia")
companiaLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")

montoLabel=Label(miFrame, text="Monto")
montoLabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")


botonEnvio=Button(root, text="Enviar", command=ingresar)
botonEnvio.pack()

botonActualizar=Button(root, text="Actualizar", command=actualizar)
botonActualizar.pack()



#---------- Segundo Frame ----------


root.mainloop()