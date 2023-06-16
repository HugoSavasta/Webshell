#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

# ecrire sur la sortie 1
# mettre var dans du html pour que le site affiche sinon impossible

# fonction qui recompose ce que l'on a entrÃ©
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


lecture = os.read(1, 100000)
lecture = lecture.decode("utf-8").split('\r\n')

param = ""
data = lecture[0]
if ("ajoute?" in data):
    param = ((data.split("&"))[0].split("="))[1]


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
                            + ("<br>".join(lecture)) + "<br><br>" + escaped_latin1_to_utf8(param.replace('+', ' ')) +
                                """<form action="ajoute" method="get">
                                    <input type="text" name="saisie" placeholder="Tapez quelque chose" />
                                    <input type="submit" name="send" value="&#9166;">
                                </form>"""
                            """</body> 
                            </html>""")

os.write(1, reponse.encode("utf-8"))