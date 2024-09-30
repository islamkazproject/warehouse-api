FROM python:3.11-buster
LABEL authors="islam"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /warehouse-api

RUN apt-get update && \
    apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi --with dev

COPY src ./src

ENV PYTHONPATH=/warehouse-api/src

WORKDIR /warehouse-api/src

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000