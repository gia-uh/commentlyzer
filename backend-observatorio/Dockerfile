FROM python:3.7.6 as backend
RUN mkdir models
RUN curl -L -o /models/cv.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/cv.joblib

RUN curl -L -o /models/pnn.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/pnn.joblib

RUN curl -L -o /models/so.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/so.joblib

RUN mkdir /backend-observatorio
WORKDIR /backend-observatorio
COPY ./backend-observatorio/requeriments.txt /requeriments.txt
# COPY ./backend-observatorio/requeriments.txt /requeriments.txt
RUN pip install -r /requeriments.txt && rm -rf /root/.cache
RUN python -m spacy download es_core_news_md
COPY ./backend-observatorio .
WORKDIR /
# COPY /backend-observatorio/app/static/index.html