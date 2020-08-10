import argparse
import sys
import os
import logging


class Config:

    """ 
        priorité aux paramètre de la ligne de commande:
            -port <port> -log_file <log_file> -log_level <log_level> -mess_dir <mess_dir> -response_status <status>
        puis aux variables d'environnement:
            T2K_LOG_FILE
            T2K_LOG_LEVEL
            T2K_MESS_DIR
        puis on se replie sur les valeurs par défaut
            port : 80
            fichier de log : stdout
            niveau de log : warning
            répertoire pour stocker les messages : aucun => pas de sauvegarde
    """

    def __init__(self):
        # valeurs pas défauts
        self.port = 80
        self.log_file_path = None  # std_out
        self.log_level_name = "WARNING"  # nom du niveau de log fourni pas l'utilisateur
        self.log_level = None  # valeur numérique du niveau de log correspondant
        self.mess_dir = (
            None  # répertoire où stocker les messages: pas de stockage si vide
        )
        self.response_status = "OK"  # la réponse de T2K

        # exploitation des variables d'environnement

        # Pas de paramétrage du port dans l'environnement
        # car si on est dans un container on en a pas besoin et ça peut
        # même devenir problématique.
        # if os.environ.get('T2K_PORT') is not None:
        #    self.port = os.environ.get('T2K_PORT')
        if os.environ.get("T2K_LOG_FILE") is not None:
            self.log_file_path = os.environ.get("T2K_LOG_FILE")
        if os.environ.get("T2K_LOG_LEVEL") is not None:
            self.log_level_name = os.environ.get("T2K_LOG_LEVEL")
        if os.environ.get("T2K_MESS_DIR") is not None:
            self.mess_dir = os.environ.get("T2K_MESS_DIR")
        if os.environ.get("T2K_RESPONSE_STATUS") is not None:
            self.response_status = os.environ.get("T2K_RESPONSE_STATUS")

        # récupération des paramètres de la ligne de commande
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", help="port d'écoute", type=int)
        parser.add_argument("--log_file", help="fichier de log")  # , type = str)
        parser.add_argument(
            "--log_level", help="niveau de log (debug, info, warning, error, critic)"
        )  # , type = str)
        parser.add_argument(
            "--mess_dir",
            help="répertoire de sauvegarde des messages reçu (pas de sauvegarde si omis)",
        )
        parser.add_argument(
            "--response_status", help="la réponse de T2K (OK par défaut)"
        )
        args = parser.parse_args()

        if args.port is not None:
            self.port = args.port
        if args.log_file is not None:
            self.log_file_path = args.log_file
        if args.log_level is not None:
            self.log_level_name = args.log_level
        if args.mess_dir is not None:
            self.mess_dir = args.mess_dir
        if args.response_status is not None:
            self.response_status = args.response_status

        # controle des paramètres
        # vérification du port
        if not isinstance(self.port, int):
            raise ValueError("Invalid port: {}".format(self.port))
        # vérification que le log_level_name correspond bien à une valeur acceptée par logging.
        self.log_level = getattr(logging, self.log_level_name.upper(), None)
        if not isinstance(self.log_level, int):
            raise ValueError("Invalid log level: {}".format(self.log_level_name))
        # vérification du répertoire du fichier de log
        if self.log_file_path is not None:
            # si le fichier n'est pas accessible on laisse l'exception remonter
            self.log_file = open(self.log_file_path, "a")
        else:
            self.log_file = sys.stdout
        # vérification du répertoire des messages
        if not self.mess_dir is None and not os.path.isdir(self.mess_dir):
            raise ValueError("Le répertoire {} n'existe pas.".format(self.mess_dir))

    def __repr__(self):
        res = "port : {}\n".format(self.port)
        res += "log level: {}\n".format(self.log_level_name)
        res += "log file: {}\n".format(self.log_file_path)
        res += "mess dir: {}\n".format(self.mess_dir)
        res += "reponses status dir: {}\n".format(self.response_status)
        return res

