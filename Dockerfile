FROM python:3.10.6-slim

WORKDIR /docker

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 5432

COPY . .
