from bs4 import BeautifulSoup
import requests
from flask import request

def scrape_canada(surname):
    surname = surname = request.form['surname'].lower().strip()
    raw_html_url = f"https://www.canada411.ca/search/?stype=si&what={surname}&where=Canada"
    base_url = "https://www.canada411.ca/"
    # Fetch the HTML content
    raw_html = requests.get(raw_html_url)
    html_content = raw_html.text
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    persons = []
    # Extract the listings on the current page
    listings = soup.find_all('div', class_='c411Listing')
    for listing in listings:
        name_element = listing.find('h2', class_='c411ListedName')
        name = name_element.text.strip()
        address_element = listing.find('span', class_='adr')
        address = address_element.text.strip()
        telephone_element = listing.find('span', class_='c411Phone')
        telephone = telephone_element.text.strip()
        # Create the person list
        person = [name, address, telephone]
        persons.append(person)
    # Find the pagination section
    pagination = soup.find('ul', class_='c411Paging')
    next_page_url = None
    if pagination:
        next_page_element = pagination.find('li', class_='pagingNext')
        if next_page_element:
            next_page_link = next_page_element.find('a')
            if next_page_link:
                next_page_url = next_page_link.get('href')
    while next_page_url:
        next_page_html = requests.get(base_url + next_page_url).text
        next_page_soup = BeautifulSoup(next_page_html, 'html.parser')
        next_page_listings = next_page_soup.find_all('div', class_='c411Listing')
        for listing in next_page_listings:
            name_element = listing.find('h2', class_='c411ListedName')
            name = name_element.text.strip()
            address_element = listing.find('span', class_='adr')
            address = address_element.text.strip()
            telephone_element = listing.find('span', class_='c411Phone')
            telephone = telephone_element.text.strip()
            person = [name, address, telephone]
            persons.append(person)
        pagination = next_page_soup.find('ul', class_='c411Paging')
        next_page_url = None
        if pagination:
            next_page_element = pagination.find('li', class_='pagingNext')
            if next_page_element:
                next_page_link = next_page_element.find('a')
                if next_page_link:
                    next_page_url = next_page_link.get('href')
    return persons
