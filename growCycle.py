from lib import *


class GrowCycle():
		
	def __init__(self):
		parser = SafeConfigParser()
		parser.read('plant.Conf')
		self.growStartDate = parser.get('PlantInfo','plantingDate')
		self.estimatedHarvest = parser.get('PlantInfo','estimatedHarvest')
		self.growStartDate = GrowCycle.strtoDate(self.growStartDate)
		self.estimatedHarvest = GrowCycle.strtoDate(self.estimatedHarvest)
		self.ledOnDuration=None
		self.ledOnInterval=None
		self.fanOnDuration=None
		self.fanOnInterval=None
		self.pumpOnDuration=None
		self.pumpOnInterval=None
		self.collectDataInterval=2
		self.collectImageInterval=2
		# self.IoT = IoT()
		# self.Accuator = AccuatorControl()
		# self.Sensor = SensorControl()
		

	def strtoDate(date):
		date = [int(x) for x in date.split('-')]
		result = datetime.date(date[0],date[1],date[2])
		return result

	def getCurrentWeek(self):
		startdate = self.growStartDate
		dayCount = datetime.date.today()-startdate
		currentWeek = dayCount.days//7
		return currentWeek

	@logging
	def schedCurrentWeek(self,currentWeek):
		parser = SafeConfigParser()
		parser.read('plant.Conf')
		#accuator = AccuatorControl()
		self.tempUL = int(parser.get('week'+str(currentWeek),'tempUL'))
		self.tempLL = int(parser.get('week'+str(currentWeek),'tempLL'))
		self.humidityUL = int(parser.get('week'+str(currentWeek),'humidityUL'))
		self.humidityLL = int(parser.get('week'+str(currentWeek),'humidityLL'))
		self.phUL = float(parser.get('week'+str(currentWeek),'phUL'))
		self.phLL = float(parser.get('week'+str(currentWeek),'phLL'))
		self.ecUL = float(parser.get('week'+str(currentWeek),'ecUL'))
		self.ecLL = float(parser.get('week'+str(currentWeek),'ecLL'))
		self.waterlevelUL = int(parser.get('week'+str(currentWeek),'waterlevelUL'))
		self.waterlevelLL = int(parser.get('week'+str(currentWeek),'waterlevelLL'))
		self.ledOnDuration = int(parser.get('week'+str(currentWeek),'ledOnDuration'))
		self.ledOnInterval = int(parser.get('week'+str(currentWeek),'ledOnInterval'))
		self.fanOnDuration = int(parser.get('week'+str(currentWeek),'fanOnDuration'))
		self.fanOnInterval = int(parser.get('week'+str(currentWeek),'fanOnInterval'))
		self.pumpOnDuration = int(parser.get('week'+str(currentWeek),'pumpOnDuration'))
		self.pumpOnInterval = int(parser.get('week'+str(currentWeek),'pumpOnInterval'))
		self.collectDataInterval = int(parser.get('week'+str(currentWeek),'collectDataInterval'))
		self.collectDataDuration = int(parser.get('week'+str(currentWeek),'collectDataDuration'))
		self.collectCameraInterval = int(parser.get('week'+str(currentWeek),'collectCameraInterval'))
		self.collectCameraDuration = int(parser.get('week'+str(currentWeek),'collectCameraDuration'))

		schedule.clear()
		
		# if self.ledOnDuration!=0:
		# 	schedule.every(self.ledOnInterval).day.do(self.lightOn)

		# if self.fanOnDuration!=0:
		# 	schedule.every(self.fanOnInterval).hour.do(self.fanOn)

		# if self.pumpOnDuration!=0:
		# 	schedule.every(self.pumpOnInterval).hour.do(self.pumpOn)

		schedule.every(self.collectCameraInterval).seconds.do(self.getCameraData)
		schedule.every(self.collectDataInterval).minutes.do(self.getSensorData)

	@logging
	def lightOn(self):
		accuator.turnLightOn()
		lightOffTime = format(datetime.datetime.now() + datetime.timedelta(hours=self.ledOnDuration),'%H:%M:%S')
		schedule.every().day.at(lightOffTime).do(self.lightOff)

	@logging
	def lightOff(self):
		accuator.turnLightOff()
		return schedule.CancelJob

	@logging
	def fanOn(self):
		accuator.turnFanOn()
		fanOffTime = format(datetime.datetime.now() + datetime.timedelta(minutes=self.fanOnDuration),'%H:%M:%S')
		schedule.every().day.at(fanOffTime).do(self.fanOff)

	@logging
	def fanOff(self):
		accuator.turnFanOff()
		return schedule.CancelJob

	@logging
	def pumpOn(self):
		accuator.turnPumpOn()
		pumpOffTime = format(datetime.datetime.now() + datetime.timedelta(minutes=self.pumpOnDuration),'%H:%M:%S')
		schedule.every().day.at(pumpOffTime).do(self.pumpOff)

	@logging
	def pumpOff(selfself):
		accuator.turnPumpOff()
		return schedule.CancelJob

	@logging
	def getSensorData(self):
		print("inside get sensor")
		# sensorData = sensor.sensorData()
		# checkSensorData(sensorData)
		# self.sendDataToIoT(sensorData)

	@logging
	def sendDataToIoT(self,data):
		IoT.sendData(data)

	@logging
	def getCameraData(self):
		print("inside camera sensor data")

	@logging
	def sendCameraToIoT(self):
		IoT.sendCameraData()

	










