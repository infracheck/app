FROM python:3.9.0b3-buster
RUN apt-get -y install openssh-client
CMD ssh-keygen -q -t rsa -N '' -f /app/key/id_rsa
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV FLASK_APP=infracheck
COPY . /app
WORKDIR /app
CMD flask run --host='0.0.0.0' --port=8080
