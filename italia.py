from bs4 import BeautifulSoup
import requests
from flask import request

def scrape_italia(surname):
    base_url = "https://www.paginebianche.it/"
    page = 1
    persons = []
    surname = surname = request.form['surname'].lower().strip()

    while True:
        
        raw_html_url = f"https://www.paginebianche.it/persone?qs={surname}&p={page}"
        
        raw_html = requests.get(raw_html_url)
        html_content = raw_html.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        
        listings = soup.find_all('div', class_="list-element__content")
        
        for listing in listings:

            name_element = listing.find('h2', class_="list-element__title ln-3 org fn")
            name = name_element.text.strip() if name_element else "N/A"
        
            address_element = listing.find('div', class_="list-element__address adr")
            address = address_element.text.strip() if address_element else "N/A"
        
            telephone_element = listing.find('div', class_="btn__label tel")
            telephone = telephone_element.text.strip() if telephone_element else "N/A"
        
            person = [name, address, telephone]
        
            persons.append(person)

        page += 1

        if not listings:
            break
        
    return persons
