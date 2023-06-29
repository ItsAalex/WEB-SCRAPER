from bs4 import BeautifulSoup
from flask import request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_france(surname):
    surname = surname = request.form['surname'].lower().strip()

    raw_html_url = f"https://annuaire.118712.fr/?s={surname}"
    base_url = "https://www.118712.fr/"

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get(f'https://annuaire.118712.fr/?s={surname}')
    # Locate and click the "Load More" button
    load_more_button = driver.find_element(By.CLASS_NAME, "bannerButton")#.click
    # Scrolling the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load after scrolling
        time.sleep(5)
        if load_more_button is None:
            time.sleep(0)
        else:
            load_more_button = driver.find_element(By.CLASS_NAME, "bannerButton")#.click
            new_height = driver.execute_script("return document.body.scrollHeight")
            
        if new_height == last_height:
            break
        last_height = new_height
        html_content = driver.page_source


    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create an empty list to store persons
    persons = []

    # Extract the listings on the current page
    listings = soup.find_all('div', class_='item-content')

    # Iterate over each listing
    for listing in listings:
        # Extract the name, address, and telephone
        name_element = listing.find('h2', class_='titre')
        name = name_element.text.strip()

        address_element = listing.find('span', class_='streetAddress')
        if address_element:
            address = address_element.text.strip()
        else:
            address = "N/A"

        telephone_element = listing.find('span', class_='button_wording')
        if telephone_element != None:
            telephone = telephone_element.text.strip()
        else:
            telephone = 'N/A'

        # Create the person list
        person = [name, address, telephone]

        # Append the person list to the persons list
        persons.append(person)
    driver.quit()
    return persons
