#ggg
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the Commonwealth Bank Wikipedia page
commbank_url = "https://en.wikipedia.org/wiki/Commonwealth_Bank"

# Scrape the image using BeautifulSoup
response = requests.get(commbank_url)
# Scrape tables using pandas
tables = pd.read_html(commbank_url)

# Assuming you want the second table on the page
if len(tables) > 1:
    commbank_table = tables[3]  # Select the second table (index 1)
    print("Second Table:")
    print(commbank_table.head())

    # Save the table as a CSV file
    commbank_table.to_csv("commbank_table.csv", index=False)
    print("Second table saved as commbank_table.csv")

    # Save the table as an Excel file
    commbank_table.to_excel("commbank_table.xlsx", index=False)
    print("Second table saved as commbank_table.xlsx")
else:
    print("The page does not contain a second table.")