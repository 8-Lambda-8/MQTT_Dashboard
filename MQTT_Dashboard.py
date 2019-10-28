#!/usr/bin/env python
import time




##
##
#	Window Stuff
##
##

from tkinter import *

fenster = Tk()
fenster.title("MQTT Dashboard")

fenster.geometry("500x500")
fenster.resizable(0,0)

def buttonLight():
	client.publish("/BOX/Light", int(not bool(relays[1])),retain=True)

my_button = Button(fenster, text="Light", command=buttonLight,height = 100,width=100)


#my_label = Label(fenster, option=value, ... )

my_button.pack()


##
##
#	MQTT Stuff
##
##

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe


relays = [0,0,0,0,0,0,0,0]

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("/BOX/#",0)
	
def on_message(client, userdata, message):
	topic = str(message.topic)
	msg = str(message.payload)[2:-1]
	
	

	if "Socket" in topic:
		relays[topic[-1:]] = int(msg)
		print(topic)	
		print(msg)
		print(relays)
	if "Light" in topic:
		relays[1] = int(msg)
		print(topic)	
		print(msg)
		print(relays)
		
		
		
def on_subscribe(topic):
	print("subscribed to \""+topic+"\"")


client = mqtt.Client()
client.username_pw_set(username="test1",password="test1")

client.on_message = on_message
client.on_connect = on_connect


client.connect("mqtt", 1883, 60)
client.loop_start()


client.on_subscribe = on_subscribe





fenster.mainloop()
	
	