FROM python:3.8.5

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

EXPOSE 80

WORKDIR /app
COPY ./sql_app /app/backend
RUN mkdir /app/data

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80" , "--reload"]
