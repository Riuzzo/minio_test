FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "app.py"]