import lib 

class ActuatorControl():

	def __init__()
		self.light_out = 23
		self.fan_out = 24
		self.pump_out = 25 

		GPIO.setmode(GPIO.BCM)

		#using GPIO 23 24 25

		GPIO.setup(self.light_out, GPIO.OUT)
		GPIO.setup(self.fan_out, GPIO.OUT)
		GPIO.setup(self.motor_out, GPIO.OUT)

	def turnLightOn(self):
		light_state = 0x01
		GPIO.output(self.light_out,light_state)

	def turnLightOff(self):
		light_state = 0x00
		GPIO.output(self.light_out,light_state)

	def turnMotorOn(self):
		motor_state = 0x01
		GPIO.output(self.motor_out,motor_state)
	
	def turnMotorOff(self):
		motor_state = 0x00
		GPIO.output(self.motor_out,motor_state)

	def turnfanOn(self):
		fan_state = 0x01
		GPIO.output(self.fan_out,fan_state)

	def turnFanOff(self):
		fan_state = 0x00
		GPIO.output(self.fan_out,fan_state)