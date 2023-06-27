from flask import render_template, send_file, Flask, request
import pandas as pd
#from bs4 import BeautifulSoup
from canada import scrape_canada
from austria import  scrape_austria
from italia import scrape_italia
from belgium import scrape_belgium
from danish import scrape_danish
from switz import scrape_switz

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('search.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    surname = request.form['surname']
    website = request.form['website']
    scraping_functions = {
        'canada': scrape_canada,
        'austria': scrape_austria,
        'italia': scrape_italia,
        'belgium': scrape_belgium,
        'danish': scrape_danish,
        'switz': scrape_switz
    }
    if website in scraping_functions:
        scrape_func = scraping_functions[website]
        persons = scrape_func(surname)
        excel_file = generate_excel(persons)
        return f'<a href="/download/{excel_file}" download>Download Excel</a>'
    return "Website not supported"

def generate_excel(data):
    df = pd.DataFrame(data, columns=['Name', 'Address', 'Telephone'])
    excel_file = 'scraped_data.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Excel file generated at path: {excel_file}")
    return excel_file


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)