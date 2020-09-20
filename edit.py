import os
from colorama import Fore, Back, Style
import sys
from time import sleep
import msvcrt
from threading import Thread

forecolor=Fore.BLACK
backcolor=Back.WHITE
width=120
height=40
text=""
filename="Untitled.txt"
scrollpos=0
curpos=[0,0]
vlist=[]
selchr="▒"
opsvn=False

def initialize(w=120,h=38):
    os.system("title AVNOTE - "+filename)
    os.system("mode con cols="+str(w))
    os.system("mode con lines="+str(h))
    os.system("color 70")

menu=["New","Open","Save","Help (F1)"]
shortcuts=[b"\x0e",b"\x0f",b"\x13",b"\x00"]
sdict=dict(zip(shortcuts,menu))

def buildmenu(w,h):
    mstr=forecolor + backcolor + " " + ' | '.join(menu) + " | " + filename
    print(mstr + " "*(w+10-len(mstr)) + Style.RESET_ALL)
    print(forecolor + backcolor + '╭─' + '─'*(w-4) + '─╮' + Style.RESET_ALL)
def buildwindow(wtxt,w,h):
    g=wtxt.split("\n")
    for ln in range(scrollpos,len(g)-1):
        line = forecolor + backcolor + '│ ' + g[ln]
        print(line + " "*(w+8-len(line)) + ' │' + Style.RESET_ALL)
    print(forecolor + backcolor + '│ ' + g[-1] + selchr +" "*(w-5-len(g[-1])) + ' │' + Style.RESET_ALL)
    for i in range(h-4-len(g)):
        print(forecolor + backcolor + '│ ' + ' '*(w-4) + ' │' + Style.RESET_ALL)
    print(forecolor + backcolor + '╰─' + '─'*(w-4) + '─╯' + Style.RESET_ALL)
    print(str(forecolor + backcolor + "| " + str(len([ i for i in text.split("\n") if i.strip(" ") != ""])) + " lines | " + str(len([i for i in text.replace("\n"," ").split(" ") if i.strip(" ") != ""])) + " words in document |"), end='', flush=True)
initialize()
def showmsg(mtitle,mtext):
    print("\n"*((height//2)-len(mtext.split("\n"))-2))
    print(' ' * ((width - len(mtitle))//2) + mtitle)
    for i in mtext.split("\n"):
        print(' ' * ((width - len(i))//2) + i)

def showwindow():
    while True:
        if not opsvn:
            height=os.get_terminal_size()[1]
            width=os.get_terminal_size()[0]
            os.system("cls")
            buildmenu(width,height)
            buildwindow(text,width,height)
            sleep(0.01)
        else:
            continue

def blink():
    while True:
        if not opsvn:
            global selchr
            selchr="▒"
            sleep(0.3)
            selchr="▓"
            sleep(0.3)
        else:
            continue

t = Thread(target=showwindow, args=())
t.start()

vb = Thread(target=blink, args=())
vb.start()

def openfile():
    global opsvn
    opsvn=True
    fname=""
    os.system("color 30")
    while True:
        os.system("cls")
        os.system("title "+filename)
        bt="Type filename\n"+"[ "+fname+" ]"
        showmsg("Open Document",bt)
        ich = msvcrt.getch()
        if ich == b"\r":
            break
        elif ich == b"\b":
            fname = fname[0:-1]
        else:
            fname += str(ich)[2:-1]
    try:    
        tex = open(fname,"r").read()
        os.system("title AVNOTE - "+filename)
        return [fname,tex]
    except:
        os.system("cls")
        os.system("color 40")
        showmsg("Error","Could not find this file.")
        sleep(1)
    opsvn=False

def savefile():
    os.system("cls")
    os.system("color 30")
    global text
    global filename
    with open(filename,"w") as fl:
        fl.write(text)
    showmsg("Saved Document","")
    sleep(1)
def showhelp():
    os.system("cls")
    os.system("color 30")
    showmsg("Help for AVNOTE","Ctrl + N for New, Ctrl + O to open, Ctrl + S to Save")
    sleep(2)

while True:
    input_char = msvcrt.getch()
    if input_char == b"\r":
        text += "\n"
    elif input_char == b"\t":
        text += "    "
    elif input_char == b"\b":
        text=text[0:-1]
    elif input_char in shortcuts:
        os.system("color 30")
        if sdict[input_char] == "New":
            opsvn=True
            os.system("cls")
            showmsg("New Document","Are you sure? (Y/N)")
            ich=msvcrt.getch()
            if ich == b"y":       
                text=""
                filename="Untitled.txt"
            opsvn=False
        elif sdict[input_char] == "Open":
            opsvn=True
            os.system("cls")
            if text.strip(" ") != "":
                showmsg("Open Document","Are you sure? You have unsaved work. (Y/N)")
                ich=msvcrt.getch()
                if ich == b"y":
                    G = openfile()
                    filename= G[0]
                    text= G[1]
            else:
                G = openfile()
                filename= G[0]
                text= G[1]
            opsvn=False
        elif sdict[input_char] == "Save":
            opsvn=True
            savefile()
            opsvn=False
        elif sdict[input_char] == "Help (F1)":
            opsvn=True
            showhelp()
            opsvn=False
        os.system("color 70")
    else:
        if not input_char == b"\xff":
            text += str(input_char)[2:-1]
