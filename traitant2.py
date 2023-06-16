#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

# ecrire sur la sortie 1
# mettre var dans du html pour que le site affiche sinon impossible

lecture = os.read(1, 100000)
verif= lecture.decode("utf-8").split("/")
verif= verif[0]+verif[1][-4:]+' '+verif[2][:3] # a modifier

if verif!="GET HTTP 1.1":
    os.write(2,"request not supported".encode("utf-8"))
    sys.exit(0) #à modifier peut être 

lecture = lecture.decode("utf-8").split('\r\n')
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
            + "<br>".join(lecture) +
            """</body> 
            </html>""")

os.write(1, reponse.encode("utf-8"))