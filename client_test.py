import requests
from xml.etree import ElementTree as ET
import os
import datetime


os.environ['NO_PROXY'] = '127.0.0.1'

URL = "http://127.0.0.1:1977"
r = requests.get(URL)
if r.text != "T2k server is up!":
	raise Exception(r.text)
	
# envoi d'un message NCA_PORT
LARefId = "FRXXX000000000000000000000000000000"
date_heure = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
nca_port = f"""<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?> 
<NCA_Port> 
	<Header Version="5.2" LARefId="{LARefId}" SentAt="{date_heure}" To="TRA2K" From="FRXXXPOR"/> 
	<Body> 
		<VesselIdentification IMONumber="9517525"/> 
		<ShipCallInformation ShipCallId="FRCFR2019000586" PortOfCall="FRXXX"/> 
		<VoyageInformation LastPort="CAREB" ETAToPortOfCall="2019-06-03T09:00:00Z" ETDFromPortOfCall="2019-06-03T13:00:00Z" TotalPersonsOnBoard="4" PositionInPortOfCall="A1-A4 - BASSIN ST PIERRE"/> 
	</Body> 
</NCA_Port>"""

r = requests.post(URL, data = nca_port)
print(r.text)