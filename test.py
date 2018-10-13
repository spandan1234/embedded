from awsInterface import AWSInterface
import time
import random
from lib import *

def printdata(client, userdata, message):
	print("received from server:")
	print(message.payload)

def randomSensor():
	keys = ['signature', 'temperature', 'humidity', 'waterlevel', 'pH', 'turbidity', 'status', 'timestamp']
	sensor = {}
	for k in keys:
		sensor[k] = random.randint(1,50)

	return sensor

def randomActuator():
	keys = ['signature', 'pump', 'fan', 'light', 'timestamp']
	actuator = {}
	for k in keys:
		actuator[k] = random.randint(0,1)

	return actuator

device = AWSInterface()
device.receiveData("sensor_data",printdata)

while True:
	data = {}
	data['sensor']=randomSensor()
	data['actuator']=randomActuator()
	device.sendData(data)
	print("sending..")
	time.sleep(5)

