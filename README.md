Шаблон, который я использую, выглядит следующим образом:

`class App(tk.Frame):
     def __init__(self, root):
        super().__init__(root)
        <your widgets go here>

if name == "main":
    root = tk.Tk()
    app = App(root)
    app.pack(fill="both", expand=True)
    root.mainloop()`
