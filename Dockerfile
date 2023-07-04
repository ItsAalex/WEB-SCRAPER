FROM python:3.8

WORKDIR /app
ADD . /app

RUN pip install requests beautifulsoup4 flask pandas selenium openpyxl

CMD ["python3", "app.py"]
