#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

# Voir pour le traitant4 si ce n'est pas possible d'avoir comme structure de donnée pour la sauvegarde qu'une simple liste plutôt qu'un dico avec une seule clé et qu'une seule valeur (liste)
# Mais possible que ce soit impossible avec json
# Pour traitant4 et traitant5 je n'ai pas utilisé de sous dictionnaires avec "commandes" et "résultats" vu que l'on veut simplement afficher ce que l'on écrit
# On utilise donc que de simples listes
# Autre chose, voir si l'on peut pas delete le else de la ligne 50 et faire tout dans le except de la fonction recupere_session()

def escaped_latin1_to_utf8(s):
 res = '' ; i = 0
 while i < len(s):
     if s[i] == '%':
         res += chr(int(s[i+1:i+3], base=16))
         i += 3
     else :
         res += s[i]
         i += 1
 return res

def recupere_session():
    try: 
        f=os.open(chemin_sauvegarde,os.O_RDONLY) # on tente d'ouvrir le fichier , s'il n'existe pas => except puis création du fichier
        SESSION=json.loads(os.read(f,MAXBYTES).decode("utf-8")) #on récupère la session dans le fichier (on suppose ici donc que le fichier existe)
        os.close(f)
        return SESSION 
    except:
        f=os.open(chemin_sauvegarde,os.O_CREAT) # on arrive ici donc en supposant que le fichier n'existe pas , on le crée
        os.close(f)
        return {'0':[]} # ici on return le dictionnaire initial , donc avec '0' comme "clé globale" qui va être la même pour chaque navigateur
        # d'où le fait que chaque session n'est pas unique , dans le traitant 5 la clé '0' sera remplacée par le pid

MAXBYTES = 10**8
lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')
param = ""
lecteur=""
data = lecture[0]
chemin_sauvegarde="/home/hugodtc/TUTORAT/Projet/historique_traitant4.json" #nom du fichier à ne pas changer mais le chemin à changer
SESSION=recupere_session() #comme son nom l'indique

if ("ajoute?" in data):
    param = ((data.split("&"))[0].split("="))[1]
    SESSION['0'].append(param) # on suppose que ce n'est pas la première connexion donc on ajoute ce que l'on a écrit dans le dico
    for i in range(len(SESSION['0'])):
        lecteur+=SESSION['0'][i]+"<br>" # on met dans le lecteur l'ensemble des éléments de la liste avec <br> en plus (maybe .join plutôt??)
    f=os.open(chemin_sauvegarde,os.O_WRONLY) # on sauvegarde
    os.write(f,json.dumps(SESSION).encode("utf-8"))
    os.close(f)

else:
    fd=os.open(chemin_sauvegarde,os.O_WRONLY) # première connexion donc on ne fait rien mis à part sauvegarder l'état de la session
    os.write(fd,json.dumps(SESSION).encode("utf-8"))
    os.close(fd)

reponse = ("""HTTP/1.1 200 
                            Content-Type: text/html; charset=utf-8
                            Connection: close
                            Content-Length: 125

                            <!DOCTYPE html>
                            <head>
                                <link rel='icon' href='data:;base64,='>
                                <title>Hello, world!</title>
                                <style>
                                body {
                                    background-color: black;
                                    color: red;
                                    background-image: url('https://c.tenor.com/BRDnAfz1WfsAAAAd/hacker.gif');
                                    background-size: cover;
                                    height: 100vh;
                                    padding:0;
                                    margin:0;
                                    }
                                
                                </style>
                            </head>
                            <body> """
                            +(escaped_latin1_to_utf8(lecteur.replace('+', ' ')))+ 
                                """<form action="ajoute" method="get">
                                    <input type="text" name="saisie" placeholder="Tapez quelque chose" />
                                    <input type="submit" name="send" value="&#9166;">
                                </form>"""
                            """</body> 
                            </html>""")
os.write(1, reponse.encode("utf-8"))