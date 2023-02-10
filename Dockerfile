FROM python:3.10-slim-buster
LABEL maintainer="yevgenii.nevmyvako@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code


COPY requirements.txt /code/

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . /code/


#RUN adduser \
#    --disabled-password \
#    --no-create-home \
#    django-user
#
#RUN chown -R django-user:django-user /vol/
#RUN chmod -R 755 /vol/web/

#USER django-user
