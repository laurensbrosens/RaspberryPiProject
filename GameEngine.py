#!/usr/bin/python
import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO
import time

topic = "ap/groep5"
player1 = ""
player2 = ""
id1 = False
position1 = 0
position2 = 0

def on_connect(client, userdata, flags, rc):
   client.subscribe(topic, qos=1)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

def on_message(client, userdata, msg):
    global id1
    message = msg.payload.decode("utf-8")
    print(message)
    if message[0] == "?":
        if not id1:
            id1 = True
            client.publish(topic, "!" + message[1:] + str("ID=0"), qos=1)
        else:
            client.publish(topic, "!" + message[1:] + str("ID=1"), qos=1)
            #client.disconnect()
            client.on_message = on_message2
            print("Authentication disconnected")

client = mqtt.Client(client_id="clientId-0Bn69AzoCg")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883)

def on_message2(client, userdata, msg):
    global player1
    global player2
    global position1
    global position2
    message = msg.payload.decode("utf-8")
    print(message)
    if message[0:2] == "ID":
        print("id = "+message[0:2])
        print("UP = " +message[7:])
        if message[2:3] == 0:
            position1 = position1 + int(message[7:])
        else:
            position2 = position2 + int(message[7:])
    print("position1 = " + str(position1))
    print("position2 = " + str(position2))
client.loop_forever()




