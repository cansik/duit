import tkinter
import tkinter as tk

import customtkinter
from customtkinter import CTkLabel, CTkScrollableFrame

from duit.ui.tk.widgets.CTkCollapsable import CTkCollapsable

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")


def button_function():
    print("button pressed")
    from tkinter import filedialog
    filedialog.askdirectory()


frame = CTkScrollableFrame(master=app)
frame.pack(fill=tk.BOTH, expand=True)

# use collapsable tkinter subpanel
panel = CTkCollapsable(master=frame, text="Group 1")
panel.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=panel.frame, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# use collapsable tkinter subpanel
panel = CTkCollapsable(master=frame, text="Group 2")
panel.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=panel.frame, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

for i in range(10):
    CTkLabel(panel.frame, text='Bar' + str(i)).pack()

for i in range(10):
    CTkLabel(frame, text='Bar' + str(i)).pack()

app.mainloop()
