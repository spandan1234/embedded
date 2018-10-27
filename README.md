# Embedded Structure
## ActuatorControl
### init()
* Initialize GPIO pins for light, fan and pump
* Set them as output pins
### turnLightOn()
* Set the light pin to ON state
### turnLightOff()
* Set the light pin to OFF state
### turnFanOn()
* Set the fan pin to ON state
### turnFanOff()
* Set the fan pin to OFF state
### turnPumpOn()
* Set the pump pin to ON state
### turnPumpOff()
* Set the pump pin to OFF state

## AWSInterface
* Get device info from device.conf file
### init()
* Create AWSMQTT client
* Configure the endpoint
* Configure Credentials
* Establish connection between device and AWS
### sendData()
* send data to AWS on device topic
### receiveData()
* set up a receive handle for specific topic

## GrowCycle
### init()
* Get plant info from plant.conf file
* Get startDate and Estimated endDate
### startGrowCycle()
* Get current week
* while current day is before estimated harvest day
	* schedule current week
	* while current week is same as getCurrentWeek
		* Run pending tasks of that week
	* update current week
### schedCurrentWeek()
* Get the actuator control information of the week
* Set the Critical sensor values
* Schedule the lightOn, fanOn, pumpOn, getSensorData and getCameraData tasks
### getCurrentWeek()
* Get the current week of the cycle
### lightOn()
* Turn ON the light and schedule the lightOff task depending on the grow info
### lightOff()
* Turn OFF the ligth and cancel the lightOff job
### fanOn()
* Turn ON the fan and schedule the fanOff task depending on the grow info
### fanOff()
* Turn OFF the fan and cancel the fanOff job
### pumpOn()
* Turn ON the pump and schedule the pumpOff task depending on the grow info
### pumpOff()
* Turn OFF the pump and cancel the pumpOff job
### getSensorData()
* Collect the sensor data
* Check for critial values
* send data to AWS
### send_data_to_aws()
* send data to aws
### getCameraData()
* get the current image
### sendCameraToAWS()
* send Image to AWS S3
### strToDate()
* Convert string to date format
## plant.conf
* It contain plant info
* upper and lower limit of sensor values
* actuator control info
## device.conf
* contain device info
* wifi info
* aws info

## main.py
### init()
* grow_cycle - access the config file and make schedules
* sensor_data - receive data from the arduino
* CC_queue - critical condition queue
* Data_queue - queue containing data acquired
* Image_queue - queue containing images acquired
* AWS_queue - queue containing info received from AWS
* states - to track the current states of the actuator
* logger = logger variable to log logic
### main_function()
* get estimated harvest date
* get current week
* loop till today is not equal to estimatedHarvest
* get current week values from plant.conf file
* schedule actuator, data_acquisition, sendData jobs
* execute jobs
* check aws queue for user input
* if any: act upon user inputs

### check_user_input()
* check the message received from AWS
* change the current mode
* modes: FOLLOW CONFIG, WATER CHANGE, PH DOSING

### schedule_jobs()
* schedule light intervals
* schedule fan intervals
* schedule pump intervals
* schedule data acquisition and image capture intervals
* schedule sending data to aws
* schedule sending images to aws
### data_acquisition_job()
* get sensor data
* check for critical condition
* if critical send for tracking
* put the data in the Queue

### get_camera_data()
* get image data from camera
### send_data_to_aws()
* send data to AWS IoT
### get_current_week()
* get current week number

#state.py
* to track the states of actuators
* states of current mode
* states of tracker functions

# critical_condition.py
## check_critical_condition()
* check critical condition for all the sensor data
* input params: sensor data (dict)
* return: cc_checklist (list - "OK","UP", "DOWN")
## track_critical_condition()