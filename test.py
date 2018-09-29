from awsInterface import IoT
import time
import json

def printdata(client, userdata, message):
	print("received from server:")
	print(message.payload)

device = IoT()
message = {}
message['message']="hello form client"
msgjson = json.dumps(message)

device.receivedata(printdata)

while True:
	device.senddata(msgjson)
	print("sending..")
	time.sleep(10)
