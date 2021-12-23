import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
 
    def init_main(self):
        toolbar = tk.Frame(bg='#d8bfd8', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog, bg='#E6E6FA', 
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)
       
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#E6E6FA',
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
               
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#E6E6FA',
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
 
        btn_search = tk.Button(toolbar, text='Поиск', bg='#E6E6FA',
                               compound=tk.TOP, command=self.open_search_dialog)

        btn_search.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'surname', 'name', 'year'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('surname', width=250, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('year', width=115, anchor=tk.CENTER)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('surname', text='Фамилия')
        self.tree.heading('name', text='Имя')
        self.tree.heading('year', text='Год поступления')
        
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, surname, name, year):
        self.db.insert_data(surname, name, year)
        self.view_records()

    def update_record(self, surname, name, year):
        self.db.c.execute('''UPDATE Students SET surname=?, name=?, year=? WHERE ID=?''',
                          (surname, name, year, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM Students''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM Students WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, surname):
        surname = ('%' + surname + '%',)
        self.db.c.execute('''SELECT * FROM Students WHERE surname LIKE ?''', surname)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить студента')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_surname = tk.Label(self, text='Фамилия:')
        label_surname.place(x=50, y=50)
        label_name = tk.Label(self, text='Имя:')
        label_name.place(x=50, y=80)
        label_year = tk.Label(self, text='Год поступления:')
        label_year.place(x=50, y=110)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=50)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=110)

        self.entry_year = ttk.Entry(self)
        self.entry_year.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_surname.get(),
                                                                       self.entry_year.get(),
                                                                       self.entry_name.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_surname.get(),
                                                                       self.entry_year.get(),
                                                                       self.entry_name.get()))
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM Students WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_surname.insert(0, row[1])
        self.entry_year.insert(0, row[2])
        self.entry_name.insert(0, row[3])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Введите фамилию')
        label_search.place(x=3, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=110, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Students.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS Students(id integer primary key, surname text, name text, year integer)''')
        self.conn.commit()

    def insert_data(self, surname, name, year):
        self.c.execute('''INSERT INTO Students(surname, name, year) VALUES (?, ?, ?)''',
                       (surname, name, year))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Database "Students"')
    root.geometry("665x350+300+200")
    root.resizable(False, False)
    root.mainloop()
