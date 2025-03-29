#ggg
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the Commonwealth Bank Wikipedia page
commbank_url = "https://en.wikipedia.org/wiki/Commonwealth_Bank"

# Scrape the image using BeautifulSoup
response = requests.get(commbank_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the first image in the infobox (usually the logo or key image)
infobox = soup.find("table", {"class": "infobox"})
if infobox:
    image_tag = infobox.find("img")
    if image_tag:
        image_url = "https:" + image_tag["src"]
        print("Image URL:", image_url)

        # Download the image (optional)
        image_response = requests.get(image_url)
        with open("commbank_logo.png", "wb") as file:
            file.write(image_response.content)
        print("Image saved as commbank_logo.png")
    else:
        print("No image found in the infobox.")
else:
    print("No infobox found on the page.")