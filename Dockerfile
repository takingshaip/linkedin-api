FROM python:3.9

WORKDIR /app

COPY . .

RUN pipenv install --dev
RUN pipenv shell

CMD ["python", "-m","pytest","tests"]

