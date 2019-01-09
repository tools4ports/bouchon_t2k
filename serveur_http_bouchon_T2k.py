#!/usr/bin/python3
 
import http.server
import xml.etree.ElementTree as ET
import datetime
 
class T2kHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "application/xml")
		self.end_headers()
		response = """<xml>réponse factice à GET</xml>"""
		self.wfile.write(bytes(response,"utf-8"))
	
	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "application/xml")
		self.end_headers()
		content_len = int(self.headers.get('content-length', 0))
		post_body = self.rfile.read(content_len).decode("utf-8")
		
		root = ET.fromstring(post_body)
		hd_att = root.find('Header').attrib
		
		# TODO contrôler le message
		# TODO sauvegarder le message dans un fichier.
		# répondre avec le bon numéro de message et la bonne version de la charte.
		print("{} messId:{}".format(datetime.datetime.now().isoformat(), hd_att['LARefId']))
		
		response = """<?xml version="1.0" encoding="ISO-8859-1"?>
<NCA_Receipt>
	<Header Version="{}" LARefId="{}" SentAt="{}" From="{}" To="{}" StatusCode="OK" StatusMessage="OK"/>
</NCA_Receipt>""".format(hd_att['Version'], hd_att['LARefId'],hd_att['SentAt'],hd_att['To'],hd_att['From'])
		self.wfile.write(response.encode("utf-8"))
		
		
		

		

PORT = 1977 
print("Serveur actif sur le port :", PORT)
httpd = http.server.HTTPServer(("", PORT), T2kHTTPRequestHandler)
httpd.serve_forever()
