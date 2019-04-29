from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import sqlite3

class Product:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Gestion de Recargas Virtuales')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Ingrese una nueva recarga')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Numero: ').grid(row = 1, column = 0)
        self.numero = Entry(frame)
        self.numero.focus()
        self.numero.grid(row = 1, column = 1)

        # Price Input
        Label(frame, text = 'Compañia: ').grid(row = 2, column = 0)
        self.compañia = Entry(frame)
        self.compañia.grid(row = 2, column = 1)

        # Amount Input
        Label(frame, text = 'Monto: ').grid(row = 3, column = 0)
        self.monto = Entry(frame)
        self.monto.grid(row = 3, column = 1)

        #Done INput
        Label(frame, text = 'Recargada: ').grid(row = 4, column = 0)
        self.recargada = Entry(frame)
        self.recargada.grid(row = 4, column = 1)

        # Button Add Product 
        ttk.Button(frame, text = 'Guardar Recarga', command = self.add_product).grid(row = 5, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 20, columns = ("Compañia", "Monto", "Recargada"))
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Numero', anchor = CENTER)
        self.tree.heading('Compañia', text = 'Compañia', anchor = CENTER)
        self.tree.heading('Monto', text = 'Monto', anchor = CENTER)
        self.tree.heading('Recargada', text = 'Recargada', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM product ORDER BY id ASC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2:])
            #print(row)
    # User Input Validation
    def validation(self):
        return len(self.numero.get()) != 0 and len(self.compañia.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?, ?)'
            parameters =  (self.numero.get(), self.compañia.get(), self.monto.get(), self.recargada.get() )
            self.run_query(query, parameters)
            self.message['text'] = 'Recarga {} registrada correctamente'.format(self.numero.get())
            self.numero.delete(0, END)
            self.compañia.delete(0, END)
            self.monto.delete(0, END)
            self.recargada.delete(0, END)
        else:
            self.message['text'] = 'Name and Price is Required'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona una recarga'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE numero = ?'
        self.run_query(query, (numero, ))
        self.message['text'] = 'La recarga {} se borro correctamente'.format(numero)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        #name = self.tree.item(self.tree.selection())['text']
        estadoRecarga = self.tree.item(self.tree.selection())['values'][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Actualizar Estado de la Recarga'

        # Old Price 
        Label(self.edit_wind, text = 'Recarga Actual:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = estadoRecarga), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'Recarga Nueva:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_price.get(), estadoRecarga)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_price, estadoRecarga):
        query = 'UPDATE product SET recargada = ? WHERE recargada = ?'
        parameters = (new_price, estadoRecarga)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(estadoRecarga)
        self.get_products()

if __name__ == '__main__':
    window = Tk()   
    window.resizable(0, 0)
    application = Product(window)

    def infoAdicional():

        messagebox.showinfo("Gestión de cargas de saldo", "Programa para gestion de cargas de Saldo Virtual")

    def avisoLicencia():

        messagebox.showwarning("Licencia", "producto bajo licencia GNU")


    def salirAplicacion():

        #valor=messagebox.askquestion("Salir", "¿Deseas salir de la aplciacion?")
        valor=messagebox.askokcancel("Salir", "¿Deseas salir de la aplciacion?")


        if valor==True:

            window.destroy()

    #---------- Menus ----------

    barraMenu=Menu(window)
    window.config(menu=barraMenu, width=300, height=300)

    archivoMenu=Menu(barraMenu, tearoff=0)

    archivoMenu.add_separator()
    archivoMenu.add_command(label="Salir", command=salirAplicacion)

    archivoAyuda=Menu(barraMenu, tearoff=0)

    archivoAyuda.add_command(label="Licencia", command=avisoLicencia)
    archivoAyuda.add_command(label="Acerca de....", command=infoAdicional)


    barraMenu.add_cascade(label="Archivo", menu=archivoMenu)

    barraMenu.add_cascade(label="Ayuda", menu=archivoAyuda)



    window.mainloop()
