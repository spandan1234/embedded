# Data Acquisition
## SensorData
### get_data()
* Initialize the variables
* Send Interrupt to Arduino
* Receive "SEND REQ" string from Arduino
* Send "SENSOR DATA" string to Arduino
* Receive SensorData from Arduino
* Filter the data
* Check signature
* If signature matches to "0xAB46CA" -> send +ACK
    * else -> send -ACK
* Convert the received data to JSON
* return  
### filter_data()
* receive data
* split the data into individual blocks
* assign each block to its appropriate attribute -> dict
* return the dict
### convert_to_json()
* convert the received dict to json
* return
### send_to_arduino()
* send a serial message to the arduino
### receive_from_arduino()
* receive the serial message from arduino
## ImageAcquire
### __init__
* initialize VideoCapture
* Specify Frame dimension
### capture_image()
* capture Frame
* save the image to Images folder
* return true 

## DataAcquisitionControlCenter
###
