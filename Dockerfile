FROM python:3.12-slim

WORKDIR /code

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . .
