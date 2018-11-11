from awsInterface import IoT
import time
from lib import *


def printdata(client, userdata, message):
	print("received from server:")
	print(message.payload)


msg_id = 0
device = IoT()

message = {}
message['device_id'] = "001"
message['grow_id'] = "marijuana"


device.receivedata("oct1_1/sensor_data", printdata)

while True:
	message['msg_id'] = msg_id
	msg_id += 1
	message['time_stamp'] = str(datetime.datetime.now())
	msgjson = json.dumps(message)
	device.senddata(msgjson)
	print("sending..")
	time.sleep(10)
