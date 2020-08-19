FROM python:3.9-rc-buster
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["waitress-serve", "--port=8080", "infracheck:app"]
