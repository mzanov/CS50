# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3
WORKDIR /app
# Allows docker to cache installed dependencies between builds
COPY requirements.txt .

ENV DEBUG=False
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000


# runs the production server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]