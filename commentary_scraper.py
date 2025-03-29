def scrape_commentary():
    commentary = ""
    with open("example_files/commentary_CBA.txt", "r") as file:
        commentary = file.read()

    return commentary

    
