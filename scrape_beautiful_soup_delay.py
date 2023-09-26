

import os
import time
import requests
from bs4 import BeautifulSoup

# ==========================
# PARAMETERS (Edit These)
# ==========================
URL = "https://haveibeentrained.com/?search_text=Bioluminescence%20abstract%20sculpture%20photographed%20on%20ektachrome%20damaged%20film,%20GLSL%20shader,%20music%20video%20by%20Chris%20Cunningham,%20%20featured%20on%20FFFFOUND!"
SAVE_PATH = "G:\My Drive\dataset-footage\Bioluminescence"
DELAY = 1  # Delay between each image download (in seconds)

def download_images(url, save_path, delay=1):
    """
    Download images from a specific URL and save them to a directory.

    Args:
        url (str): The URL to scrape images from.
        save_path (str): The directory to save images to.
        delay (int): The delay between requests in seconds.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for img in img_tags:
        img_url = img.get('src')
        if img_url and 'http' not in img_url:  # Check if img_url is not None and then if it's relative
            img_url = '{}{}'.format(url, img_url)
        response = requests.get(img_url, stream=True)
        with open(os.path.join(save_path, img_url.split('/')[-1]), 'wb') as out_file:
            out_file.write(response.content)
        time.sleep(delay)  # Delay in seconds

# Execute the function with the parameters specified above
download_images(URL, SAVE_PATH, DELAY)
