from lib import *


class GrowCycle():
		
	def __init__(self):
		''' intialize the actuator duration varibles 
			sensor critical limits and start end date of grow'''
		parser = SafeConfigParser()
		parser.read('plant.Conf')
		self.startGrow = True
		self.growStartDate = parser.get('PlantInfo','plantingDate')
		self.estimatedHarvest = parser.get('PlantInfo','estimatedHarvest')
		self.growStartDate = strtoDate(self.growStartDate)
		self.estimatedHarvest = strtoDate(self.estimatedHarvest)
		self.tempUL = None
		self.tempLL = None
		self.humidityUL = None
		self.humidityLL = None
		self.phUL = None
		self.phLL = None
		self.ecUL = None
		self.ecLL = None
		self.waterlevelUL = None
		self.waterlevelLL = None
		self.ledOnDuration = None
		self.ledOnInterval = None
		self.fanOnDuration = None
		self.fanOnInterval = None
		self.pumpOnDuration = None
		self.pumpOnInterval = None
		self.collectDataInterval = 30
		self.collectImageInterval = 60
		self.AWS = AWSInterface()
		self.Accuator = AccuatorControl()
		self.Sensor = SensorData()
		
	@logging
	def startGrowCycle():
		'''Get the current week and schedule the grow varibles for current week
			loop schedule current week till day reachs the estimated harvest date'''
		currentWeek = self.getCurrentWeek()
		
		while(datetime.date.today()<=self.estimatedHarvest and self.startGrow):
			self.schedCurrentWeek(currentWeek)
			while(self.getCurrentWeek()==currentWeek and self.startGrow):
				schedule.run_pending()
				time.sleep(1)
			currentWeek = self.getCurrentWeek()

	@logging
	def endGrowCycle():
		'''turn off all actuators
			cancel all scheduled jobs
			send current stauts report to aws'''
		self.startGrow = False
		accuator.turnLigthOff()
		accuator.turnFanOff()
		accuator.turnPumpOff()
		schedule.clear()


	@logging
	def schedCurrentWeek(self,currentWeek):
		''' get the current week crtical limits of sensors and actuators 
		    schedule them accordingly'''
		parser = SafeConfigParser()
		parser.read('plant.Conf')
		
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
		
		schedule.clear()
		
		if self.ledOnDuration!=0:
			schedule.every(self.ledOnInterval).day.do(self.lightOn)

		if self.fanOnDuration!=0:
			schedule.every(self.fanOnInterval).hour.do(self.fanOn)

		if self.pumpOnDuration!=0:
			schedule.every(self.pumpOnInterval).hour.do(self.pumpOn)

		schedule.every(self.collectImageInterval).minutes.do(self.getCameraData)
		schedule.every(self.collectDataInterval).minutes.do(self.getSensorData)

	def getCurrentWeek(self):
		startdate = self.growStartDate
		dayCount = datetime.date.today()-startdate
		currentWeek = dayCount.days//7
		return currentWeek

	@logging
	def lightOn(self):
		''' turn ON the lights and auto schedule turn off depending on ON duration'''
		accuator.turnLightOn()
		lightOffTime = format(datetime.datetime.now() + datetime.timedelta(hours=self.ledOnDuration),'%H:%M:%S')
		schedule.every().day.at(lightOffTime).do(self.lightOff)

	@logging
	def lightOff(self):
		''' turn off the lights and auto cancel schedule turn off '''
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
		# collects the sensor data 
		print("inside get sensor")
		# sensorData = sensor.sensorData()
		# checkSensorData(sensorData)
		# self.sendDataToIoT(sensorData)

	@logging
	def sendDataToIoT(self,data):
		''':type data: dictonary {}
        :rtype: status: bool'''
		status = AWS.sendData(data)
		return status

	@logging
	def getCameraData(self):
		print("inside camera sensor data")

	@logging
	def sendCameraToIoT(self,data):
		''':type data: str
        :rtype: status: bool'''
		AWS.sendCameraData(data)
		return status

	











