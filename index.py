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
        frame.grid(row = 0, column=0, columnspan=3, pady = 20)

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
        self.message.grid(row=3, column=0, columnspan=2, sticky= W + E)

        #tabla
        self.tree = ttk.Treeview(height=10, columns=3)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text = 'Name', anchor=CENTER)
        self.tree.heading('#1', text = 'Price', anchor=CENTER)
        self.tree.heading('#2', text = 'Quantity', anchor=CENTER)

        #botones
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='UPDATE', command=self.edit_product).grid(row=5, column=1, sticky=W + E)

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
            self.tree.insert('', 0, text = row[1], values=row[2])
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)

        else:
            self.message['text'] = 'Name and Price are required'

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
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
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
        old_price = self.tree.item(self.tree.selection())['values'][0]

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

        #boton de actualizar
        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=4)

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name,new_price,name,old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} update successfully'.format(name) 
        self.get_products()



if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()