FROM python:3.9

EXPOSE 80

WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app
RUN pip install -U pip \
    && pip install --no-cache-dir poetry \
    && poetry install --no-dev
COPY src/ /app/src
RUN mkdir /app/data

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
