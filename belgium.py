import requests
import re
from flask import request
from bs4 import BeautifulSoup

def scrape_belgium(surname):
    base_url = "https://www.pagesblanches.be/"
    page = 1
    persons = []
    surname = surname = request.form['surname'].lower().strip()

    while True:
        raw_html_url = f"https://www.pagesblanches.be/chercher/personne/{surname}/-/{page}/"
        
        # Fetch the HTML content
        raw_html = requests.get(raw_html_url)
        html_content = raw_html.text
        
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the listings on the current page
        listings = soup.find_all('div', class_="wg-results-list__item")
        
        # Iterate over each listing
        for listing in listings:
            # Extract the name, address, and telephone
            name_element = listing.find('a', class_="t-c")
            name = name_element.text.strip() if name_element else "N/A"
        
            address_element = listing.find('span', class_="wg-address")
            address = address_element.text.strip() if address_element else "N/A"
        
            phone_data = listing['data-small-result']
            phone_number = re.search(r'"phone":"([\d\s]+)"', phone_data)
            telephone = phone_number.group(1).replace(" ", "") if phone_number else "N/A"
        
            # Create the person list
            person = [name, address, telephone]
        
            # Append the person list to the persons list
            persons.append(person)
        
        # Increment the page number
        page += 1
        
        # If no listings found, exit the loop
        if not listings:
            break
    return persons
