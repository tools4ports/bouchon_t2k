# bouchon_t2k
Mini serveur simulant une réponse Traffic2000

## Fonctionnalités
Retourne une réponse correcte à un message correct.
Accepte les messages respectant les chartes T2k 5.0.x et 5.1.x (xsd 5.0 et 5.2)

## Limitations actuelles
Ne fait aucun contrôle métier
Retourne toujour "ok" sauf si le message est suffisamment mal contruit pour provoquer une erreur (retourne un code 500).

## Prérequis
Python 3.x

## Comment lancer le serveur:
```bash
python3 serveur_http_bouchon_t2k.py config.json
```
ou
```bash
nohup python3 serveur_http_bouchon_T2k.py config.json &
```

## utilisation de docker:
```bash
docker build -t bouchon_t2k
docker run --rm --detach --publish 1977:80 --name bouchon_t2k bouchon_t2k
```

## Comment tester (ici le serveur écoute le port 1977):
```bash
curl -d "le contenu du xml envoyé par le SIP" -X POST http://localhost:1977
```
ou 
```bash
python3 client_test.py 
```
