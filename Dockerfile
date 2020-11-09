FROM python:3.6

ADD . /djangoapp
WORKDIR /djangoapp

RUN pip install -r requirements.txt

EXPOSE 8000

CMD exec gunicorn imagedatabase.wsgi:application --bind 0.0.0.0:8000 --workers 3
