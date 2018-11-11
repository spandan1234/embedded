from actuator.actuatorControl import ActuatorControl
from data_acquisition.CameraCapture import CameraCapture
from data_acquisition.SensorData import SensorData
from configparser import ConfigParser
import datetime
import schedule
from os import path
import os


class GrowCycle:

    def __init__(self, states, logger):
        self.parser = ConfigParser()
        # get current working directory
        cwd = os.getcwd()
        # check if file is present
        if path.isfile("config_files/plant.conf"):
            print("config file present")
        self.parser.read('plant.conf')
        self.plantCycleDuration = self.parser.get('PlantInfo', 'plantCycle')
        self.growStartDate = datetime.datetime.now()
        self.estimatedHarvest = datetime.datetime.now() + datetime.timedelta(weeks=self.plantCycleDuration)
        self.ledOnDuration = None
        self.ledOnInterval = None
        self.fanOnDuration = None
        self.fanOnInterval = None
        self.pumpOnDuration = None
        self.pumpOnInterval = None
        self.collectDataInterval = None
        self.collectImageInterval = None
        self.Actuator = ActuatorControl()
        self.states = states
        self.Sensor = SensorData()
        self.CameraCapture = CameraCapture()
        self.logger = logger

    # def startGrowCycle(self):
    #     currentWeek = self.getCurrentWeek()
    #
    #     while(datetime.date.today() <= self.estimatedHarvest):
    #         self.schedCurrentWeek(currentWeek)
    #         while(self.getCurrentWeek() == currentWeek):
    #             schedule.run_pending()
    #             time.sleep(1)
    #         currentWeek = self.getCurrentWeek()

    def schedCurrentWeek(self, currentWeek):
        parser = ConfigParser()
        self.parser.read('plant.conf')
        # get plant critical data
        self.tempUL = int(parser.get(currentWeek, 'tempUL'))
        self.tempLL = int(parser.get(currentWeek, 'tempLL'))
        self.humidityUL = int(parser.get(currentWeek,
                                         'humidityUL'))
        self.humidityLL = int(parser.get(currentWeek,
                                         'humidityLL'))
        self.phUL = float(parser.get(currentWeek, 'phUL'))
        self.phLL = float(parser.get(currentWeek, 'phLL'))
        self.ecUL = float(parser.get(currentWeek, 'ecUL'))
        self.ecLL = float(parser.get(currentWeek, 'ecLL'))
        self.waterlevelUL = int(parser.get(currentWeek,
                                           'waterlevelUL'))
        self.waterlevelLL = int(parser.get(currentWeek,
                                           'waterlevelLL'))
        self.ledOnDuration = float(parser.get(currentWeek,
                                              'ledOnDuration'))
        self.ledOnInterval = float(parser.get(currentWeek,
                                              'ledOnInterval'))
        self.fanOnDuration = float(parser.get(currentWeek,
                                              'fanOnDuration'))
        self.fanOnInterval = float(parser.get(currentWeek,
                                              'fanOnInterval'))
        self.pumpOnDuration = int(parser.get(currentWeek,
                                             'pumpOnDuration'))
        self.pumpOnInterval = int(parser.get(currentWeek,
                                             'pumpOnInterval'))
        self.collectDataInterval = int(parser.get(currentWeek,
                                                  'collectDataInterval'))
        self.collectDataDuration = int(parser.get(currentWeek,
                                                  'collectDataDuration'))
        self.collectCameraInterval = int(parser.get(currentWeek,
                                                    'collectCameraInterval'))
        self.collectCameraDuration = int(parser.get(currentWeek,
                                                    'collectCameraDuration'))
        self.sendDataToAWSInterval = float(parser.get(currentWeek,
                                                      'sendDataInterval'))
        self.sendImagesToAWSInterval = float(parser.get(currentWeek,
                                                        'sendImagesInterval'))

        self.logger.debug('Weekly data from Config File collected')
        schedule.clear()
        self.initialize_states()

    def initialize_states(self, states):
        """
        Initialize the global states with the plant.conf
        :return:No return
        """
        self.states.tempLL = self.tempLL
        self.states.tempUL = self.tempUL
        self.states.humidityUL = self.humidityUL
        self.states.humidityLL = self.humidityLL
        self.states.phUL = self.phUL
        self.states.phLL = self.phLL
        self.states.ecUL = self.ecUL
        self.states.ecLL = self.ecLL
        self.states.waterlevelUL = self.waterlevelUL
        self.states.waterlevelLL = self.waterlevelLL

        self.logger.debug('Critical Level states initialized')
        return

    def lightOn(self):
        self.Actuator.turnLightOn()
        self.logger.debug('Led switched ON')
        self.states.LED_status = True
        lightOffTime = format(datetime.datetime.now() +
                              datetime.timedelta(hours=self.ledOnDuration),
                              '%H:%M:%S')
        schedule.every().day.at(lightOffTime).do(self.lightOff)

    def lightOff(self):
        self.Actuator.turnLightOff()
        self.logger.debug('Led Switch Off')
        self.states.LED_status = False
        return schedule.CancelJob

    def fanOn(self):
        self.Actuator.turnFanOn()
        self.logger.debug('Fan switched ON')
        self.states.FAN_status = True
        fanOffTime = format(datetime.datetime.now() +
                            datetime.timedelta(minutes=self.fanOnDuration),
                            '%H:%M:%S')
        schedule.every().day.at(fanOffTime).do(self.fanOff)

    def fanOff(self):
        self.Actuator.turnFanOff()
        self.logger.debug('Fan switched Off')
        self.states.FAN_status = False
        return schedule.CancelJob

    def pumpOn(self):
        self.Actuator.turnPumpMixingOn()
        self.logger.debug('Mixing Pump switched ON')
        self.states.Pump_Mix_status = True
        pumpOffTime = format(datetime.datetime.now() +
                             datetime.timedelta(minutes=self.pumpOnDuration),
                             '%H:%M:%S')
        schedule.every().day.at(pumpOffTime).do(self.pumpOff)

    def pumpOff(self):
        self.Actuator.turnPumpMixingOff()
        self.logger.debug('Mixing Pump switched OFF')
        self.states.Pump_Mix_status = False
        return schedule.CancelJob

    def strtoDate(self, date):
        date = [int(x) for x in date.split('-')]
        result = datetime.date(date[0], date[1], date[2])
        return result
