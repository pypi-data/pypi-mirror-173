import tkinter as tk
import os
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from time import sleep
from datetime import datetime
from datetime import timedelta

update_label_after_id = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        view = View(self)
        self.title('Sirius Studio')
        self.iconbitmap('../img/base_logo.ico')
        self.iconphoto(False, tk.PhotoImage(file='../img/base_logo.png'))
        self.geometry('800x600')
        self.resizable(False, False)

        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label='Run', command=view.test_button)
        self.filemenu.add_command(label='Save', command=view.save_page)
        self.filemenu.add_command(label='Stop', command='')
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.config(menu=self.menubar)
        view.grid(row=0, column=0, padx=10, pady=10)

class View(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.timespent = timedelta(seconds=0)
        self.value = 0
        self.base_value = 0.0055555555555556

        self.label = ttk.Label(self, text='foo')
        self.label.grid(row=3, column=0, sticky=tk.W)

        self.timespent_label = ttk.Label(self, text='')
        self.timespent_label.grid(row=1, column=2)

        self.datetime_label = ttk.Label(self, text='')
        self.datetime_label.grid(row=1, column=0, sticky=tk.W)

        self.base_value_label = ttk.Label(self, text=f'Valor de base R$: {self.base_value} /s')
        self.base_value_label.grid(row=2, column=0, sticky=tk.W)


    def set_timespent_label(self):
        self.timespent_auto_increment()
        self.timespent_label['text'] = f'Tempo corrido: {self.timespent} s'

    def set_datetime_label(self):
        self.datetime_label['text'] = f'Início da contagem: {datetime.today(): %d/%m/%Y - %H:%M:%S}'

    def timespent_auto_increment(self):
        self.timespent += timedelta(seconds=1)

    def label_auto_increment(self):
        self.value += self.base_value

    def set_label_value(self):
        self.label['text'] = f'Valor Atual R$: {self.value:.10f}'

    def save_page(self):
        f = asksaveasfile(initialfile='timespent.txt', defaultextension='txt', filetypes=[("All Files", "*.*"), ("Text Document", "*.txt")])
        texto = f"Relatório de horas\n{self.datetime_label['text']}\n{self.label['text']}\n{self.timespent_label['text']}"
        f.write(f'{texto}')

    def update_label(self, cancel=False):
        global update_label_after_id
        self.label_auto_increment()
        self.set_label_value()
        self.set_timespent_label()
        if cancel is False:
            update_label_after_id = self.after(1000, self.update_label)

    def update_label_cancel(self):
        global update_label_after_id
        self.after_cancel(update_label_after_id)

    def test_button(self):
        self.set_datetime_label()
        self.update_label()



if __name__ == "__main__":
    app = App()
    app.mainloop()
