import requests
from bs4 import BeautifulSoup
import json
from flask import request

def scrape_norway(surname):
    surname = surname = request.form['surname'].lower().strip()
    page = 1
    base_url = "https://www.gulesider.no"
    persons = []

    while True:
        raw_html_url = f"https://www.gulesider.no/{surname}/personer/{page}"

        # Fetch the HTML content
        response = requests.get(raw_html_url)
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract JSON data
        json_script = soup.find('script', id='__NEXT_DATA__').contents[0]
        json_data = json.loads(json_script)

        # Extract phone numbers and names from JSON
        persons_data = json_data['props']['pageProps']['initialState']['persons']
        for person in persons_data:
            name = person['name']['firstName'] + ' ' + person['name']['lastName']

            phone_numbers = [phone['number'] for phone in person['phones']]

            address = None

            # Append name, address, and phone numbers to the persons list
            person_data = [name, address, phone_numbers]
            persons.append(person_data)

        # Increment the page number
        page += 1

        # Check if no listings found
        if not persons_data:
            break

    # Print the persons list
    return persons