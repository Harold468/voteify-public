FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev


RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python manage.py collectstatic --no-input && python manage.py migrate --no-input && gunicorn voteifybackend.wsgi:application --bind 0.0.0.0:8000"]