FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers=4", "--threads=2", "--bind=0.0.0.0:5000", "app:app"]
