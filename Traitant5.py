#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

def escaped_latin1_to_utf8(s):
 res = '' ; i = 0
 while i < len(s):
     if s[i] == '%':
         res += chr(int(s[i+1:i+3], base=16))
         i += 3
     elif s[i]=='+':
         res+=' '
         i+=1
     else :
         res += s[i]
         i += 1
 return res

def recupere_pid(s,a,b):
    chaine=''
    for i in range(a,b):
        chaine+=s[i]
    return chaine

def recupere_session():
    try:
        f=os.open(chemin_sauvegarde,os.O_RDONLY) # on tente d'ouvrir le fichier , s'il n'existe pas => except puis création du fichier
        SESSION=json.loads(os.read(f,MAXBYTES).decode("utf-8")) #on récupère la session dans le fichier (on suppose ici donc que le fichier existe)
        os.close(f)
        return SESSION
    except:
        f=os.open(chemin_sauvegarde,os.O_CREAT) # on arrive ici donc en supposant que le fichier n'existe pas , on le crée
        os.close(f)
        return {} # ici différent du traitant4 on return un dictionnaire vide , on ajoutera lors de chaque première session les pids correspondants comme clés

MAXBYTES = 10**8
signature=str(os.getpid())
lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')
param = ""
lecteur=""
data = lecture[0]
chemin_sauvegarde="/home/hugodtc/TUTORAT/Projet/historique_traitant5.json" #nom du fichier à ne pas changer mais le chemin à changer
SESSION=recupere_session() #comme son nom l'indique

if ("ajoute" in data):
    a=data.index('e')
    b=data.index('?')
    XXX=recupere_pid(data,a+1,b)
    param = ((data.split("&"))[0].split("="))[1]
    signature=XXX
    SESSION[signature].append(param) # on ajoute dans la bonne session (pid) ce que l'on vient d'écrire 
    for i in range(len(SESSION[signature])):
        lecteur+=SESSION[signature][i]+"<br>" # on met dans le lecteur l'ensemble des éléments de la liste avec <br> en plus (maybe .join plutôt??)
    f=os.open(chemin_sauvegarde,os.O_WRONLY) # on sauvegarde 
    os.write(f,json.dumps(SESSION).encode("utf-8"))
    os.close(f)

else:
    SESSION[signature]=[] # première connexion donc on initialise notre session puis on sauvegarde
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
                            <body> """
                            +(escaped_latin1_to_utf8(lecteur))+ 
                                """<form action="ajoute{}" method="get">
                                    <input type="text" name="saisie" placeholder="Tapez quelque chose" />
                                    <input type="submit" name="send" value="&#9166;">
                                </form>"""
                            """</body> 
                            </html>""".format(signature))
os.write(1, reponse.encode("utf-8"))