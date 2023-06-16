#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json, os.path

#deco
#https://c.tenor.com/5ry-200hErMAAAAd/hacker-hacker-man.gif ordi
#https://33.media.tumblr.com/9cebcec899889b81f2adea7b5486fdbb/tumblr_ne8fbcYjVR1ru5h8co1_500.gif poutine
#https://c.tenor.com/-SV9TjUGabMAAAAC/hacker-python.gif hackeur

def handler(sig,frame):
    try:
        os.system("rm /tmp/shell_vers_traitant{} /tmp/traitant_vers_shell{}".format(signature,signature)) # On verra plus tard pour la suppression du fichier de sauvegarde
    except:
        pass

def handlerAlarm(sig, frame):
    print("reçu",file=sys.stderr)
    w = os.open(shellTraitant, os.O_WRONLY)
    os.write(w, "readFlag COUCOU\n".encode("utf-8"))
    os.close(w)

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


def save_historyREAD(date,param, result, signature):
    global SESSION # pas obligatoire ? dictionnaire agit comme des pointeurs donc pas obligatoire ?
    SESSION[signature]["flagNEUF"]=1
    if not (y(key1) in param):
        date=''
    SESSION[signature]["commandes"].append(date+param)  # on ajoute dans la session avec le bon pid la date + param (la commande tapée)
    SESSION[signature]["resultats"].append(result) # on ajoute dans la session avec le bon pid le résultat de la commande tapée
    f=os.open(chemin_sauvegarde,os.O_WRONLY) # sauvegarde
    os.write(f,json.dumps(SESSION).encode("utf-8"))
    os.close(f)

def get_initial_pid():
    a=data.index('e')
    b=data.index('?')
    return recupere_pid(data,a+1,b)

def search_reponse(L):
    reponse=[]
    for i in range(len(L)):
        if "read" in L[i]:
            reponse.append(i)
    try:return L[reponse[-1]+1]
    except:return ''

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
        verify=param.split(";")
        bool1,bool2=False,True
        if y(key2) in param:
            bool1=True
            indices,sup=[],[]
            for i in range(len(verify)):
                if y(key2) in verify[i]:
                    indices.append(i)
                else:
                    bool2=False
                    sup.append(verify[i])
            param=";".join(sup)
        param=param.replace(";","&&")
        param += "; echo COUCOU\n" #MARKER
        os.write(w,param.encode("utf-8"))
        dataOut = b''
        while (not dataOut.endswith("COUCOU\n".encode("utf-8"))):
            signal.alarm(2)
            dataOut += os.read(r,1)
        dataOut = dataOut.decode("utf-8")[:-1]

        if ("readFlag" in dataOut ):
            send_reponseREAD(traitantShell, shellTraitant, firstExecFlag, param, signature, date, dataOut)
            
        else:
            if (dataOut.split("\n")[0] == ""):
                result="<br>".join(dataOut.split("\n")[1:-1])
            else:
                result="<br>".join(dataOut.split("\n"))
               
            param = param.replace("&&", ";")[:-14] + "\n"
        try:
            if "; echo COUCOU" in result:
                result="".join("".join(result.split("<br>")).split(";")[:-1])
            else:
                result="<br>".join(result.split("<br>")[:-1])
            if bool1:
                result=result.split("<br>")
                param=param.split(";")
                for i in range(len(indices)):
                    param.insert(indices[i],"echo $REPLY")
                    result.insert(indices[i],search_reponse(SESSION[signature]["commandes"]))
                if bool2:
                    param,result=param[:-1],result[:-1]
                param=";".join(param)
                result="<br>".join(result)

            if SESSION[signature]["flagNEUF"]==1 and not ("readFlag" in dataOut):
                save_history('', param, result, signature)
            else:
                save_history(date, param, result, signature)
        except:sys.exit(0)
        

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
def y(x): return "".join([chr(ord(x[i])-5) for i in range(len(x))])
def send_reponseREAD(traitantShell, shellTraitant, firstExecFlag, param, signature, date, dataOut):
    w = os.open(traitantShell, os.O_WRONLY)
    r = os.open(shellTraitant, os.O_RDONLY)
    if (dataOut.split("\n")[0] == ""):
        result="<br>".join(dataOut.split("\n")[1:-1])
    else:
        result="<br>".join(dataOut.split("\n")[:-1])
    param = param.replace("&&", ";")[:-14] + "\n"
    save_historyREAD(date,param, result, signature)
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
                        background-image: url('https://33.media.tumblr.com/9cebcec899889b81f2adea7b5486fdbb/tumblr_ne8fbcYjVR1ru5h8co1_500.gif');
                        background-size: cover;
                        height: 40vh;
                        padding:0;
                        margin:0;
                        }
                    
                    </style>
                </head>
                <body>"""
                +(escaped_latin1_to_utf8(lecteur.replace('+', ' ')))+
                    """<form action="ajoute{}" method="get"> 
                        <input type="text" name="saisie" placeholder="Tapez quelque chose" />
                        <input type="submit" name="send" value="&#9166;">
                    </form>"""
                """</body> 
                </html>""".format(signature))
    os.write(1, reponse.encode("utf-8"))

lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')

param=''
lecteur=""
result=""
key1,key2='wjfi',"jhmt%)WJUQ^"
firstExecFlag = 1
data = lecture[0]
signature=str(os.getpid())
date=time.ctime()+" : "
MAXBYTES = 10**8
readflag=True
chemin_sauvegarde="/home/hugodtc/TUTORAT/Projet/historique_webshell.json" #nom du fichier à ne pas changer mais le chemin à changer
SESSION=recupere_session() #comme son nom l'indique

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGALRM, handlerAlarm)

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
    SESSION[signature]={"commandes":[],"resultats":[],"flagNEUF":0} # première connexion donc on initialise avec un sous dictionnaire comprenant la liste des commandes et la liste de tous les résultats
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

        os.execvp('zsh', ['zsh traitant_vers_shell 3<> traitant_vers_shell &> shell_vers_traitant 4< shell_vers_traitant'])
    else:
        send_reponse(traitantShell, shellTraitant, firstExecFlag, param, signature, date)
        os.wait()