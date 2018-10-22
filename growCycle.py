from lib import *


class GrowCycle:

    def __init__(self):
        parser = ConfigParser()
        parser.read('plant.Conf')
        self.growStartDate = parser.get('PlantInfo', 'plantingDate')
        self.estimatedHarvest = parser.get('PlantInfo', 'estimatedHarvest')
        self.growStartDate = GrowCycle.strtoDate(self.growStartDate)
        self.estimatedHarvest = GrowCycle.strtoDate(self.estimatedHarvest)
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
        self.Sensor = SensorData()

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
        self.collectCameraInterval = int(parser.get(
            'week'+str(currentWeek), 'collectCameraInterval'))
        self.collectCameraDuration = int(parser.get(
            'week'+str(currentWeek), 'collectCameraDuration'))

        schedule.clear()

        if self.ledOnDuration != 0:
            schedule.every(self.ledOnInterval).day.do(self.lightOn)

        if self.fanOnDuration != 0:
            schedule.every(self.fanOnInterval).hour.do(self.fanOn)

        if self.pumpOnDuration != 0:
            schedule.every(self.pumpOnInterval).hour.do(self.pumpOn)

        schedule.every(self.collectCameraInterval).seconds\
            .do(self.getCameraData)
        schedule.every(self.collectDataInterval).minutes.do(self.getSensorData)

    def getCurrentWeek(self):
        startdate = self.growStartDate
        dayCount = datetime.date.today()-startdate
        currentWeek = dayCount.days//7
        return currentWeek

    def lightOn(self):
        self.Actuator.turnLightOn()
        lightOffTime = format(datetime.datetime.now() +
                              datetime.timedelta(hours=self.ledOnDuration),
                              '%H:%M:%S')
        schedule.every().day.at(lightOffTime).do(self.lightOff)

    def lightOff(self):
        self.Actuator.turnLightOff()
        return schedule.CancelJob

    def fanOn(self):
        self.Actuator.turnFanOn()
        fanOffTime = format(datetime.datetime.now() +
                            datetime.timedelta(minutes=self.fanOnDuration),
                            '%H:%M:%S')
        schedule.every().day.at(fanOffTime).do(self.fanOff)

    def fanOff(self):
        self.Actuator.turnFanOff()
        return schedule.CancelJob

    def pumpOn(self):
        self.Actuator.turnPumpOn()
        pumpOffTime = format(datetime.datetime.now() +
                             datetime.timedelta(minutes=self.pumpOnDuration),
                             '%H:%M:%S')
        schedule.every().day.at(pumpOffTime).do(self.pumpOff)

    def pumpOff(self):
        self.Actuator.turnPumpOff()
        return schedule.CancelJob

    def getSensorData(self):
        print("inside get sensor")
        # sensorData = sensor.sensorData()
        # checkSensorData(sensorData)
        # self.sendDataToIoT(sensorData)

    def sendDataToIoT(self, data):
        self.AWS.sendData(data)

    def getCameraData(self):
        print("inside camera sensor data")

    def sendCameraToIoT(self):
        self.AWS.sendCameraData()

    def strtoDate(date):
        date = [int(x) for x in date.split('-')]
        result = datetime.date(date[0], date[1], date[2])
        return result
