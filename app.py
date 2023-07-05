from flask import render_template, Flask, request, send_from_directory
import pandas as pd
import os
from canada import scrape_canada
from austria import scrape_austria
from italia import scrape_italia
from france import scrape_france
from norway import scrape_norway
from sweden import scrape_sweden
from belgium import scrape_belgium
from danish import scrape_danish
from switz import scrape_switz
from germany import scrape_germany

app = Flask(__name__)

# Define the directory for saving files
#UPLOAD_FOLDER = os.path.join(app.root_path, '/app/downloads')
UPLOAD_FOLDER = '/app/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        'switz': scrape_switz,
        'france': scrape_france,
        'sweden': scrape_sweden,
        'norway': scrape_norway,
        'germany': scrape_germany
    }
    if website in scraping_functions:
        scrape_func = scraping_functions[website]
        persons = scrape_func(surname)
        excel_file = generate_excel(persons, surname, website)
        return send_from_directory(app.config['UPLOAD_FOLDER'], excel_file, as_attachment=True)
    return "Website not supported"


def generate_excel(data, surname, website):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    excel_file = f'{surname}_{website}.xlsx'
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.lstrip('/'))
    df = pd.DataFrame(data, columns=['Name', 'Address', 'Telephone'])
    df.to_excel(excel_path, index=False)

    print(f"Excel file generated at path: {excel_path}")
    return excel_file


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)