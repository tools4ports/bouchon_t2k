import argparse
import sys
import os
import logging

class Config():

    """ 
        priorité aux paramètre de la ligne de commande:
            -port <port> -log_file <log_file> -log_level <log_level> -mess_dir <mess_dir>
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
        #valeurs pas défauts
        self.port = 80
        self.log_file_path = None       # std_out
        self.log_level_name = "WARNING" # nom du niveau de log fourni pas l'utilisateur
        self.log_level = None           # valeur numérique du niveau de log correspondant
        self.mess_dir = None            # répertoire où stocker les messages: pas de stockage si vide

        # exploitation des variables d'environnement

        # Pas de paramétrage du port dans l'environnement
        # car si on est dans un container on en a pas besoin et ça peut
        # même devenir problématique.
        # if os.environ.get('T2K_PORT') is not None:
        #    self.port = os.environ.get('T2K_PORT')
        if os.environ.get('T2K_LOG_FILE') is not None:
            self.log_file_path = os.environ.get('T2K_LOG_FILE')
        if os.environ.get('T2K_LOG_LEVEL') is not None:
            self.log_level_name = os.environ.get('T2K_LOG_LEVEL')
        if os.environ.get('T2K_MESS_DIR') is not None:
            self.mess_dir = os.environ.get('T2K_MESS_DIR')

        # récupération des paramètres de la ligne de commande
        parser = argparse.ArgumentParser()
        parser.add_argument("--port", help="port d'écoute", type=int)
        parser.add_argument("--log_file", help="fichier de log")#, type = str)
        parser.add_argument("--log_level", help="niveau de log")#, type = str)
        parser.add_argument("--mess_dir", help="répertoire de sauvegarde des messages reçu (pas de sauvegarde si omis)")
        args = parser.parse_args()

        if args.port is not None:
            self.port = args.port
        if args.log_file is not None:
            self.log_file_path = args.log_file
        if args.log_level is not None:
            self.log_level_name = args.log_level
        if args.mess_dir is not None:
            self.mess_dir = args.mess_dir
        
        # controle des paramètres
        # vérification du port
        if not isinstance(self.port, int):
            raise ValueError(f"Invalid port: {self.port}")
        # vérification que le log_level_name correspond bien à une valeur acceptée par logging.
        self.log_level = getattr(logging, self.log_level_name.upper(), None)
        if not isinstance(self.log_level, int):
            raise ValueError(f"Invalid log level: {self.log_level_name}")
        # vérification du répertoire du fichier de log
        if self.log_file_path is not None:
            # si le fichier n'est pas accessible on laisse l'exception remonter
            self.log_file = open(self.log_file_path, "a")
        else:
            self.log_file = sys.stdout
        # vérification du répertoire des messages
        if not self.mess_dir is None and not os.path.isdir(self.mess_dir):
            raise ValueError(f"Le répertoire {self.mess_dir} n'existe pas.")
    
    def __repr__(self):
        res = f"port : {self.port}\n"
        res += f"log level: {self.log_level_name}:{self.log_level_name}\n"
        res += f"log file: {self.log_file_path}\n"
        res += f"mess dir: {self.mess_dir}\n"
        return res

