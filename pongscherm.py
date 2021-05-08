from tkinter import *
import random
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt




class ball():
    def __init__(self,can):
        self.canvas = can
        self.x = 0
        self.y = 0
        self.r = 10
    def draw(self):
        self.canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill="white") 
        
    def setcords(self,X,Y):
        self.x = X
        self.y =Y


class paddel():
    def __init__(self,can,LR):
        self.canvas = can
        self.y = 200 
        self.length = 40
        self.width = 5
        if LR == 0:
            self.x = 10
        else:
            self.x = 485

    def sety(self,Y):
        self.y = Y
    def draw(self):
        self.canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.length, outline="white", fill="white")


class ponggame():
    def __init__(self): 
        self.tk = Tk()
        self.tk.title("GROEP5 PONG GAME")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost",1) 
        self.canvas=Canvas(self.tk,bg="black",width=500,height=400,bd=0,highlightthickness=0)
        self.canvas.pack()
        self.b = ball(self.canvas)
        self.pad1 = paddel(self.canvas,0)
        self.pad2 = paddel(self.canvas,1)
        self.score1 = 0
        self.score2 = 0

        self.txt1 = Label(self.tk, text="1" ,bg="black",fg="white", font=("Helvetica", 20))
        self.txt2 = Label(self.tk,text="1" ,bg="black",fg="white", font=("Helvetica", 20))
        self.txt1.place(x=160,y=20)
        self.txt2.place(x=320,y=20)
        self.txt1.place()
        self.txt2.place()

    def drawfield(self):
        self.canvas.create_rectangle(248,0,252,400,dash=(5,1), outline="white")
        self.txt1.configure(text=self.score1)
        self.txt2.configure(text=self.score2)  
    def gamecycle(self,data):
        while True:
            print(data)
            #clear screen
            self.tk.update()
            self.canvas.delete("all")
            #new positions
            posx = random.randint(10,480)
            posy = random.randint(10,380)
            self.b.setcords(posx,posy)
            randy = random.randint(10,380)
            self.pad1.sety(randy)
            self.pad2.sety(randy)
            #draw
            self.drawfield()
            self.b.draw()
            self.pad1.draw() 
            self.pad2.draw()
            #wait
            sleep(0.2)

def playgame(p):
    p.gamecycle(data)
pong = ponggame()
job = Thread(target = playgame, args=(pong, ))
job.start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("ap/groep5/scherm")


def on_message(client, userdata, msg):
    #P1=0;P2=0;BX=250;BY=200;S1=0;S2=0
    #message = msg.payload.decode("utf-8")
    #global data
    #data = message#message.split(";")
    #pong.pad1=data[0][2:]
    global data
    data = msg.payload.decode("utf-8")
    print(data[0][2:])

client = mqtt.Client(clean_session=True) #make id for mqtt
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect("broker.mqttdashboard.com", 1883) #choose broker and port
client.loop_start()
while True:
    pass
