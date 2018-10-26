from lib import *
from growCycle import GrowCycle
from queue import Queue


class Main:
    def __init__(self):
        """
        :param: grow_cycle - access the config file and make schedules
                sensor_data - receive data from the arduino
                CC_queue - critical condition queue
                Data_queue - queue containing data acquired
                Image_queue - queue containing images acquired
                AWS_queue - queue containing info received from AWS
                states - to track the current states of the actuator
        """
        self.grow_cycle = GrowCycle()
        self.currentWeek = self.grow_cycle.getCurrentWeek()
        self.states = State()
        self.sensor_data = SensorData()
        self.actuator = ActuatorControl()
        self.camera_capture = CameraCapture()
        self.CC_Queue = Queue()
        self.Data_Queue = Queue()
        self.Image_Queue = Queue()
        self.AWS_Queue = Queue()

    def main_function(self):
        estimated_harvest = self.grow_cycle.estimatedHarvest
        current_week = self.grow_cycle.getCurrentWeek()
        self.grow_cycle.schedCurrentWeek(current_week)
        return

    def check_user_input(self, user_data):
        """

        :param user_data: data received from AWS
        :return: no return
        """
        # convert the json to dict
        data = json.loads(user_data)
        new_mode = None

        # assign the new mode to current mode in state
        if data["activity"] is "mode change":
            new_mode = data["mode"]
        self.states.Current_Mode = new_mode

        return

    def AWS(self):
        return

    def actuator_job(self):
        """
        :parameter: creating scheduling jobs
        :return:
        """
        # led scheduling
        if self.grow_cycle.ledOnDuration != 0:
            schedule.every(self.grow_cycle.ledOnInterval).day.do(self.grow_cycle.lightOn)

        # fan scheduling
        if self.grow_cycle.fanOnDuration != 0:
            schedule.every(self.grow_cycle.fanOnInterval).hour.do(self.grow_cycle.fanOn)

        # pump_mixing scheduling
        if self.grow_cycle.pumpOnDuration != 0:
            schedule.every(self.grow_cycle.pumpOnInterval).hour.do(self.grow_cycle.pumpOn)

        # data acquisition and image capture scheduling
        schedule.every(self.grow_cycle.collectImageInterval).minutes.do(self.getCameraData)
        schedule.every(self.grow_cycle.collectDataInterval).minutes.do(self.data_acquisition_job)

        return

    def data_acquisition_job(self):
        """
        :parameter: data - get sensor data
        :parameter: critical_check - get critical condition check data
        :return:
        """
        # get sensor data
        data = self.sensor_data.get_data()

        # send data for critical check
        critical_check = check_critical_condition(sensor_data=data)

        # evaluate the critical condition checklist
        if critical_check.count("OK") < 5:
            track_critical_condition(critical_check)
            self.Data_Queue.put(data)
        else:
            self.Data_Queue.put(data)
        return

    def interprete_item(self):
        return

    def getCameraData(self):
        """
        get image and store it in the image_queue
        :return: no return
        """
        # get image data
        image = self.camera_capture.capture_image(frame_no=self.states.frame_no)
        self.Image_Queue.put(image)
        return

