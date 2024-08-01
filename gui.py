import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

class InputForm(tk.Tk):

    def __init__(self):
        self.slices = []
        self.material_width = 0
        self.material_height = 0

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

        label_1 = tk.Label(self, text="Slice Width:", font=label_font)
        label_2 = tk.Label(self, text="Slice Height:", font=label_font)
        label_3 = tk.Label(self, text="Rectangle Width:", font=label_font)
        label_4 = tk.Label(self, text="Rectangle Height:", font=label_font)

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

        self.tree = ttk.Treeview(self, columns=("Slice Width", "Slice Height"), show="headings")
        self.tree.column("Slice Width", width=100, anchor='center')
        self.tree.heading("Slice Width", text="Slice Width")
        self.tree.column("Slice Height", width=100, anchor='center')
        self.tree.heading("Slice Height", text="Slice Height")
        self.tree.place(x=20, y=20, width=200, height=200)

        myfont = tk.font.Font(family='Arial', size=10, weight='bold')

        self.button1 = tk.Button(self, text="Add Slice", font=myfont, command=self.add_to_table)
        self.button1.place(x=250, y=150, width=130, height=35)

        self.button2 = tk.Button(self, text="Start Program", font=myfont, command=self.start_program)
        self.button2.place(x=20, y=380, width=130, height=35)

    def validate(self, P):
        if P.isdigit():
            return True
        else:
            self.bell()
            return False

    def add_to_table(self):
        slice_width = self.input_1.get()
        slice_height = self.input_2.get()

        if slice_width.isdigit() and slice_height.isdigit():
            self.tree.insert("", "end", values=(slice_width, slice_height))
            self.slices.append([slice_width, slice_height])
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')
        else:
            messagebox.showerror("Error", "You can only enter numbers!")
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')

    def start_program(self):
        material_width = self.input_3.get()
        material_height = self.input_4.get()

        if material_width.isdigit() and material_height.isdigit() and len(self.slices) != 0:
            self.material_width = material_width
            self.material_height = material_height
            self.destroy()
        else:
            messagebox.showerror("Error", "You can only enter numbers!")
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')


if __name__ == "__main__":
    form = InputForm()
    form.mainloop()

    print(form.slices)
    print(form.material_width)
    print(form.material_height)
