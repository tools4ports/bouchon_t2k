#!/usr/bin/python3
# coding: utf-8

import http.server
import xml.etree.ElementTree as ET
import datetime
import logging
import config


class T2kHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = (
            open("get.html", "r")
            .read()
            .replace("{{response_status}}", config.response_status)
        )
        self.wfile.write(bytes(response, "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        content_len = int(self.headers.get("content-length", 0))
        # Les xml en provenance d'Escaleport sont en iso-8859-1
        post_body = self.rfile.read(content_len).decode("iso-8859-1")

        root = ET.fromstring(post_body)
        hd_att = root.find("Header").attrib

        # TODO contrôler le message
        # info: hd_att['LARefId'] est l'identifiant unique du message
        logging.info(
            "{} messId:{}".format(
                datetime.datetime.now().isoformat(), hd_att["LARefId"]
            )
        )

        # si l'utilisateur a fourni un répertoire pour garder les messages on les y écrit.
        if config.mess_dir is not None:
            logging.debug(
                "Ecriture du fichier {}/{}.xml".format(
                    config.mess_dir, hd_att["LARefId"]
                )
            )
            with open(
                "{}/{}.xml".format(config.mess_dir, hd_att["LARefId"]), "w"
            ) as mess_file:
                mess_file.write(post_body)

        # répondre avec le bon numéro de message et la bonne version de la charte.
        response = """<?xml version="1.0" encoding="ISO-8859-1"?>
<NCA_Receipt>
	<Header Version="{}" LARefId="{}" SentAt="{}" From="{}" To="{}" StatusCode="{}" StatusMessage="Le bouchon T2k est en mode réponses systématique : {}"/>
</NCA_Receipt>""".format(
            hd_att["Version"],
            hd_att["LARefId"],
            hd_att["SentAt"],
            hd_att["To"],
            hd_att["From"],
            config.response_status,
            config.response_status,
        )
        # Cela peut sembler surprenant que déclarer un encodage en ISO et de transmettre en utf-8 mais
        # c'est bien ce que fait le vrai traffic 2000 alors bon...
        self.wfile.write(response.encode("utf-8"))


# Conversion dict vers objet ET gestion des valeurs par défaut.
config = config.Config()
print(config)

logging.basicConfig(stream=config.log_file, level=config.log_level)

print("Serveur actif sur le port :", config.port)
httpd = http.server.HTTPServer(("", config.port), T2kHTTPRequestHandler)
httpd.serve_forever()
