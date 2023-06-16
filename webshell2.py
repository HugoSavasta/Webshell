#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json, os.path

#faut ajouter un \n à la fin du cat pour que lon ne reste pas sur la même ligne
# voir le bonus de changement de shell pour tous les traitants et webshell ou que webshell je sais plus 

def handler(sig,frame):
    try: 
        os.system("rm /tmp/shell_vers_traitant{} /tmp/traitant_vers_shell{}".format(signature,signature)) # On verra plus tard pour la suppression du fichier de sauvegarde
    except:
        pass
    
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

def supprime_element_vide(SESSION):
    commandes,resultats=[],[]
    for i in range(len(SESSION[signature]["commandes"])):
        if SESSION[signature]["commandes"][i]==SESSION[signature]["resultats"][i]=="":
            pass
        else:
            commandes.append(SESSION[signature]["commandes"][i])
            resultats.append(SESSION[signature]["resultats"][i])
    return commandes,resultats

def save_history(date, param, result, signature):
    global SESSION # pas obligatoire ? dictionnaire agit comme des pointeurs donc pas obligatoire ?
    SESSION[signature]["flagNEUF"]=0
    SESSION[signature]["commandes"].append(date+param)  # on ajoute dans la session avec le bon pid la date + param (la commande tapée)
    SESSION[signature]["resultats"].append(result) # on ajoute dans la session avec le bon pid le résultat de la commande tapée
    SESSION[signature]["commandes"]=supprime_element_vide(SESSION)[0]
    SESSION[signature]["resultats"]=supprime_element_vide(SESSION)[1]
    f=os.open(chemin_sauvegarde,os.O_WRONLY) # sauvegarde
    os.write(f,json.dumps(SESSION).encode("utf-8"))
    os.close(f)

def get_initial_pid():
    a=data.index('e')
    b=data.index('?')
    return recupere_pid(data,a+1,b)

def load_history(signature):
    lecteur=''
    for i in range(len(SESSION[signature]["commandes"])): # même chose qu'au traitant5 sauf que l'on ajoute un <br> entre chaque commande tapée (nombre de commandes==nombres de résultats)
        lecteur+=SESSION[signature]["commandes"][i]+"<br>"# et chaque résultat de commande
        if SESSION[signature]["resultats"][i]!="":
            lecteur+=SESSION[signature]["resultats"][i]+"<br>"
    return lecteur

def recupere_session():
    try:
        f=os.open(chemin_sauvegarde,os.O_RDONLY) # on tente d'ouvrir le fichier , s'il n'existe pas => except puis création du fichier
        SESSION=json.loads(os.read(f,MAXBYTES).decode("utf-8")) #on récupère la session dans le fichier (on suppose ici donc que le fichier existe)
        os.close(f)
        return SESSION
    except:
        f=os.open(chemin_sauvegarde,os.O_CREAT)  # on arrive ici donc en supposant que le fichier n'existe pas , on le crée
        os.close(f)
        return {} # on renvoie un dictionnaire vide , on ajoutera pour chaque session chaque pid comme clé et comme valeur un sous dictionnaire avec les commandes et les résultats

def send_reponse(traitantShell, shellTraitant, firstExecFlag, param, signature, date):
    w = os.open(traitantShell, os.O_WRONLY)
    r = os.open(shellTraitant, os.O_RDONLY)

    if (firstExecFlag == 1):
        result = ""
        save_history("", "", "", signature)
    else:
        param=param.replace(";","&&")
        param += "; echo COUCOU\n" #MARKER
        os.write(w,param.encode("utf-8"))
        dataOut = b''
        while (not dataOut.endswith("COUCOU".encode("utf-8"))):
            dataOut += os.read(r,1)
        dataOut = dataOut.decode("utf-8")

        if (dataOut.split("\n")[0] == ""):
            result="<br>".join(dataOut.split("\n")[1:-1])
        else:
            result="<br>".join(dataOut.split("\n")[:-1])
        param = param.replace("&&", ";")[:-14] + "\n"
        save_history(date, param, result, signature)

    lecteur = load_history(signature) 
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

lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')

param=''
lecteur=""
result=""
firstExecFlag = 1
data = lecture[0]
signature=str(os.getpid())
date=time.ctime()+" : "
MAXBYTES = 10**8
chemin_sauvegarde="/home/hugodtc/TUTORAT/Projet/historique_webshell2.json" #nom du fichier à ne pas changer mais le chemin à changer
SESSION=recupere_session() #comme son nom l'indique

signal.signal(signal.SIGINT, handler)

if ("ajoute" in data):
    firstExecFlag = 0
    param = ((data.split("&"))[0].split("="))[1]
    param = escaped_latin1_to_utf8(param).replace("+", " ")

    signature = get_initial_pid() 
   
shellTraitant = "/tmp/shell_vers_traitant" + signature
traitantShell = "/tmp/traitant_vers_shell" + signature

if (firstExecFlag == 0):
    send_reponse(traitantShell, shellTraitant, firstExecFlag, param, signature, date)
else:
    SESSION[signature]={"commandes":[],"resultats":[]} # première connexion donc on initialise avec un sous dictionnaire comprenant la liste des commandes et la liste de tous les résultats
    fd=os.open(chemin_sauvegarde,os.O_WRONLY) #sauvegarde
    os.write(fd,json.dumps(SESSION).encode("utf-8"))
    os.close(fd)
    os.mkfifo(traitantShell)
    os.mkfifo(shellTraitant)

    pid = os.fork()
    if pid == 0:
        r = os.open(traitantShell, os.O_RDONLY)
        w = os.open(shellTraitant, os.O_WRONLY)
        
        os.dup2(r, 0)
        os.dup2(w, 1)
        os.dup2(w, 2)

        os.execvp('zsh', ['zsh'])
    else:
        send_reponse(traitantShell, shellTraitant, firstExecFlag, param, signature, date)
        os.wait()