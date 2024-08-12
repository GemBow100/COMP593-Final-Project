
import apod_desktop
# Import apod_api
import apod_api
# import image_lib
import image_lib
# Import 
from tkinter import *
from tkinter import ttk
import ctypes
# pillow
from PIL import Image, ImageTk
# tkcalendar
from tkcalendar import DateEntry
# requests
import requests
#import hashlib
import hashlib


# Initialize the image cache
apod_desktop.init_apod_cache()

#Create the GUI
root = Tk()
root.title("APOD Viewer")


#Creating frames for the GUI


#frame for image (top frame)
root.columnconfigure(0,weight=2)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
    
    
image_frame = ttk.Frame(root)

image_frame.grid(row=0, column=0, columnspan=2)

#top frame widget


#frame for title and  (middle frame)
middle_frame = Label(root, text="") #This will need to be pulled from the API
middle_frame.grid(row=1, column=0)

#frame for cached image and set button (bottom left frame)
bottom_left_frame = LabelFrame(root, text="View Cached Image")
bottom_left_frame.grid(row=1, column=0, padx=10, pady=10)

#frame for date entry and get download image button (bottom right frame)
bottom_right_frame = LabelFrame(root, text="Get More Images")
bottom_right_frame.grid(row=1, column=1, padx=100)

#Set Icon
iconID = 'COMP593.APODViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(iconID)
root.iconbitmap('nasa.ico')

#Set default picture
openIMG = Image.open("moonwalking.jpg")
img = ImageTk.PhotoImage(openIMG)
# Add it to the label
label = Label(image_frame, image=img)
label.grid()


# Get all images from cache
allImages = apod_desktop.get_all_apod_titles()
#Select Image Label
selImgLbl = Label(bottom_left_frame, text="Select Image:")
selImgLbl.grid()
#Select Image drop down
selImgcmbx = ttk.Combobox(bottom_left_frame, values=allImages)
selImgcmbx.set("Select an Image")
selImgcmbx.grid(padx=(10,3))

# Set as desktop
def setAsDesktop():
    # Get from the combo box
    selectedValue = selImgcmbx.get()
    # Run show iMage
    show_image()
    # Run set as destkop
    image_lib.set_desktop_background_image(f"images/{selectedValue}")


#Set as Desktop button
setDskBtn = Button(bottom_left_frame, text="Set as Desktop")
setDskBtn.grid(row=1,column=1, padx=10, pady=10)

#Select Date Label
selDateLbl = Label(bottom_right_frame, text="Select Date:")
selDateLbl.grid(padx=20, pady=2)

# Calendar Date Picker 
cal = DateEntry(bottom_right_frame, date_pattern="yyyy-mm-dd")
cal.grid()

# Set Button click
setDskBtn.config(command=setAsDesktop)
#show image preview in top frame when date is selected
def show_image(date=cal.get_date()):
    # get the date
    date = cal.get_date()
    # Destroy the window
    root.destroy()
    # Add to the cache
    apod_desktop.add_apod_to_cache(date)
    # Get the info
    apod_info = apod_api.get_apod_info(date)
    # Get the url
    image_url = apod_info["url"]
    # Get image data
    image_data = image_lib.download_image(image_url)
    image_lib.set_desktop_background_image("APODPic.jpg")
    # Save it 
    image_lib.save_image_file(image_data, "APODPic.jpg")
    # add to cache
    apod_desktop.add_apod_to_cache(date)
    
    # GET message
    respMsg = requests.get(apod_api.get_apod_image_url(apod_info))
    
    # Check if download was successful
    if respMsg.status_code == requests.codes.ok:
        # Extract binary data
        content = respMsg.content
        # Hash
        hashValue = hashlib.sha256(content).hexdigest()
    # Add to database
    apod_desktop.add_apod_to_db(title=apod_info['title'],sha256=hashValue, file_path="APODPic.jpg", explanation=apod_info["explanation"])
    # Create new window
    #Create the GUI and set geometry
    newRoot = Tk()
    newRoot.title("APOD Viewer")

    #frame for image (top frame)
    newRoot.columnconfigure(0,weight=2)
    newRoot.columnconfigure(1,weight=1)
    newRoot.columnconfigure(2,weight=1)
    newRoot.rowconfigure(0,weight=1)
    newRoot.rowconfigure(1,weight=1)
    newRoot.rowconfigure(2,weight=1)
    
    # top frame
    image_frame = ttk.Frame(newRoot)
    image_frame.grid(row=0, column=0, columnspan=3)

    #frame for title and date (middle frame)
    middle_frame = Label(newRoot, text="") #This will need to be pulled from the API
    middle_frame.grid(row=1, column=0,columnspan=3, padx=10, pady=10)

    #frame for cached image and set button (bottom left frame)
    bottom_left_frame = LabelFrame(newRoot, text="View Cached Image")
    bottom_left_frame.grid(row=2, column=0, padx=10, pady=10)

    #frame for date entry and get download image button (bottom right frame)
    bottom_right_frame = LabelFrame(newRoot, text="Get More Images")
    bottom_right_frame.grid(row=2, column=2, padx=100)

    #Set Icon
    iconID = 'COMP593.APODViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(iconID)
    newRoot.iconbitmap('nasa.ico')

    #Select Image Label
    selImgLbl = Label(bottom_left_frame, text="Select Image:")
    selImgLbl.grid()
    #Select Image drop down
    selImgcmbx = ttk.Combobox(bottom_left_frame)
    selImgcmbx.grid(padx=(10,3))
    #Set as Desktop button
    setDskBtn = Button(bottom_left_frame, text="Set as Desktop")
    setDskBtn.grid(row=1,column=1, padx=10, pady=10)

    #Select Date Label
    selDateLbl = Label(bottom_right_frame, text="Select Date:")
    selDateLbl.grid(padx=20, pady=2)

    # Calendar Date Picker 
    calendar = DateEntry(bottom_right_frame, date_pattern="yyyy-mm-dd")
    calendar.grid()

    # TODO: Download Image Button
    dwnldImgBtn = Button(bottom_right_frame, text="Download Image")
    dwnldImgBtn.grid(row=1, column=1, padx=10, pady=10)
    
    # get description
    description = apod_info["explanation"]
    # Description Text
    desTxt = Label(middle_frame, text=description, wraplength=1100, height=6)
    desTxt.pack(anchor=CENTER)
    
    #Change picture
    openImage = Image.open("APODPic.jpg")
    resize_image = openImage.resize((500, 500))
    image = ImageTk.PhotoImage(resize_image)
    
    # Add it to the label
    imageLabel = Label(image_frame, image=image)
    imageLabel.image = image
    imageLabel.grid()

    return 

# TODO: Download Image Button
dwnldImgBtn = Button(bottom_right_frame, text="Download Image")
dwnldImgBtn.grid(row=1, column=1, padx=10, pady=10)
dwnldImgBtn.config(command=show_image)

root.mainloop()

root.mainloop()