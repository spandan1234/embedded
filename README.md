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
*Set the fan pin to OFF state
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
### strToDate()
* Convert string to date format
### getCurrentWeek()
* Get the current week of the cycle
### schedCurrentWeek()
* Get the actuator control information of the week
* Set the Critical sensor values 
* Schedule the lightOn, fanOn, pumpOn, getSensorData and getCameraData tasks
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
### sendDataToAWS()
* send data to aws 
### getCameraData()
* get the current image
### sendCameraToAWS()
* send Image to AWS S3
## plant.conf
* It contain plant info
* upper and lower limit of sensor values
* actuator control info
## device.conf
* contain device info
* wifi info
* aws info



