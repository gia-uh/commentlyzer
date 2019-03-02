FROM python:3.6.8

RUN git clone --depth=1 https://github.com/hiancdtrsnm/CubaCrawler Crawler

RUN mkdir app

RUN cd app &&\
    wget "https://drive.google.com/uc?authuser=0&id=1resrPNTxlVfeUgICncN51-1HsL0WvJJT&export=download" -O engine.tar.gz&&\
    tar -xzvf engine.tar.gz &&\
    rm engine.tar.gz


COPY requeriments.txt /requeriments.txt
RUN pip install -r /Crawler/requeriments.txt
RUN pip install -r /requeriments.txt && rm -rf /root/.cache
RUN spacy download es_core_news_md
COPY . /backend-observatorio
WORKDIR /
CMD python backend-observatorio/production.py
