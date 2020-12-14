#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import socket           ##### CLIENT TCP ##### 	

PORT = 12345 
HOTE = "localhost"    # <---À ADAPTER !!
TAILLE_MAX_PAQUET = 1024

sCli = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
sCli.connect((HOTE, PORT))
print("Connexion établie avec le serveur sur le port", PORT) 
print("Saisir FIN ferme le client, STOP arrête aussi le serveur") 

while 1:
    # Saisie du message 
    msg_a_envoyer = input("===(FIN / STOP pour terminer)==> ") 
    # Envoi du message encodé en octets
    envoi = bytes(msg_a_envoyer, encoding="utf-8") 
    sCli.send(envoi) 
    # Réception de l'accusé, si le serveur en envoie un 
    paquet_recu = sCli.recv(TAILLE_MAX_PAQUET)   # octets, donc 
    msg_recu = str(paquet_recu, encoding="utf-8")    #  à encoder... 
    print(msg_recu) 
    # On termine la boucle ? 
    if msg_a_envoyer == "FIN"  or msg_a_envoyer == "STOP" : 
        sCli.close() 
        print("Bye !") 
        break
