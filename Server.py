#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

def handler(sig,frame):  # se met en attente de la mort d'un fils
    global clients
    try:
        fils, filstatu = os.waitpid(-1,0)
        clients.remove(fils)
    except:pass

def handler2(sig,frame): 
    if flag == 0:
        for e in clients:
            os.kill(e, signal.SIGINT)
            fils, filstatu = os.waitpid(e,0)
        serversocket.close()
    sys.exit(0)

def verifType(string):
    for e in string:
        if e not in "0123456789":
            print("TypeError")  
            sys.exit(0)

def verifValue(string):
    if (int(string) <= 2000):
        print("PORT trop petit")
        sys.exit(0)

def deletePort(server): # liberation du port 
    print("\nPort liberé")
    server.close()

if len(sys.argv) != 3:
    print("ValueError")
    sys.exit(0) 
else:
    verifType(sys.argv[2]) #je donnne le 2eme argument car c une string # pour vérifier si c'est un entier # je dois parcourir chaque caractere de la string
    verifValue(sys.argv[2]) 

HOST = "127.0.0.1" # or 'localhost' or '' - Standard loopback interface
PORT = int(sys.argv[2]) # Port to listen on (non-privileged ports are > 1023)
flag=0
clients=[]
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(4)
signal.signal(signal.SIGCHLD,handler)
signal.signal(signal.SIGINT, handler2)
atexit.register(deletePort,serversocket)
print("[serveur , pid={}] écoute sur le port {}".format(os.getpid(),PORT))

while True:
    (clientsocket,(addr,port,),) = serversocket.accept() # blocking; returns if a client connects.
    if (addr != "127.0.0.1"):
            clientsocket.close()
    pid=os.fork()
    if pid==0:
        os.dup2(clientsocket.fileno(),0)
        os.dup2(clientsocket.fileno(),1)
        serversocket.close()
        os.execvp(sys.argv[1],  [sys.argv[1]])
    else:
        clientsocket.close()
        clients.append(pid)
        print(f"[serveur] nouvelle connexion acceptée (pid={pid} , port client={port})\n")