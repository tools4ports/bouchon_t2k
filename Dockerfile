FROM python:3-alpine


RUN mkdir /usr/src/t2k

WORKDIR /usr/src/t2k

COPY . /usr/src/t2k

EXPOSE 80

CMD ["python", "serveur_http_bouchon_T2k.py"]
