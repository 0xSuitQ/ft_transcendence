FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-client nginx

RUN pip install django psycopg2-binary djangorestframework djangorestframework-simplejwt django-extensions Werkzeug pyOpenSSL web3 pyotp qrcode

COPY ./entrypoint.sh /entrypoint.sh
COPY . .

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]