from bs4 import BeautifulSoup
import requests
from flask import request

def scrape_austria(surname):
    base_url = "https://www.dasschnelle.at/"
    page = 1
    persons = []
    surname = surname = request.form['surname'].lower().strip()
    while True:
        raw_html_url = f"https://www.dasschnelle.at/{surname}/0/{page}/typ/privat"
        
        raw_html = requests.get(raw_html_url)
        html_content = raw_html.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        listings = soup.find_all("article", class_="search-result p-3 shadow-bottom-3 mt-3")
        
        if not listings:
            break
        
        for listing in listings:
            
            name_element = listing.find("div", class_="result-head name_head")
            name = name_element.text.strip() if name_element else "N/A"
            address_element = listing.find("div", class_="adresse")
            address = address_element.text.strip() if address_element else "N/A"
            telephone_element = listing.find("p", class_="telefon")
            telephone = telephone_element.text.strip() if telephone_element else "N/A"
            
            person = [name, address, telephone]
            persons.append(person)

        page += 1

        if page > 50:
            break
    return persons
