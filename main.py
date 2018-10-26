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
        self.states = State()
        self.sensor_data = SensorData()
        self.actuator = ActuatorControl()
        self.camera_capture = CameraCapture()
        self.CC_Queue = Queue()
        self.Data_Queue = Queue()
        self.Image_Queue = Queue()
        self.AWS_Queue = Queue()
        self.AWS = AWSInterface()
        # initialize logger_variable
        self.logger = logger_variable(__name__, 'Log_files\\main.log')

    def main_function(self):
        estimated_harvest = self.grow_cycle.estimatedHarvest
        current_week = self.get_current_week()
        self.states.Current_Mode = "FOLLOW CONFIG"
        self.states.activated = False

        while datetime.date.today() <= estimated_harvest:

            # start weekly jobs
            while self.get_current_week() == current_week:
                # check the current activated mode
                if self.states.Current_Mode == "FOLLOW CONFIG" and not self.states.activated:
                    self.grow_cycle.schedCurrentWeek(current_week)
                    self.schedule_jobs()
                    self.states.activated = True

                elif self.states.Current_Mode == "WATER CHANGE" and not self.states.activated:
                    self.grow_cycle.schedCurrentWeek('water_change')
                    self.schedule_jobs()
                    self.states.activated = True

                elif self.states.Current_Mode == "PH DOSING" and not self.states.activated:
                    self.grow_cycle.schedCurrentWeek('ph_dosing')
                    self.schedule_jobs()
                    self.states.activated = True
                else:
                    self.logger.error('Wrong Mode of Operation')

                # check user input from AWS
                if not self.AWS_Queue.empty():
                    user_input = self.AWS_Queue.get()
                    self.check_user_input(user_input)

                # run scheduled jobs
                schedule.run_pending()
                time.sleep(1)

            # self.grow_cycle.schedCurrentWeek(current_week)

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
        self.states.activated = False

        return

    def schedule_jobs(self):
        """
        :parameter: creating scheduling jobs
        :return:
        """
        # led scheduling
        if self.grow_cycle.ledOnDuration != 0:
            schedule.every(self.grow_cycle.ledOnInterval).day.\
                do(self.grow_cycle.lightOn)

        # fan scheduling
        if self.grow_cycle.fanOnDuration != 0:
            schedule.every(self.grow_cycle.fanOnInterval).hour.\
                do(self.grow_cycle.fanOn)

        # pump_mixing scheduling
        if self.grow_cycle.pumpOnDuration != 0:
            schedule.every(self.grow_cycle.pumpOnInterval).hour.\
                do(self.grow_cycle.pumpOn)

        # data acquisition and image capture scheduling
        schedule.every(self.grow_cycle.collectImageInterval).minutes.\
            do(self.get_camera_data)
        schedule.every(self.grow_cycle.collectDataInterval).minutes.\
            do(self.data_acquisition_job)

        # schedule sending data to aws
        schedule.every(self.grow_cycle.sendDataToAWSInterval).hour.\
            do(self.send_data_to_aws)

        # schedule sending images to aws S3
        schedule.every(self.grow_cycle.sendImagesToAWSInterval).hour.\
            do(self.send_camera_data)

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
        # send the data to queue
        if critical_check.count("OK") < 5:
            track_critical_condition(critical_check)
            self.Data_Queue.put(data)
        else:
            self.Data_Queue.put(data)

        return

    # def interprete_item(self):
    #     return

    def get_camera_data(self):
        """
        get image and store it in the image_queue
        :return: no return
        """
        # get image data
        image = self.camera_capture.capture_image(frame_no=self.states.frame_no)
        self.Image_Queue.put(image)
        return

    def send_camera_data(self):
        """
        function to send image to aws
        :return: no return
        """
        while not self.Image_Queue.empty():
            # send images to AWS
            self.AWS.sendData(self.Image_Queue.get())
        return

    def send_data_to_aws(self):
        """
        send data to aws iot
        :return:no return
        """
        while not self.Data_Queue.empty():
            self.AWS.sendData(self.Data_Queue.get())
        return

    def get_current_week(self):
        """
        return current week
        :return: current_week (string): current week number
        """
        startdate = self.grow_cycle.growStartDate
        day_count = datetime.date.today() - startdate
        week_number = day_count.days // 7
        current_week = 'week'+str(week_number)
        return current_week


if __name__ == '__main__':
    central_control = Main()
    central_control.main_function()
