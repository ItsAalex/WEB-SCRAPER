import requests
from bs4 import BeautifulSoup
from flask import request

def scrape_austria(surname):
    base_url = "https://www.herold.at/"
    page = 1
    persons = []
    surname = request.form['surname'].lower().strip()


    while True:
        raw_html_url = f"https://www.herold.at/telefonbuch/suche/?userTerm={surname}&seite={page}"
        # Fetch the HTML content
        raw_html = requests.get(raw_html_url)
        html_content = raw_html.text
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract the listings on the current page
        listings = soup.find_all('div', class_="white-pages-search-result-item_wrap__rGC8M")
        # Iterate over each listing
        for listing in listings:
            name_element = listing.find('h2', class_="white-pages-search-result-item_heading__1BDNn")
            name = name_element.text.strip() if name_element else "N/A"
            address_element = listing.find('p', class_="white-pages-search-result-item_paragraph__2yKbl")
            address = address_element.text.strip() if address_element else "N/A"
            
            # Find all div elements with the specified class
            div_elements = listing.find_all("div", class_="white-pages-search-result-item_button_wrapper__22Y1P")
            # Initialize telephone as "N/A"
            telephone = "N/A"
            # Iterate over the div elements
            for div_element in div_elements:
                # Find the <a> tag within the div element
                a_tag = div_element.find('a', {'data-yxt': 'phn'})
                # Extract the title attribute
                if a_tag:
                    telephone = a_tag.get('title')
                    break
            
            # Create the person list
            person = [name, address, telephone]
            # Append the person list to the persons list
            persons.append(person)
        
        # Increment the page number
        page += 1
        
        # If no listings found, exit the loop
        if not listings:
            break
        for person in persons:
            print(person)
    return persons
