import RPi.GPIO as GPIO


class ActuatorControl:
    def __init__(self):
        self.interrupt = 19
        self.led_out = 21
        self.fan_out = 22
        self.pump_mixing_out = 23
        self.pump_pour_out = 24

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.interrupt, GPIO.OUT, initial=0)
        GPIO.setup(self.led_out, GPIO.OUT, initial=0)
        GPIO.setup(self.fan_out, GPIO.OUT, initial=0)
        GPIO.setup(self.pump_mixing_out, GPIO.OUT, initial=0)
        GPIO.setup(self.pump_pour_out, GPIO.OUT, initial=0)

    def turnLightOn(self):
        light_state = 0x01
        GPIO.output(self.light_out, light_state)

    def turnLightOff(self):
        light_state = 0x00
        GPIO.output(self.light_out, light_state)

    def turnMotorOn(self):
        motor_state = 0x01
        GPIO.output(self.motor_out, motor_state)

    def turnMotorOff(self):
        motor_state = 0x00
        GPIO.output(self.motor_out, motor_state)

    def turnfanOn(self):
        fan_state = 0x01
        GPIO.output(self.fan_out, fan_state)

    def turnFanOff(self):
        fan_state = 0x00
        GPIO.output(self.fan_out, fan_state)
