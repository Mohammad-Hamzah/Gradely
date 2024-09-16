import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)



class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("720x720+150+50")
        self.title("Tracktive")
        self.iconbitmap('assets/tracktivedark.ico')
        ctk.set_appearance_mode("dark")

        self.grid_rowconfigure((0,1,2,3,4), weight=1) 
        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=2,rowspan=2, column=1,columnspan=5, sticky="nsew")

        image = ctk.CTkImage(dark_image=Image.open('assets/tracktivedark.png'), size=(150, 150))

        self.logo = ctk.CTkLabel(self, image=image,text="")
        self.logo.grid(row=1, column=1)

        self.text = ctk.CTkLabel(self, text="Tracktive",font=('Georgia',100),text_color='#3ef1f3')
        self.text.grid(row=1,column=2,columnspan=3)


window = Window()
window.mainloop()