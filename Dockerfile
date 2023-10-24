FROM python:3.7.17-slim-bullseye
RUN pip install --upgrade pip
RUN pwd
WORKDIR /app
COPY . /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate

EXPOSE 8000

ENTRYPOINT [ "python3" ]
CMD [ "manage.py","runserver","0.0.0.0:8000" ]
