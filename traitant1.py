#!/usr/bin/env python3
import os,sys,signal,socket,select,atexit,random,time,json

lecture = os.read(1, 100000)
os.write(2, lecture)
lecture= lecture.decode("utf-8").split("/")
tmp=lecture[0]+lecture[1][-4:]+' '+lecture[2][:3]

if tmp!="GET HTTP 1.1":
    os.write(2,"request not supported".encode("utf-8"))
    sys.exit(0) #à modifier peut être 
