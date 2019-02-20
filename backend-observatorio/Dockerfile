FROM python:3.6.8-alpine3.9
COPY requeriments.txt /requeriments.txt
RUN pip install -r /requeriments.txt

RUN spacy download es_core_news_md
COPY . /backend-observatorio
WORKDIR /backend-observatorio
CMD python production.py
