from lib import *
from os import path
import os


class GrowCycle:

    def __init__(self):
        parser = ConfigParser()
        # get current working directory
        cwd = os.getcwd()
        # check if file is present
        if path.isfile(cwd+"/config_files/plant.conf"):
            parser.read('plant.Conf')
        self.growStartDate = parser.get('PlantInfo', 'plantingDate')
        self.estimatedHarvest = parser.get('PlantInfo', 'estimatedHarvest')
        self.growStartDate = self.strtoDate(self.growStartDate)
        self.estimatedHarvest = self.strtoDate(self.estimatedHarvest)
        self.ledOnDuration = None
        self.ledOnInterval = None
        self.fanOnDuration = None
        self.fanOnInterval = None
        self.pumpOnDuration = None
        self.pumpOnInterval = None
        self.collectDataInterval = 2
        self.collectImageInterval = 2
        self.AWS = AWSInterface()
        self.self.Actuator = self.ActuatorControl()
        self.states = State()
        self.Sensor = SensorData()
        self.CameraCapture = CameraCapture()

    def startGrowCycle(self):
        currentWeek = self.getCurrentWeek()

        while(datetime.date.today() <= self.estimatedHarvest):
            self.schedCurrentWeek(currentWeek)
            while(self.getCurrentWeek() == currentWeek):
                schedule.run_pending()
                time.sleep(1)
            currentWeek = self.getCurrentWeek()

    def schedCurrentWeek(self, currentWeek):
        parser = ConfigParser()
        parser.read('plant.Conf')
        # get plant critical data
        self.tempUL = int(parser.get('week'+str(currentWeek), 'tempUL'))
        self.tempLL = int(parser.get('week'+str(currentWeek), 'tempLL'))
        self.humidityUL = int(parser.get('week'+str(currentWeek),
                                         'humidityUL'))
        self.humidityLL = int(parser.get('week'+str(currentWeek),
                                         'humidityLL'))
        self.phUL = float(parser.get('week'+str(currentWeek), 'phUL'))
        self.phLL = float(parser.get('week'+str(currentWeek), 'phLL'))
        self.ecUL = float(parser.get('week'+str(currentWeek), 'ecUL'))
        self.ecLL = float(parser.get('week'+str(currentWeek), 'ecLL'))
        self.waterlevelUL = int(parser.get('week'+str(currentWeek),
                                           'waterlevelUL'))
        self.waterlevelLL = int(parser.get('week'+str(currentWeek),
                                           'waterlevelLL'))
        self.ledOnDuration = int(parser.get('week'+str(currentWeek),
                                            'ledOnDuration'))
        self.ledOnInterval = int(parser.get('week'+str(currentWeek),
                                            'ledOnInterval'))
        self.fanOnDuration = int(parser.get('week'+str(currentWeek),
                                            'fanOnDuration'))
        self.fanOnInterval = int(parser.get('week'+str(currentWeek),
                                            'fanOnInterval'))
        self.pumpOnDuration = int(parser.get('week'+str(currentWeek),
                                             'pumpOnDuration'))
        self.pumpOnInterval = int(parser.get('week'+str(currentWeek),
                                             'pumpOnInterval'))
        self.collectDataInterval = int(parser.get('week'+str(currentWeek),
                                                  'collectDataInterval'))
        self.collectDataDuration = int(parser.get('week'+str(currentWeek),
                                                  'collectDataDuration'))
        self.collectCameraInterval = int(parser.get('week'+str(currentWeek),
                                                    'collectCameraInterval'))
        self.collectCameraDuration = int(parser.get('week'+str(currentWeek),
                                                    'collectCameraDuration'))

        schedule.clear()
        self.initialize_states()

    def initialize_states(self):
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
        return

    def getCurrentWeek(self):
        startdate = self.growStartDate
        dayCount = datetime.date.today()-startdate
        currentWeek = dayCount.days//7
        return currentWeek

    def lightOn(self):
        self.Actuator.turnLightOn()
        self.states.LED_status = True
        lightOffTime = format(datetime.datetime.now() +
                              datetime.timedelta(hours=self.ledOnDuration),
                              '%H:%M:%S')
        schedule.every().day.at(lightOffTime).do(self.lightOff)

    def lightOff(self):
        self.Actuator.turnLightOff()
        self.states.LED_status = False
        return schedule.CancelJob

    def fanOn(self):
        self.Actuator.turnFanOn()
        self.states.FAN_status = True
        fanOffTime = format(datetime.datetime.now() +
                            datetime.timedelta(minutes=self.fanOnDuration),
                            '%H:%M:%S')
        schedule.every().day.at(fanOffTime).do(self.fanOff)

    def fanOff(self):
        self.Actuator.turnFanOff()
        self.states.FAN_status = False
        return schedule.CancelJob

    def pumpOn(self):
        self.Actuator.turnPumpOn()
        self.states.Pump_Mix_status = True
        pumpOffTime = format(datetime.datetime.now() +
                             datetime.timedelta(minutes=self.pumpOnDuration),
                             '%H:%M:%S')
        schedule.every().day.at(pumpOffTime).do(self.pumpOff)

    def pumpOff(self):
        self.Actuator.turnPumpOff()
        self.states.Pump_Mix_status = False
        return schedule.CancelJob

    def send_data_to_aws(self, data):
        self.AWS.sendData(data)

    # def sendCameraToIoT(self):
    #     self.AWS.sendCameraData()

    def strtoDate(date):
        date = [int(x) for x in date.split('-')]
        result = datetime.date(date[0], date[1], date[2])
        return result
