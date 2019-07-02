#!/usr/bin/python3
# coding: utf-8
 
import http.server
import xml.etree.ElementTree as ET
import datetime
import json
import argparse
import logging


class Configuration():
	def __init__(self, user_config):
		self.port = user_config.get("port", 80)
		levels_ok = {"debug":logging.DEBUG, "info": logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
		user_level = user_config.get("log_level", "info")
		if user_level not in levels_ok:
			raise Exception("le log_level n'est pas correct!")
		self.log_level = user_config.get("log_level", levels_ok[user_level])
		self.log_path = user_config.get("log_path", "./t2k_bouchon.log")
		self.mess_dir = user_config.get("mess_dir", ".")
 
class T2kHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		response = "T2k server is up!"
		self.wfile.write(bytes(response,"utf-8"))
	
	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "application/xml")
		self.end_headers()
		content_len = int(self.headers.get('content-length', 0))
		# Les xml en provenance d'Escaleport sont déclarés en iso-8859-1
		# post_body = self.rfile.read(content_len).decode("utf-8")
		post_body = self.rfile.read(content_len).decode("iso-8859-1")
		
		root = ET.fromstring(post_body)
		hd_att = root.find('Header').attrib
		
		# TODO contrôler le message
		# TODO sauvegarder le message dans un fichier.
		# répondre avec le bon numéro de message et la bonne version de la charte.
		logging.info("{} messId:{}".format(datetime.datetime.now().isoformat(), hd_att['LARefId']))
		
		with open(f"{config.mess_dir}/{hd_att['LARefId']}.xml",'w') as mess_file:
			mess_file.write(post_body)
		
		response = """<?xml version="1.0" encoding="ISO-8859-1"?>
<NCA_Receipt>
	<Header Version="{}" LARefId="{}" SentAt="{}" From="{}" To="{}" StatusCode="OK" StatusMessage="OK"/>
</NCA_Receipt>""".format(hd_att['Version'], hd_att['LARefId'],hd_att['SentAt'],hd_att['To'],hd_att['From'])
		self.wfile.write(response.encode("utf-8"))
		
# définition des paramètres de la ligne de commande
parser = argparse.ArgumentParser()
parser.add_argument("config", help="Fichier json de configuration")
config_path = parser.parse_args().config

with open(config_path,'r') as config_file:
	user_config = json.load(config_file)
	
# Conversion dict vers objet ET gestion des valeurs par défaut.
config = Configuration(user_config)

logging.basicConfig(filename = config.log_path, level = config.log_level)
		
print("Serveur actif sur le port :", config.port)
httpd = http.server.HTTPServer(("", config.port), T2kHTTPRequestHandler)
httpd.serve_forever()
