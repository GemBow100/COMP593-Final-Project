from tkinter import *
import apod_desktop

# Initialize the image cache
apod_desktop.init_apod_cache()

# TODO: Create the GUI
root = Tk()
root.geometry('600x400')
root.minsize(500,500)
root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)


root.mainloop()