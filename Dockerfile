FROM python:3.12-slim AS base
ENV PATH /opt/venv/bin:$PATH
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base AS builder
WORKDIR /opt
RUN apt-get update && \
    apt-get install -y gcc
RUN python -m venv venv
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false &&  poetry install --no-cache

FROM base
WORKDIR /opt
COPY --from=builder /opt/venv venv
COPY . /opt
CMD sleep 100 && python3  main.py