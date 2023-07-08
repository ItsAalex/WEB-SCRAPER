FROM python:3.8

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y wget gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

RUN mkdir /app/downloads

COPY chromedriver ./chromedriver

RUN chmod +x ./chromedriver

CMD ["python3", "app.py"]
