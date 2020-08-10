FROM python:3.9.0b3-buster
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
CMD waitress-serve --port=8080 infracheck:app
