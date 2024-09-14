import tkinter as tk


window=tk.Tk()
#window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
window.title("Tracktive")
window.iconbitmap("assets/tracktivedark.ico")
window['bg'] = "#36454f"
window.state('zoomed')


window.mainloop()
