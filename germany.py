import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import request

def scrape_germany(surname):
    surname = surname = request.form['surname'].lower().strip()
    url = f"https://www.dastelefonbuch.de/Suche/{surname}?s=eyJvcmRlcmJ5IjoibmFtZSIsImF0IjoiMSJ9"
    response = requests.get(url)
    html_content = BeautifulSoup(response.text, 'html.parser')

    persons = []
    while True:
        results = html_content.find_all("div", class_="entry hitlistitem")
        
        if not results:
            break

        for result in results:
            name = result.find("div", class_="name")
            if name:
                name_text = name.text.strip()

            address = result.find("a", class_="addr")
            if address:
                street = address.find("span", itemprop="streetAddress")
                town = address.find("span", itemprop="addressLocality")
                if street and town:
                    address_text = street.text.strip() + " " + town.text.strip()

            telephone_1 = result.find("span", class_="nr")
            telephone_2 = telephone_1.next_sibling

            if telephone_1 and telephone_2:
                telephone_text = (telephone_1.text.strip() + telephone_2.text.strip()).replace("...", "").replace("\xa0", "")

            persons.append([name_text, address_text, telephone_text])

        next_link = html_content.find("a", class_="next")
        if next_link:
            next_url = next_link["href"]
            response = requests.get(next_url)
            html_content = BeautifulSoup(response.text, 'html.parser')
        else:
            break
        
        return persons