import sqlite3
from tkinter import *

con = sqlite3.connect("Synergy.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS  Jokes
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                joke TEXT)
            """)

"""cur.execute("INSERT INTO Jokes VALUES(?, ?);",
            (1, 'Собеседование.'
            '- У Вас есть навыки работы с DOM?'
            '- Вам строитель нужен или программист?'))

cur.execute("INSERT INTO Jokes VALUES(?, ?);", (2, 'Ребенок, воспитанный программистом, называет отчима "Новая папка"'))

cur.execute("INSERT INTO Jokes VALUES(?, ?);", (3, 'Программист умирает в 45 лет и попадает в рай. Он спрашивает у Бога, почему же он умер так рано.'
                'Бог: Сын мой, если учитывать, сколько отработанных часов ты указывал в своих отчетах, ты прожил 82 года.'),)

cur.execute("INSERT INTO Jokes VALUES(?, ?);", (4, 'Разработчики, обвиненные в написании нечитабельного кода, отказались давать комментарии'))

cur.execute("INSERT INTO Jokes VALUES(?, ?);",  (5, 'Быть программистом и смотреть, как кто-то «хакает» ноутбук в сериале, это как быть медсестрой и смотреть, как кто-то затыкает рану от пули морковкой.'))

con.commit()"""


class Refresh:

    def random_joke(self):
        self.delete(1.0, "end")
        cur.execute("SELECT joke FROM Jokes ORDER BY RANDOM() LIMIT 1;")
        result = str(cur.fetchall())
        result = result.replace('[', ' ')
        result = result.replace(']', ' ')
        result = result.replace('(', ' ')
        result = result.replace(',)', ' ')
        self.insert(1.0, result)


root = Tk()

root['bg'] = '#fafafa'
root.title('JokeGenerator')
root.geometry('500x450')

root.resizable(width=False, height=False)

frame = Frame(root, bg='#ecf96a')
frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)

frame1 = Frame(root, background='#ecf96a')
frame1.place(relx=0, rely=0.3, relwidth=1, relheight=1)

jokes = Text(frame1, height=15, wrap="word")
photo = PhotoImage(file=r"C:\Users\Admin\Desktop\synergy\newpng_white.png")
btn = Button(frame, text='Click Me !', image=photo, background='#ecf96a', command=lambda: Refresh.random_joke(jokes))
btn.pack(expand=TRUE)

jokes.pack(anchor=S, fill=X)

root.mainloop()
