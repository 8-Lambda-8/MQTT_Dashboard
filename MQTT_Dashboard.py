#!/usr/bin/env python
import time


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
		#print("switchSocket "+topic[-1:])
		relNr = int(topic[-1:])
		relays[relNr] = int(msg)
		Socket_buttons[relNr-2]['bg']="green" if relays[relNr] else "red"

	if "Light" in topic:
		#print("switchLight")
		relays[1] = int(msg)
		Light_button['bg']="green" if relays[1] else "red"

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

def MqttToggle(topic,relayNr):
	val = int(not bool(relays[relayNr]))
	#print()
	#print("mqtt toggle "+topic+"  "+str(relayNr)+" "+str(val))
	client.publish(topic, val,retain=True)



##
##
#	Window Stuff
##
##

from tkinter import *
#import tkFont

from tkinter import font

root = Tk()
root.title("MQTT Dashboard")

BTN_Font = font.Font(family='Helvetica', size=36, weight='bold')

root.geometry("800x500")
root.resizable(200,200)
root.minsize(600,200)

frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)

Light_button = Button(frame, 
					text="Light", 
					command=lambda: MqttToggle("/BOX/Light",1),
					height = 50,
					width=50,
					font=BTN_Font)

Socket_buttons = [Button(frame, 
					text="Socket "+str(i), 
					command=lambda topic="/BOX/Socket/"+str(2+i),relNr=int(2+i): MqttToggle(topic,relNr),
					height = 50,
					width=50,
					font=BTN_Font) for i in range(6)]
i = 0

Light_button.grid(column=0, row=0, sticky=N+S+E+W)
Light_button['bg']="green" if relays[1] else "red"

for y in range(2):
	for x in range(3):
		Socket_buttons[i].grid(column=x, row=y+1, sticky=N+S+E+W)
		Socket_buttons[i]['bg']="green" if relays[i+2] else "red"
		i=i+1

for x in range(3):
	Grid.columnconfigure(frame, x, weight=1)

for y in range(3):
	Grid.rowconfigure(frame, y, weight=1)

#Temperature Control
temperatureFrame=Frame(frame)
temperatureFrame.grid(sticky=N+S+E+W, column=1, row=0, columnspan=2)
temperatureFrame['bg']="gray"


root.mainloop()
	
	