FROM python:3.8

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

RUN mkdir /app/downloads

COPY chromedriver /usr/local/bin/chromedriver

RUN chmod +x /usr/local/bin/chromedriver

CMD ["python3", "app.py"]
