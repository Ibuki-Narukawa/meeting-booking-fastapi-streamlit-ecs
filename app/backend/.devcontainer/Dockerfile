FROM python:3.9-buster

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN echo 'alias awsume=". awsume"' >> /root/.bashrc

COPY pyproject.toml poetry.lock ./
RUN poetry install
