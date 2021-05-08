#!/usr/bin/python
import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import time
from ball import ball

topic = "ap/groep5"
player1 = ""
player2 = ""
id1 = False
position1 = 0
position2 = 0
score0 = 0
score1 = 0
b = ball()
gamestarted = False

def on_connect(client, userdata, flags, rc):
   client.subscribe(topic, qos=2)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def on_message(client, userdata, msg):
    global id1
    message = msg.payload.decode("utf-8")
    print(message)
    if message[0] == "?":
        if not id1:
            id1 = True
            client.publish(topic, "!" + message[1:] + str("ID=0"), qos=2)
        else:
            client.publish(topic, "!" + message[1:] + str("ID=1"), qos=2)
            #client.disconnect()
            client.on_message = on_message2
            print("Authentication done")

client = mqtt.Client(client_id="clientId-0Bn69AzoCg")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883)
def on_message2(client, userdata, msg):
   message = msg.payload.decode("utf-8")
   print(message)
   if message[0:5] == "START":
      print("Game start")
      global gamestarted
      gamestarted = True
      b.reset()
      client.on_message = on_message3

def on_message3(client, userdata, msg):
    global player1
    global player2
    global position1
    global position2
    message = msg.payload.decode("utf-8")
    print(message)
    if message[0:2] == "ID":
        print("id = "+message[3:4])
        print("UP = " +message[7:])
        if message[3:4] == 0:
            position1 = position1 + int(message[7:])
        else:
            position2 = position2 + int(message[7:])
    print("position1 = " + str(position1))
    print("position2 = " + str(position2))
client.loop_start()
while True:
   if gamestarted:
      b.update(position1,position2)
      if b.goal:
         client.publish(topic, "$", qos=2)
         b.goal = False
         if b.scorer == 0:
            score0 += 1
         else:
            score1 += 1
         b.reset()
      client.publish(topic, "P1="+str(position1)+"P2="+str(position2)+"BX="+str(b.xpos)+"BY="+str(b.ypos)+"S1="+str(score0)+"S2="+str(score1), qos=0)
      print("P1="+str(position1)+";P2="+str(position2)+";BX="+str(b.xpos)+";BY="+str(b.ypos)+";S1="+str(score0)+";S2="+str(score1))
      if score0 >= 10 or score1 >= 10:
         client.loop_stop()
         break
print("Game over")



