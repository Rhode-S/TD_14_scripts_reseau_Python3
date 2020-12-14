#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 

import socket                ##### SERVEUR TCP - Multi-clients ##### 
import select  # pour 'balayer' les connexions demandées / acceptées.
 
HOTE = ''   # signifie 'quelconque '
PORT = 12345 
TAILLE_MAX_PAQUET = 1024 
 
sSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSrv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sSrv.bind((HOTE, PORT)) 
sSrv.listen(5)  # Nbre maxi acceptés "en parallèle" 
print("Le serveur écoute à présent sur le port", PORT) 
 
clients_connectes = [] 
serveur_ecoute = True 
while serveur_ecoute:
    # (1) On vérifie si de nouveaux clients demandent à se connecter 
    #  => on écoute le serveur, maxi pendant 0.05 sec. 
    connexions_demandees, wlist, xlist = select.select([sSrv], 
                                                       [], [], 0.05) 
    # triplet de listes pour select.select 
    #   = a_lire, a_ecrire, en_except.
    # (..)  connexions_demandees est une liste de sockets «demandeurs»
    for connexion in connexions_demandees: 
        sCli, infos_connexion = connexion.accept() 
        # On ajoute le socket connecté à la liste des clients connectés 
        clients_connectes.append(sCli) 
        # (..) clients_connectes est une liste de sockets «acceptés»
    # (2) Maintenant, on écoute la liste des clients «connectés»
    liste_a_lire = [] 
    # (..) liste_a_lire est une liste de demandes de messages à lire
    try:        # sinon, exception levée si la liste des clients est vide 
        liste_a_lire, wlist, xlist = select.select(clients_connectes, 
                                                        [], [], 0.05) 
    except select.error: 
        pass    # Ne rien faire s'il n'y en a pas, sans message d'erreur 
    else: 
        # On parcourt la liste des messages à lire 
        for sCli in liste_a_lire: 
            paquet_recu = sCli.recv(TAILLE_MAX_PAQUET)      # octets, donc 
            msg_recu = str(paquet_recu, encoding="utf-8")    #  à encoder... 
            print("'", msg_recu, "' reçu de",   #  message, 
                  sCli.getpeername()[0],        #  IP et 
                  "/", sCli.getpeername()[1])   #  port de l'envoyeur
        
            ### Facultatif : accusé de réception ########################### 
            sCli.send(bytes("'"+msg_recu+"' bien reçu !", encoding="utf-8")) 
            ################################################################ 
            if msg_recu == "STOP": 
                serveur_ecoute = False 
print("Fermeture des connexions au serveur") 
for sCli in clients_connectes: 
    sCli.close() 
sSrv.close()
