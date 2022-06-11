FROM python:3.8.5

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

EXPOSE 8501

WORKDIR /app
COPY . /app

CMD streamlit run app.py \
    --browser.serverAddress="0.0.0.0" \
    --server.port="8501"
