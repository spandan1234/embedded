import wiringpi as wpi
import serial
import json
import datetime
from logger import logger_variable


class SensorData:
    """
    functions: get_data(), filter_data(), convert_to_json()
    public variables:
    """

    def __init__(self):
        """
        Initialize variables and operators
        1. initialize serial port
        2. initialize GPIO pins

        identifier:
            serialOpen: Serial Port
        """
        # initialize logger_variable
        self.logger = logger_variable(__name__, 'SensorData.log')

        # open serial port
        self.serialOpen = serial.Serial('/dev/ttyACM0', 115200)
        # initialize wiringPi GPIO mode
        wpi.wiringPiSetupGpio()
        # set GPIO pins as output
        wpi.pinMode(self.interrupt_pin, 1)
        wpi.pinMode(26, 1)

    def get_data(self):
        """
        identifier:
            sensor_data: list
            interrupt: boolean
            ack: boolean
            request: string
        :return: filter_sensor_data: dict
        """
        sensor_data = ""
        interrupt_pin = 25
        ack = False
        request = ""

        # set interrupt -> True
        interrupt = True

        # send interrupt to Arduino
        wpi.digitalWrite(interrupt_pin, interrupt)

        # receive string "SEND REQ"
        while request != "SEND REQ":
            try:
                request = self.receive_from_arduino()
            except serial.ConnectionError:
                print("Connection Error")

        # Send a request for SENSOR DATA
        self.send_to_arduino("SENSOR DATA")

        # receive sensor data in a list
        while ack is False:
            try:
                sensor_data = self.receive_from_arduino()
            except ConnectionError:
                print("Connection Error")

            # Check the bytes of data received before other checks

            # filter the received information
            filter_sensor_data = self.filter_data(sensor_data)

            # check the packet for device signature & send +/-ACK to arduino
            if filter_sensor_data[0] == '0xAB46CA':
                filter_sensor_data['status'] = 'OK'
                ack = True
            else:
                ack = False
            self.send_to_arduino(ack)

        # convert to json before sending
        # json_sensor_data = self.convert_to_json(filter_sensor_data)

        return filter_sensor_data

    # split the string data and return the dict
    @staticmethod
    def filter_data(self, data):
        # initialize a filter_data dictionary
        filtered_data = {}

        # split the data string into individual elements using list & dict
        data_split = data.split()
        data = ['signature', 'temperature', 'humidity',
                'waterlevel', 'pH', 'turbidity', 'status', 'timestamp']
        filtered_data[data[0]] = data_split[0]
        filtered_data[data[1]] = data_split[1]
        filtered_data[data[2]] = data_split[2]
        filtered_data[data[3]] = data_split[3]
        filtered_data[data[4]] = data_split[4]
        filtered_data[data[5]] = data_split[5]
        filtered_data[data[6]] = ""
        filtered_data[data[7]] = datetime.datetime.now()

        return filtered_data

    # send data to arduino
    def send_to_arduino(self, message):
        self.serialOpen.write(message)

    # receive data from arduino
    def receive_from_arduino(self):
        return self.serialOpen.readline()

    # convert any dict to json
    @staticmethod
    def convert_to_json(self, data):
        if type(data) == dict:
            json_data = json.dumps(data)
        else:
            print("Incorrect Data Format")
        return json_data
