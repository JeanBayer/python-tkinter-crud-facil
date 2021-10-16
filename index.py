from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Products Application')

        #contenedor
        frame = LabelFrame(self.wind, text = 'Register a new product')
        #grid para posicionar elementos
        frame.grid(row = 0, column=0, columnspan=4, pady = 20)

        #name input
        Label(frame, text = 'Name: ').grid(row = 1, column=0)
        self.name = Entry(frame) #Entry es para crear un input
        self.name.focus()
        self.name.grid(row = 1, column=1)

        #price input
        Label(frame, text = 'Price: ').grid( row = 2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #quantity input
        Label(frame, text= 'Quantity: ' ).grid(row = 3, column=0)
        self.quantity = Entry(frame)
        self.quantity.grid(row=3, column=1)

        #boton agregar producto
        ttk.Button(frame, text = 'Save product', command=self.add_product).grid(row=4, columnspan=2, sticky=W + E)

        #mensaje de salida
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=10, sticky= W + E)

        #tabla
        self.tree = ttk.Treeview(height=10, columns=("#1", "#2", "#3"))
        self.tree.grid(row=5, column=0, columnspan=5)
        self.tree['show'] = 'headings'
        self.tree.heading('#1', text = 'Name', anchor=CENTER)
        self.tree.heading('#2', text = 'Price', anchor=CENTER)
        self.tree.heading('#3', text = 'Quantity', anchor=CENTER)

        #botones
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=6, column=0,columnspan=2, sticky=W + E)
        ttk.Button(text='UPDATE', command=self.edit_product).grid(row=6, column=2,columnspan=2, sticky=W + E)

        #llenando las filas
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn: #conexión a bd
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        #limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #consultando los datos
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        #rellenando los datos
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values=(row[1],row[2],row[3]))
    
    def validation(self, name, price, quantity):
        return len(name.get()) != 0 and len(price.get()) != 0 and len(quantity.get()) != 0
    
    def name_exist(self, input_entry, var_comparable = ""):

        query = 'SELECT name FROM product' #hacemos la query para cargar los names
        db_prueba = self.run_query(query) #guardamos los datos de la db
        arreglo = [] #creamos un arreglo para guardar los datos

        for prueba in db_prueba:
            arreglo.extend(prueba) #asignamos los datos al arreglo

        bandera = True #bandera

        if var_comparable == "": #esta validacion es en el caso de agregar productos
            for arre in arreglo: #comparamos si el name del arreglo es igual a lo del input

                if arre == input_entry.get(): #si son iguales retornamos false
                    bandera = False 
        else:
            for arre in arreglo: #comparamos si el name del arreglo es igual a lo del input

                if arre == input_entry.get() and var_comparable != input_entry.get() : #si son iguales retornamos false
                        bandera = False 
    
        return bandera
        
    def add_product(self):    
            
        if self.validation(self.name, self.price, self.quantity):    

            if self.name_exist(self.name):

                query = 'INSERT INTO product VALUES(NULL, ?, ?, ?)'
                parameters = (self.name.get(), self.price.get(), self.quantity.get())
                self.run_query(query, parameters)
                self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
                self.name.delete(0, END)
                self.price.delete(0, END)
                self.quantity.delete(0, END)

            else:

                self.message['text'] = 'Name does exist'  

        else:
            self.message['text'] = 'Name, Price and Quantity are required'

        self.get_products()

    def delete_product(self):
        self.message['text'] = ''

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a record'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        price = self.tree.item(self.tree.selection())['values'][1]
        query = 'DELETE FROM product WHERE name = ? AND price = ?'
        self.run_query(query, (name, price))
        self.message['text'] = 'Record {} deleted succesfully'.format(name)
        self.get_products()
    
    def edit_product(self):
        self.message['text'] = ''

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a record'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][1]
        old_quantity = self.tree.item(self.tree.selection())['values'][2]

        #crear una ventana encima
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit product'

        #nombre antiguo
        Label(self.edit_wind, text='Old name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        #nombre nuevo
        Label(self.edit_wind, text='New name: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #precio viejo
        Label(self.edit_wind, text='Old price: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)

        #precio nuevo
        Label(self.edit_wind, text='New price: ').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        #cantidad vieja
        Label(self.edit_wind, text='Old quantity: ').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_quantity), state='readonly').grid(row=4, column=2)

        #cantidad nueva
        Label(self.edit_wind, text='New quantity: ').grid(row=5, column=1)
        new_quantity = Entry(self.edit_wind)
        new_quantity.grid(row=5, column=2)

        #boton de actualizar
        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name, name, new_price, old_price, new_quantity)).grid(row=7, column=1, columnspan=2, sticky= W + E)

    def edit_records(self, new_name, name, new_price, old_price, new_quantity):

        if self.validation(new_name, new_price, new_quantity): #validacion para saber que todos los campos tengan contenido

            if self.name_exist(new_name, name): #validacion para asegurar que no agregemos un nombre repetido al editar, el parametro name es para enviar como punto de comparacion
                query = 'UPDATE product SET name = ?, price = ?, quantity = ? WHERE name = ? AND price = ?'
                parameters = (new_name.get(), new_price.get(), new_quantity.get(), name, old_price)
                self.run_query(query, parameters)
                self.edit_wind.destroy()
                self.message['text'] = 'Record {} update successfully'.format(name) 
                self.get_products()
            else:
                #crear una ventana encima cuando el usuario no ingresa los campos
                self.error_wind = Toplevel()
                self.error_wind.title = 'Error product'
                Label(self.error_wind, text="Record update Un-Successfully, try again").grid(row=0, column=0)
        else:
            #crear una ventana encima cuando el usuario no ingresa los campos
            self.error_wind = Toplevel()
            self.error_wind.title = 'Error product'
            Label(self.error_wind, text="Record update Un-Successfully, try again").grid(row=0, column=0)




if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()