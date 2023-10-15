<h1 align="center">Итоговый проект курса: "Разработка
на Python"</h1> 

Шаблон, который я использую, выглядит следующим образом:<br>
<code>class App(tk.Frame):<br>
        def __init__(self, root):<br>
        super().__init__(root)<br>
        <your widgets go here><br>

if name == "main":<br>
    root = tk.Tk()<br>
    app = App(root)<br>
    app.pack(fill="both", expand=True)<br>
    root.mainloop()<code>
