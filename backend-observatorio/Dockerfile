FROM python:3.6
COPY requeriments.txt /requeriments.txt
RUN mkdir /root/.pip && echo "[global]\nindex = http://10.6.120.227:8081/repository/pypi-proxy/pypi\nindex-url = http://10.6.120.227:8081/repository/pypi-proxy/simple\ntrusted-host = 10.6.120.227" > /root/.pip/pip.conf
pip install -r /requeriments.txt
#RUN pip install -r /requeriments.txt
#RUN spacy download es_core_news_md
COPY ./app/engine/es_core_news_md /backend-observatorio/app/engine/es_core_news_md
COPY . /backend-observatorio
WORKDIR /backend-observatorio
CMD python production.py
