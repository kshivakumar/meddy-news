FROM python:3-alpine
RUN mkdir /app
WORKDIR /app
COPY ./src /app
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8005", "--nothreading", "--noreload"]


