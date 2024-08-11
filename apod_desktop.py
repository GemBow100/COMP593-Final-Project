""" 
Team: Joelle Waugh, Manuel Manrique Lopez, Ricardo Rubin, Sadia Shoily
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import sys
import sqlite3
import hashlib
import requests

# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')
APOD_DESKTOP_KEY = 'kedWME7bEfDhDgCTCo17gedoZxZI1Wm14UQyBJqi'
APOD_DESKTOP_URL = 'https://api.nasa.gov/planetary/apod'

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    
    print(apod_date)

    # Initialize the image cache
    init_apod_cache()

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    date_today = date.today()
    if len(sys.argv) >= 2:
        value = sys.argv[1]
        try :
            apod_date = date.fromisoformat(value)
            if apod_date > date_today:
                print("Please enter a date that is more recent.") # TODO: Proper Error Message
                sys.exit(1)
            elif apod_date < date.fromisoformat("1995-06-16"):
                print("Please enter a date that is before 1995-06-16.") # TODO: Proper Error Message
                sys.exit(1)
            else:
                return apod_date
        except:
            print("Please enter a valid date.") # TODO: Proper Error Message
            sys.exit(1)
    else:
        return date_today
    

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already 
    if not os.path.isfile(image_cache_dir):
        os.makedirs(image_cache_dir)

    # TODO: Create the DB if it does not already exist/fix
    if not os.path.isfile(image_cache_db):
    
        con = sqlite3.connect('image_cache.db')
        cur = con.cursor
        image_query = """
    CREATE TABLE IS NOT EXIST IMAGE
    (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,
        explanation TEXT NOT NULL,
        file_path   TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    );
"""
    cur.excute(image_query)
    con.commit()
    con.close()


    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    # Hint: Use a function from apod_api.py
    apod_api = get_apod_info(apod_date)

    # TODO: Download the APOD image
    # Hint: Use a function from image_lib.py 
    apod_image = image_lib(apod_api)
    # TODO: Check whether the APOD already exists in the image cache
    # Hint: Use the get_apod_id_from_db() function below
    image_lib.download_image(apod_api)
    # TODO: Save the APOD file to the image cache directory
    # Hint: Use the determine_apod_file_path() function below to determine the image file path
    # Hint: Use a function from image_lib.py to save the image file

    # TODO: Add the APOD information to the DB
    # Hint: Use the add_apod_to_db() function below
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body
    post_params = {'api_dev_key': APOD_DESKTOP_KEY,
                   'api_option': 'paste' ,
                   'api_paste_code': explanation,
                   'api_paste_name': title,
                   'api_paste_private' : 0 if listed else 1,
                   'api_paste_expire_date': expiration}
    
    resp_msg =requests.post(, data= post_params)
    #check is paste was created successful
    if resp_msg.status_code == requests.codes.ok:
        print("Success!")
    else:
        print(f"Failure in creating paste!")
        print(f'Status code: {resp_msg.status_code} ({resp_msg.reason})')

    return resp_msg.text
    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    image_hash =hashlib.sha256(image_sha256).hexdigest()
    print(image_hash) 
    if image_sha256 == image_hash:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.
    url = f"https://apod.nasa.gov/apod/image/2408/Rhemann799_109P_24_11_92.jpg"
    image_tile = "Periodic Comet Swift-Tuttle"
    image_path = r'C:\temp\APOD\"Periodic Comet Swift-Tuttle.jpg'
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        file_content =resp_msg.content
    
        
    return file_content
    return

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    con = sqlite3.connect('image_cache.db')
    cur = con.cursor
    image_query = """
    CREATE TABLE IS NOT EXIST IMAGE
    (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,
        explanation TEXT NOT NULL,
        file_path   TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    );
"""
    cur.excute(image_query)
    con.commit()
    con.close()

    #con = sqlite3.connect('social_network.db')
    #cur = con.cursor()

    #add_person_query = """
        INSERT INTO people
        (
            name,
            email,
            address,
            city,
            province,
            bio,
            age,
            created_at,
            updated_at
        )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """


    # TODO: Put information into a dictionary
    apod_info = {
        'title': "Periodic Comet Swift-Tuttle" , 
        'explanation': 'A Halley-type comet with an orbital period of about 133 years, Comet 109P/Swift-Tuttle is recognized as the parent of the annual Perseid Meteor Shower. The comet's last visit to the inner Solar System was in 1992. Then, it did not become easily visible to the naked eye, but it did become bright enough to see from most locations with binoculars and small telescopes. This stunning color image of Swift-Tuttle's greenish coma, long ion tail and dust tail was recorded using film on November 24, 1992. That was about 16 days after the large periodic comet's closest approach to Earth. Comet Swift-Tuttle is expected to next make an impressive appearance in night skies in 2126. Meanwhile, dusty cometary debris left along the orbit of Swift-Tuttle will continue to be swept up creating planet Earth''s best-known July and August meteor shower.' ,
        'file_path': 'TBD',
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()