FROM python:3.9-rc-buster
RUN apt-get update
RUN apt-get install sshpass
COPY requirements/build.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["waitress-serve", "--port=8080", "infracheck:app"]
