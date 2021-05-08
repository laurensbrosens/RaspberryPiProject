 #!/usr/bin/python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO				#RPI.GPIO inkorten tot GPIO
from time import sleep
import random
from threading import Thread

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#boven
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#speed
GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#onder

#leds 
lednummers = [13,5,6]

GPIO.setup(lednummers[2],GPIO.OUT)
GPIO.setup(lednummers[1],GPIO.OUT)#Groen
GPIO.setup(lednummers[0],GPIO.OUT)






def on_publish(client, userdata, mid):
    print("message: "+str(mid))

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    #print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("ap/groep5")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def on_message2(client, userdata,msg):
	temp = str(msg.payload)
	print(temp[2])
	if temp[2] == "$":
		ledjob = Thread(target = c1.newball)
		ledjob.start()


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    #print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    temp = str(msg.payload)
    print(temp)
    if len(temp) > 7 and c1.id == "-1":
    	responsenum = temp[2:5]
    	authnum = "!" + str(c1.num)
    	if authnum == responsenum:
    		idnum = temp.split("ID=")[1][0]
    		print("authenticated ID=" + str(idnum))
    		c1.setid(idnum)
    		client.on_message = on_message2

    	else:
    		print("could not authenticate")


client = mqtt.Client(clean_session=True) #make id for mqtt
client.on_publish = on_publish
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect("broker.mqttdashboard.com", 1883) #choose broker and port
client.loop_start()

class Control():
	"""docstring for control"""
	def __init__(controller, idnummer,leds):
		controller.id = idnummer
		controller.speed = 1
		controller.leds =leds
		controller.num = random.randint(00,100)
		controller.authenticate()

	def authenticate(c):
		sleep(5)
		if c.num <10:
			c.num = "0" + str(c.num)
		msg="?" + str(c.num)
		client.publish("ap/groep5",str(msg), qos=2)	

	def setid(c,num):
		c.id = int(num)
		if c.id == 0:
			print("links led" + str(c.leds[c.id]))

		elif c.id ==1:
			print("rechte led" + str(c.leds[c.id]))
	def newball(c):
		for x in range(3):
			print("led aan")
			sleep(0.5)
			print("led uit")
			sleep(0.5)

	def sentmsg(c,msg):
		client.publish("ap/groep5", str(msg), qos=0)
			


	def drukknop(c,channel):
		movement=""
		if channel == 23:
			movement = ""
		elif channel == 24:
			if c.speed == 1:
				c.speed = 2
			else:
				c.speed = 1
		elif channel == 25:
			movement = "-"

		movement = movement + str(c.speed)


		msg = "ID=" + str(c.id) + "UP="+str(movement)
		#print(msg)
		if c.id !="-1" and channel != 24:

			job = Thread(target = c1.sentmsg,args=(msg,))
			job.start()
			#client.publish("ap/groep5", str(msg), qos=0)




		
c1 = Control("-1",lednummers)


GPIO.add_event_detect(23, GPIO.RISING, callback = c1.drukknop, bouncetime=300)
GPIO.add_event_detect(24, GPIO.RISING, callback = c1.drukknop, bouncetime=300)
GPIO.add_event_detect(25, GPIO.RISING, callback = c1.drukknop, bouncetime=300)


try:
	while True:
		sleep(5)

except KeyboardInterrupt:
	client.loop_stop()
	client.disconnect()
	GPIO.remove_event_detect(23)
	GPIO.remove_event_detect(24)
	GPIO.remove_event_detect(25)
	GPIO.cleanup()
