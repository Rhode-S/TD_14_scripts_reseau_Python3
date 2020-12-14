#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import socket               ##### CLIENT UDP #####

# Adresse et port du serveur :
PORT = 12345                # N'importe quel port non réservé (> 1023)
HOTE = "localhost"        # <---Adresse du serveur, À ADAPTER À VOTRE SITUATION !! 
sCli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

TAILLE_MAX_PAQUET = 1024    # Utile pour la réception uniquement.

print("Saisir vos messages, suivi de [ENTRÉE].")
print("Écrire FIN pour terminer, voire STOP pour arrêter aussi le serveur.\n")

while 1 :                                                   # On envoie des
    msg = input("===(FIN / STOP pour terminer)==> ")        # octets, donc on
    sCli.sendto(bytes(msg, encoding="utf8"), (HOTE,PORT))   # doit encoder
                                                            # les chaînes...
                                                            
    #### Facultatif : afficher l'accusé de réception #############
    paquet_recu, src = sCli.recvfrom(TAILLE_MAX_PAQUET)
    msg_recu = str(paquet_recu, encoding='utf-8')
    print("Confirmation :", msg_recu)
    ##############################################################

    if msg == "FIN" or msg == "STOP" :
        sCli.close()
        print("Bye !")
        break
