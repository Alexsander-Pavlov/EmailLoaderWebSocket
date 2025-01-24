FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_V=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

RUN adduser user \
    && addgroup docker \
    && adduser user docker


COPY pyproject.toml ./

RUN apt-get update \
    && apt-get install -y postgresql \
    && apt-get install -y postgresql-client \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get install -y git \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-root

COPY ./docker/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN mkdir static
RUN mkdir media/images

WORKDIR /app

RUN chown -R user:user .

USER user

EXPOSE 8000

ENTRYPOINT [ "/entrypoint" ]
