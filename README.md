# STEPS TO EXECUTE THE APP on LINUX UBUNTU

1. Install Python : On UBUNTU Python is already installed
2. Install pip: sudo apt install python3-pip
3. Install Flask: pip install flask
4. Install pandas: pip install pandas
5. Install BeautifulSoup4: pip install bs4
6. Install Selenium : pip install selenium
7. Install openpyxl : pip3 install openpyxl
8. Download webdriver and set the path for it : https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/


FROM python:3.8

WORKDIR /app
ADD . /app

RUN pip install requests beautifulsoup4 flask pandas selenium openpyxl

CMD ["python3", "app.py"]
