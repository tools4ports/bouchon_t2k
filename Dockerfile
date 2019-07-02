FROM python:3


RUN mkdir /usr/src/t2k
WORKDIR /usr/src/t2k

COPY . /usr/src/t2k

EXPOSE 80

CMD ["python", "serveur_http_bouchon_T2k.py", "docker_t2k_config.json"]