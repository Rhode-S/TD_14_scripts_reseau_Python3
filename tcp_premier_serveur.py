#!/usr/bin/env python3
#-*- coding: utf-8 -*- 

import socket           ##### SERVEUR TCP (1) #####

HOTE = ""    # <---À ADAPTER !!
PORT = 12345
TAILLE_MAX_PAQUET = 1024 
TAILLE_FILE_ATTENTE = 10 

sSrv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
sSrv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Rend le port disponible
sSrv.bind((HOTE,PORT))                                      #  plus rapidement à la fin
sSrv.listen(TAILLE_FILE_ATTENTE) 
print("Serveur à l'écoute à l'adresse", HOTE, "et sur le port", PORT)

donnees = "" 
while 1 : 
    sCli, source = sSrv.accept()     # Connexion acceptée avec client
    print("Connexion avec un client à l'adresse", source[0], 
          "sur le port", source[1])
    while 1:  # Connexion acceptée, on écoute en boucle ce client 
              #  pourvoir en accepter d'autre...
        donnees = sCli.recv(TAILLE_MAX_PAQUET)  # Réception de paquets
        msg_recu = str(donnees, encoding="utf-8")
        print("↳ Reçu (de l'adresse", source[0], ", sur le port", end="")
        print(source[1], ") :", msg_recu)
        sCli.send(b"'" + donnees + bytes("' bien reçu. ✔", encoding="utf-8")) 
        if "FIN" in msg_recu or "STOP" in msg_recu : 
            break  # Sortie de la boucle 'While' la plus intérieure, on va fermer le client 
    sCli.close() 
    if "STOP" in msg_recu : 
        break  # Sortie de la bouce 'While' la plus extérieure, on doit fermer le serveur
sSrv.close() 
