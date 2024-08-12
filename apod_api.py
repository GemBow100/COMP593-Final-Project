'''
Team: Joelle Waugh, Manuel Manrique Lopez, Ricardo Rubin, Sadia Shoily
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests
import json 
import apod_desktop
import hashlib
import re

APOD_DESKTOP_KEY = 'kedWME7bEfDhDgCTCo17gedoZxZI1Wm14UQyBJqi'

APOD_DESKTOP_URL = 'https://api.nasa.gov/planetary/apod'
def main():
    # TODO: Add code to test the functions in this module

    date = apod_desktop.get_apod_date()

    get_apod_info(date)

def cleanTitle(v_title):
    # {REQ-18, part 1}
    v_aux=v_title.strip()           # Leading and trailing spaces are removed
    v_aux2=v_aux.replace(' ', '_')  # Inner spaces are replaced by '_'
    # Use a regular expression, obtein lettters, numbers and '_'
    v_titleaux = re.findall(r'[a-zA-Z_0-9]+', v_aux2)   
    v_Title=""
    for titles in v_titleaux:
        v_Title += titles
    

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # TODO: Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 

    params = {'date': apod_date, 'thumbs': True, 'api_key': APOD_DESKTOP_KEY}

    respmsg = requests.get(APOD_DESKTOP_URL, params=params)

    print(f"Recieving {apod_date} and information from NASA.", end = " ")

    if respmsg.status_code == requests.codes.ok:
        print(f"Successful!")

        dict_apod_info =json.loads(respmsg.content)

        title = dict_apod_info['title'].title()

        print(f"Title : {title}")
    return dict_apod_info

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # TODO: Complete the function body
    # Hint: The APOD info dictionary includes a key named 'media_type' that indicates whether the APOD is an image or video
    v_date ="2023-15-27"
    #url = NASA_API_URL + v_date
    url = APOD_DESKTOP_URL
    resp_msg = requests.get(url, params= params)

    print (resp_msg.url)
    if resp_msg.status_code == requests.codes.ok:
           results = resp_msg.json()
           print(results)
           print(f"titulo:{results['title']}")
           url2 = results["url"]
           # Check if is an image
           print(results["media_type"])
           if results["media_type"] == "image":
               with open("nasa_apod.jpg", "wb") as f:
                   f.write(requests.get(url2).content)
           else:
               # Extract binay content from response message body
               file_content = resp_msg.content
               image_hash = hashlib.sha256(file_content).hexdigest
               print("SE TIENE EL HAS256 DEL VIDEO") 
               print(image_hash)
               print (url2)
    else:
        print("No se pudo obtener el archivo")
        
    return (results)


    

if __name__ == '__main__':
    main()