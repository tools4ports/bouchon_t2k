# bouchon_t2k
Mini serveur simulant une réponse Traffic2000

## Fonctionnalités
Retourne une réponse correcte à un message correct.
Accepte les messages respectant les chartes T2k 5.0.x et 5.1.x (xsd 5.0 et 5.2)

## Limitations actuelles
Ecoute le port 1977 défini en dur
Ne fait aucun contrôle métier
Retourne toujour "ok" sauf si le message est suffisamment mal contruit pour provoquer une erreur (retourne un code 500).

## Prérequis
Python 3.x

## Comment lancer le serveur:
```bash
python3 serveur_http_bouchon_t2k.py
```
ou
```bash
nohup python3 serveur_http_bouchon_T2k.py &
```

Comment tester:
```bash
curl -d "le contenu du xml envoyé par le SIP" -X POST http://localhost:1977
```
