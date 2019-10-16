
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY Commenlyzer-front/package*.json ./
RUN npm install
COPY Commenlyzer-front .
RUN npm run build



FROM python:3.6.8 as backend
RUN git clone --depth=1 https://github.com/hiancdtrsnm/CubaCrawler Crawler
RUN pip install -r /Crawler/requeriments.txt
#RUN mkdir app
RUN mkdir /backend-observatorio
WORKDIR /backend-observatorio
COPY ./backend-observatorio/requeriments.txt /requeriments.txt
# COPY ./backend-observatorio/requeriments.txt /requeriments.txt
RUN pip install -r /requeriments.txt && rm -rf /root/.cache
RUN spacy download es_core_news_md
RUN mkdir -p /backend-observatorio/app
RUN mkdir /models &&\
    cd /models &&\
    wget "https://drive.google.com/uc?authuser=0&id=1resrPNTxlVfeUgICncN51-1HsL0WvJJT&export=download" -O engine.tar.gz&&\
    tar -xzvf engine.tar.gz &&\
    rm engine.tar.gz
RUN chmod 777 /models/engine/serialized/
COPY ./backend-observatorio .
CMD python backend-observatorio/production.py
COPY --from=build-stage /app/dist /backend-observatorio/app/static
RUN mv /backend-observatorio/app/static/static/* /backend-observatorio/app/static
WORKDIR /
# COPY /backend-observatorio/app/static/index.html