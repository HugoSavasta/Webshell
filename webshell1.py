#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

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

def recupere_pid(s,a,b):
    chaine=''
    for i in range(a,b):
        chaine+=s[i]
    return chaine

def ajoute_echo(liste_commandes):
    n=len(liste_commandes)
    if n<=1: return liste_commandes
    echo,liste="echo '\n'",[]
    for i in range(n-1):
        liste.append(liste_commandes[i])
        liste.append(echo)
    return liste+[liste_commandes[-1]]

def executer_commandes(liste_commandes):
    global RESULTAT
    liste_commandes=ajoute_echo(liste_commandes)
    for commande in liste_commandes:
        r,w=os.pipe()
        pid=os.fork()

        if pid==0:
            os.dup2(w,1)
            os.dup2(w,2)
            os.close(w)
            if commande!='':
                os.execvp(shell, [shell,'-c',commande])
            else:
                os.write(1,"".encode("utf-8"))
                sys.exit(0)
        os.close(w)
        RESULTAT+="<br>".join(os.read(r,MAXBYTES).decode('utf-8').split("\n")[:-1])
        os.close(r)

def recupere_session():
    try:
        f=os.open(chemin_sauvegarde,os.O_RDONLY) # on tente d'ouvrir le fichier , s'il n'existe pas => except puis création du fichier
        SESSION=json.loads(os.read(f,MAXBYTES).decode("utf-8")) #on récupère la session dans le fichier (on suppose ici donc que le fichier existe)
        os.close(f)
        return SESSION
    except:
        f=os.open(chemin_sauvegarde,os.O_CREAT) # on arrive ici donc en supposant que le fichier n'existe pas , on le crée
        os.close(f)
        return {} # on renvoie un dictionnaire vide , on ajoutera pour chaque session chaque pid comme clé et comme valeur un sous dictionnaire avec les commandes et les résultats

lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')
(param,lecteur,RESULTAT)=('','','')
data = lecture[0]
liste_commandes=[]
signature=str(os.getpid())
date=time.ctime()+" : "
MAXBYTES = 10**8
notfirst=False
chemin_sauvegarde="/home/hugodtc/TUTORAT/Projet/historique_webshell1.json"
SESSION=recupere_session()
shell=os.environ["SHELL"].split("/")[-1] # voir plus tard on sen branle pour le moment

if ("ajoute" in data):
    notfirst=True
    param = ((data.split("&"))[0].split("="))[1]
    param = escaped_latin1_to_utf8(param).replace("+", " ")
    liste_commandes=param.split(";")

executer_commandes(liste_commandes)

if notfirst:
    a=data.index('e')
    b=data.index('?')
    XXX=recupere_pid(data,a+1,b)
    signature=XXX
    SESSION[signature]["commandes"].append(date+param) # on ajoute dans la session avec le bon pid la date + param (la commande tapée)
    SESSION[signature]["resultats"].append(RESULTAT) # on ajoute dans la session avec le bon pid le résultat de la commande tapée
    for i in range(len(SESSION[signature]["commandes"])): # même chose qu'au traitant5 sauf que l'on ajoute un <br> entre chaque commande tapée (nombre de commandes==nombres de résultats)
        lecteur+=SESSION[signature]["commandes"][i]+"<br>"# et chaque résultat de commande
        lecteur+=SESSION[signature]["resultats"][i]+"<br>" 
    f=os.open(chemin_sauvegarde,os.O_WRONLY) #sauvegarde
    os.write(f,json.dumps(SESSION).encode("utf-8"))
    os.close(f)

else:
    SESSION[signature]={"commandes":[],"resultats":[]} # première connexion donc on initialise avec un sous dictionnaire comprenant la liste des commandes et la liste de tous les résultats
    fd=os.open(chemin_sauvegarde,os.O_WRONLY)
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
                            <body>"""
                            +(escaped_latin1_to_utf8(lecteur.replace('+', ' ')))+
                                """<form action="ajoute{}" method="get">
                                    {}
                                    <input type="text" name="saisie" placeholder="Tapez quelque chose" />
                                    <input type="submit" name="send" value="&#9166;">
                                </form>"""
                            """</body> 
                            </html>""".format(signature,date))
os.write(1, reponse.encode("utf-8"))