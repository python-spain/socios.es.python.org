FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # psycopg2 dependencies
  && apt-get install -y gcc python3-dev musl-dev \
  # Pillow dependencies
  && apt-get install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev libtiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apt-get install -y libffi-dev python-cffi \
  # Translations dependencies
  && apt-get install -y gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apt-get install -y postgresql-client



RUN addgroup --system django \
  && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
RUN pip install poetry
COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
ENV PIP_NO_BINARY=psycopg2
RUN poetry config virtualenvs.create false && poetry install -n --no-ansi --no-dev
RUN rm -rf /pyproject.toml \
  && rm -rf /poetry.lock

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
