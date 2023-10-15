import sqlite3
import tkinter as tk
from tkinter import ttk


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.widgets()

    def widgets(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='images/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # добавляем таблицу
        # columns - столбцы
        # height - высота таблицы
        # show='headings' - скрывает нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')

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

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):  # Toplevel, который будет представлять собой кастомное окно
    def __init__(self):
        super().__init__(root)

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_numb = tk.Label(self, text='Телефон')
        label_numb.place(x=50, y=80)
        label_email = tk.Label(self, text='Email')
        label_email.place(x=50, y=110)

        # добавлем строку ввода для ФИО
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_numb = ttk.Entry(self)
        self.entry_numb.place(x=200, y=110)

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy())
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_add.bind('<Button-1>')


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(width=False, height=False)
    root.mainloop()
