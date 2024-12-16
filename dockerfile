FROM python:3.8-buster

ENV PYTHONBUFFERED=1

WORKDIR /django

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn Library.wsgi:application --bind 0.0.0.0:8000


EXPOSE 8000
