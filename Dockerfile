FROM python:3.11-alpine

WORKDIR /code/

RUN mkdir ./mysite

COPY ./mysite/ /code/mysite
COPY ./.env /code/
COPY ./requirements.txt /code/

RUN mkdir ./mysite/static

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./mysite/manage.py", "runserver", "0.0.0.0:80"]