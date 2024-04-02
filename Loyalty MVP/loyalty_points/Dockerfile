# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3
WORKDIR /app

RUN apt-get update -y && apt-get install -y tesseract-ocr

# Allows docker to cache installed dependencies between builds
COPY requirements.txt .

ENV DEBUG=False
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "migrate"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]