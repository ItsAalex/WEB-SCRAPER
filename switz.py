from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import re

def scrape_switz(surname):
    #surname = input("Enter your name")
    surname = surname = request.form['surname'].lower().strip()
    browser = webdriver.Chrome()
    browser.get(f'https://tel.search.ch/?was={surname}&privat=1&pages=1')

    items = []
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        elements = browser.find_elements(By.CSS_SELECTOR, "body > div")
        textElements = []

        # Get the final URL
        final_url = browser.current_url

        base_url = "https://www.search.ch/"
        # Fetch the HTML content
        raw_html = requests.get(final_url)
        html_content = raw_html.text
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Create an empty list to store persons
        persons = []
        # Extract the listings on the current page
        listings = soup.find_all('table', class_='tel-resultentry')
        # Iterate over each listing
        for listing in listings:
            # Extract the name, address, and telephone
            name_element = listing.find('h1')
            name = name_element.text.strip()
            address_element = listing.find('div', class_='tel-address')
            address = address_element.text.strip()
            telephone_element = listing.find('a', class_='tel-result-action')
            if telephone_element:
                telephone_href = telephone_element.get('href')
                telephone_match = re.search(r'\+(\d+)', telephone_href)
                if telephone_match:
                    telephone = telephone_match.group(1)
                else:
                    telephone = 'N/A'
            else:
                telephone = 'N/A'
            # Create the person list
            person = [name, address, telephone]
            # Append the person list to the persons list
            persons.append(person)

    browser.quit()
    
    return persons