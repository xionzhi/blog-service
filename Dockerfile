FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

ENV FLASK_APP=runserver

RUN pip install -r requirements.txt

COPY . .

CMD python -m flask run -h 0.0.0.0 -p 5001
