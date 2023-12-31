import sqlite3
import tkinter as tk
from tkinter import ttk
import re


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.widgets()
        self.db = db
        self.view_records()
        self.check = check

    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute("""SELECT * FROM employees
        WHERE name LIKE ?""", (name,))

        # удаления данных таблицы в момент поиска
        [self.tree.delete(i) for i in self.tree.get_children()]
        # вывод искомых данных
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def open_search_dialog(self):
        Search()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute("""DELETE FROM employees
            WHERE id=?""", (self.tree.set(selection_item, '#1')))
            self.db.conn.commit()
            self.view_records()

    # изменение данных сотрудника
    def update_record(self, name, tel, email):
        self.db.cur.execute("""UPDATE employees SET name=?, tel=?, email=?
        WHERE ID=?""", (name, tel, email,
                        # устанавливаем фокус на первый столбец выделенной строки (ID)
                        self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def records(self, name, tel, email):
        if check.isValidTel(tel) and check.isValidEmail(email)\
                and check.isValidName(name):
            self.db.insert_data(name, tel, email)
            self.view_records()

    def widgets(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='images/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # добавляем таблицу
        # height - высота таблицы
        # show='headings' - скрывает нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')

        # добавляем параметры колонкам
        # width - ширина
        # anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='Email')

        self.tree.pack(side=tk.LEFT)

        # кнопка изменения данных
        self.update_img = tk.PhotoImage(file='images/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # кнопка удаления записи
        self.delete_img = tk.PhotoImage(file='images/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска записи
        self.search_img = tk.PhotoImage(file='images/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # обновление данных
        self.refresh_img = tk.PhotoImage(file='images/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

    def open_dialog(self):
        Child()

    # вывод данных в виджет таблицы
    def view_records(self):
        self.db.cur.execute("""SELECT * FROM employees""")
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]


class Child(tk.Toplevel):  # Toplevel, который будет представлять собой дочернее окно
    def __init__(self):
        super().__init__(root)
        self.init_child()
        # обращаемся к классу Main
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Email')
        label_tel.place(x=50, y=80)
        label_email = tk.Label(self, text='Телефон')
        label_email.place(x=50, y=110)

        # добавлем строку ввода для ФИО
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                        self.entry_tel.get(),
                                                                        self.entry_email.get()))


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
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get()
        ))
        # закрываем окно редактирования
        # add='+' добавляет возможность 'повесить' на кнопку более одного события
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_add.destroy()

    # подгрузка данных в форму для рекдактирования
    def default_data(self):
        self.db.cur.execute("""SELECT * FROM employees WHERE id=?""",
                            (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        # получаем доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB():
    def __init__(self):
        self.conn = sqlite3.connect('Synergy.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        tel TEXT,
        email TEXT);
        """)
        self.conn.commit()

    def insert_data(self, name, tel, email):
        self.cur.execute("""INSERT INTO employees (name, tel, email) VALUES(?, ?, ?)""",
                         (name, tel, email))
        self.conn.commit()


class Check():
    def isValidName(self, name):
        pattern_name = re.compile(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?')
        if re.match(pattern_name, name):
            return True
        else:
            print('Uncorrected name')

    def isValidTel(self, number):
        pattern_tel = re.compile(r'(\+7|8).*?(\d{2,3}).*?(\d{2,3}).*?(\d{2}).*?(\d{2})')
        if re.match(pattern_tel, number):
            return True
        else:
            print('Uncorrected number')

    def isValidEmail(self, email):
        pattern_email = re.compile(r'[\w\.-]+@[\w\.-]+')
        if re.match(pattern_email, email):
            return True
        else:
            print('Uncorrected email')


if __name__ == '__main__':
    root = tk.Tk()
    check = Check()
    db = DB()
    app = Main(root)
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(width=False, height=False)
    root.mainloop()
