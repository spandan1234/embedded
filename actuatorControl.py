import lib 

class ActuatorControl():
	light_out = 23
	fan_out = 24
	pump_out = 25 

	GPIO.setmode(GPIO.BCM)

	#using GPIO 23 24 25 17 27 22

	GPIO.setup(light_out, GPIO.OUT)
	GPIO.setup(fan_out, GPIO.OUT)
	GPIO.setup(motor_out, GPIO.OUT)

	def turnLightOn(self):
		light_state = 0x01
		GPIO.output(ActuatorControl.light_out,light_state)

	def turnLightOff(self):
		light_state = 0x00
		GPIO.output(ActuatorControl.light_out,light_state)

	def turnMotorOn(self):
		motor_state = 0x01
		GPIO.output(ActuatorControl.motor_out,motor_state)
	
	def turnMotorOff(self):
		motor_state = 0x00
		GPIO.output(ActuatorControl.motor_out,motor_state)

	def turnfanOn(self):
		fan_state = 0x01
		GPIO.output(ActuatorControl.fan_out,fan_state)

	def turnFanOff(self):
		fan_state = 0x00
		GPIO.output(ActuatorControl.fan_out,fan_state)