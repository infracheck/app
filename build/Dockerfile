FROM python:3.9.0b3-buster
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV FLASK_APP=infracheck
COPY . /app
WORKDIR /app
CMD flask run --host='0.0.0.0' --port=8080
