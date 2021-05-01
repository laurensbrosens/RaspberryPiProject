 #!/usr/bin/python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO				#RPI.GPIO inkorten tot GPIO
from time import sleep
import random	
GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#boven
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#speed
GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)#onder

#leds 
lednummers = [13,5,6]

GPIO.setup(lednummers[2],GPIO.OUT)
GPIO.setup(lednummers[1],GPIO.OUT)#Groen
GPIO.setup(lednummers[0],GPIO.OUT)


num = random.randint(00,100)
class Control():
	"""docstring for control"""
	def __init__(controller, idnummer,leds):
		controller.id = idnummer
		controller.speed = 1
		controller.leds =leds

	def setid(c,num):
		c.id = int(num)
		if c.id == 0:
			print("links led" + str(c.leds[c.id]))

		elif c.id ==1:
			print("rechte led" + str(c.leds[c.id]))


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
		if c.id !="-1":
			client.publish("ap/groep5", str(msg), qos=0)




		
c1 = Control("-1",lednummers)

def on_publish(client, userdata, mid):
    print("message: "+str(mid))

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    #print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("ap/groep5")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    #print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    temp = str(msg.payload)
    print(temp)
    if len(temp) > 7 and c1.id == "-1":
    	responsenum = temp[2:5]
    	authnum = "!" + str(num)
    	if authnum == responsenum:
    		idnum = temp.split("ID=")[1][0]
    		print("authenticated ID=" + str(idnum))
    		c1.setid(idnum)

    	else:
    		print("could not authenticate")



client = mqtt.Client("digi_mqtt_test") #make id for mqtt
client.on_publish = on_publish
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect("broker.mqttdashboard.com", 1883) #choose broker and port
client.loop_start()

def druk(channel):
	c1.drukknop(channel)
	
	#print(msg)

GPIO.add_event_detect(23, GPIO.RISING, callback = druk, bouncetime=300)
GPIO.add_event_detect(24, GPIO.RISING, callback = druk, bouncetime=300)
GPIO.add_event_detect(25, GPIO.RISING, callback = druk, bouncetime=300)


def authenticate():
	global num
	sleep(5)
	if num <10:
		num = "0" + str(num)
	msg="?" + str(num)
	client.publish("ap/groep5",str(msg), qos=0)


try:
	authenticate()
	
	while True:
		sleep(0.05)

except KeyboardInterrupt:
	client.loop_stop()
	client.disconnect()
	GPIO.remove_event_detect(23)
	GPIO.remove_event_detect(24)
	GPIO.remove_event_detect(25)
	GPIO.cleanup()
