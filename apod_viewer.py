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

# TODO: Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.NasaIMageViewer')#
root.iconbitmap(os.path.join(script_dir, 'Nasa.ico'))#

# TODO: Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky= NSEW)


root.mainloop()