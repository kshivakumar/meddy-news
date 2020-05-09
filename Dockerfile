FROM python:3-alpine
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "manage.py", "runserver"]
CMD ["0:8005"]


