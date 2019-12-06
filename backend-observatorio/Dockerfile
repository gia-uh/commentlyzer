FROM python:3.6.8 as backend
RUN mkdir models
RUN curl -L -o /models/cv.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/countvectorizer.joblib

RUN curl -L -o /models/pnn.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/CountVectorizer.Positivo.-.Neutro.-.Negativo.+.LinearSVC.joblib

RUN curl -L -o /models/so.joblib \
    https://github.com/giamatcom/CommenlyzerEngine/releases/download/v1.0.1/CountVectorizer.Objetivo.-.Subjetivo.+.RidgeClassifier.joblib

RUN mkdir /backend-observatorio
WORKDIR /backend-observatorio
COPY ./backend-observatorio/requeriments.txt /requeriments.txt
# COPY ./backend-observatorio/requeriments.txt /requeriments.txt
RUN pip install -r /requeriments.txt && rm -rf /root/.cache
COPY ./backend-observatorio .
WORKDIR /
# COPY /backend-observatorio/app/static/index.html