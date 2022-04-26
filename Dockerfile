FROM python:3.10

COPY ./src /app/src
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

WORKDIR /app/src

CMD ["python", "main.py"]