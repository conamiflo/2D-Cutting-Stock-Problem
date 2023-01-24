import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox


class InputForm(tk.Tk):

    def __init__(self):

        self.isecci = []
        self.sirina_materijala = 0
        self.visina_materijala = 0

        super().__init__()

        self.geometry("470x450")
        self.title("Input Form")

        input_font = font.Font(size=15)
        label_font = font.Font(size=15)

        style = ttk.Style()
        style.configure("TEdge.TEntry",
                        background="white",
                        fieldbackground="white",
                        foreground="black",
                        relief="solid",
                        bordercolor="black",
                        borderwidth=2,
                        padding=5,
                        font=input_font,
                        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label_1 = tk.Label(self, text="Sirina isecka:", font=label_font)
        label_2 = tk.Label(self, text="Visina isecka:", font=label_font)
        label_3 = tk.Label(self, text="Sirina pravougaonika:", font=label_font)
        label_4 = tk.Label(self, text="Visina pravougaonika:", font=label_font)

        vcmd = (self.register(self.validate), '%P')
        self.input_1 = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.input_2 = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.input_3 = tk.Entry(self, validate="key", validatecommand=vcmd)
        self.input_4 = tk.Entry(self, validate="key", validatecommand=vcmd)

        self.input_1 = ttk.Entry(self, style="TEdge.TEntry")
        self.input_2 = ttk.Entry(self, style="TEdge.TEntry")
        self.input_3 = ttk.Entry(self, style="TEdge.TEntry")
        self.input_4 = ttk.Entry(self, style="TEdge.TEntry")

        label_1.place(x=250, y=20)
        self.input_1.place(x=250, y=50, width=150, height=25)

        label_2.place(x=250, y=80)
        self.input_2.place(x=250, y=110, width=150, height=25)

        label_3.place(x=20, y=250)
        self.input_3.place(x=20, y=280, width=170, height=25)

        label_4.place(x=20, y=310)
        self.input_4.place(x=20, y=340, width=170, height=25)

        self.tree = ttk.Treeview(self, columns=("Sirina isecka", "Visina isecka"), show="headings")
        self.tree.column("Sirina isecka", width=100, anchor='center')
        self.tree.heading("Sirina isecka", text="Sirina isecka")
        self.tree.column("Visina isecka", width=100, anchor='center')
        self.tree.heading("Visina isecka", text="Visina isecka")
        self.tree.place(x=20, y=20, width=200, height=200)

        myfont = tk.font.Font(family='Arial', size=10, weight='bold')

        self.button1 = tk.Button(self, text="Dodaj isecak", font=myfont, command=self.dodaj_u_tabelu)
        self.button1.place(x=250, y=150, width=130, height=35)

        self.button2 = tk.Button(self, text="Pokreni program", font=myfont, command=self.pokreni_program)
        self.button2.place(x=20, y=380, width=130, height=35)

    def validate(self, P):
        if P.isdigit():
            return True
        else:
            self.bell()
            return False

    def dodaj_u_tabelu(self):
        sirina_isecka = self.input_1.get()
        visina_isecka = self.input_2.get()

        if sirina_isecka.isdigit() and visina_isecka.isdigit():
            self.tree.insert("", "end", values=(sirina_isecka, visina_isecka))
            self.isecci.append([sirina_isecka, visina_isecka])
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')
        else:
            messagebox.showerror("Greska", "Mozete da unesete samo brojeve!")
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')

    def pokreni_program(self):
        sirina_materijala = self.input_3.get()
        visina_materijala = self.input_4.get()

        if sirina_materijala.isdigit() and visina_materijala.isdigit() and len(self.isecci) != 0:
            self.sirina_materijala = sirina_materijala
            self.visina_materijala = visina_materijala
            self.destroy()
        else:
            messagebox.showerror("Greska", "Mozete da unesete samo brojeve!")
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')


if __name__ == "__main__":
    form = InputForm()
    form.mainloop()

    print(form.isecci)
    print(form.sirina_materijala)
    print(form.visina_materijala)