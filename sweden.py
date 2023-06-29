import requests
from bs4 import BeautifulSoup
import json
from flask import request

def scrape_sweden(surname):
    i = 0
    base_url = "https://www.eniro.se/"
    page = 1
    persons = []
    surname = surname = request.form['surname'].lower().strip()

    while True:
        raw_html_url = f"https://www.eniro.se/{surname}/personer/{page}"

        # Fetch the HTML content
        raw_html = requests.get(raw_html_url)
        html_content = raw_html.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract JSON data
        json_script = soup.find('script', id='__NEXT_DATA__').contents[0]
        json_data = json.loads(json_script)

        # Extract persons data from JSON
        persons_data = json_data['props']['pageProps']['initialState']['persons']

        # Iterate over each person
        for person in persons_data:
            # Extract the name and address
            name = person['name']['firstName'] + ' ' + person['name']['lastName']
            address_parts = person['addresses'][0]
            address = f"{address_parts['streetName']} {address_parts['streetNumber']}, {address_parts['postalCode']} {address_parts['postalArea']}"

            # Extract the telephone number
            telephone_number = person['phones'][0]['number'] if person['phones'] else "N/A"

            # Create the person list
            person_data = [name, address, telephone_number]
            persons.append(person_data)

        # Increment the page number
        page += 1

        # If no listings found, exit the loop
        if not persons_data:
            break

    for person in persons:
        print(i,person) 
        i+=1
    return persons