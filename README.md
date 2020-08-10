# bouchon_t2k
Mini serveur simulant une réponse Traffic2000

## Fonctionnalités
Retourne une réponse correcte à un message correct.
Si demandé le statut de la réponse peut être modifiée.
Accepte les messages respectant les chartes T2k 5.0.x et 5.1.x (xsd 5.0 et 5.2)

## Limitations actuelles
Ne fait aucun contrôle métier.
Retourne toujour systématiquement la même réponse ("OK" par défaut) sauf si le message est suffisamment mal contruit pour provoquer une erreur (retourne un code 500).

## Prérequis
Python 3.x

## Comment lancer le serveur:
Pour avoir la liste des options:
```bash
python3 serveur_http_bouchon_t2k.py --help 
```

exemple avec toutes les option
```bash
python3 serveur_http_bouchon_T2k.py --port 5000 --log_level info --log_file /var/log/t2k/t2k.log --mess_dir /var/data/messages --response_status
```
valeurs par défaut:
port: 80
log_level: warning
log_file: stdout
mess_dir: aucun donc pas de sauvegarde des messages
response_status: "OK"

Note: sur certains système il est nécessaire d'avoir les droits root pour utiliser les ports au dessous de 4096.

lancé en relachant le terminal:
```bash
nohup python3 serveur_http_bouchon_T2k.py &
```

## utilisation de docker:
Il est aussi possible d'utiliser les variables d'environnement suivantes:
T2K_LOG_LEVEL
T2K_LOG_FILE
T2K_MESS_DIR
T2K_RESPONSES_STATUS

```bash
docker build . -t bouchon_t2k
docker run --rm --detach --publish 5000:80 --name bouchon_t2k bouchon_t2k
```
ou utiliser docker-compose.

## Comment tester (ici le serveur écoute le port 5000):
```bash
curl http://localhost:5000
```
Retourne une  page html statique avec le rappel de la configuration du serveur.

Pour transmettre des messages:
```bash
curl -d "le contenu du xml envoyé par le SIP" -X POST http://localhost:5000
```

ou tester les deux:
```bash
python3 client_test.py http://localhost:5000
```
