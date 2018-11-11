from configparser import ConfigParser
from growCycle import GrowCycle
import schedule
from data_acquisition.logger import *

logger = logger_variable(__name__, 'Log_files\\schedulerTest.log')

grow_cycle = GrowCycle()
grow_cycle.schedCurrentWeek('week0')

if grow_cycle.ledOnDuration != 0:
    schedule.every(grow_cycle.ledOnInterval).minute. \
        do(logger.info, msg='Led On')

# fan scheduling
if grow_cycle.fanOnDuration != 0:
    schedule.every(grow_cycle.fanOnInterval).minute. \
        do(logger.debug, msg='Fan On')

# pump_mixing scheduling
if grow_cycle.pumpOnDuration != 0:
    schedule.every(grow_cycle.pumpOnInterval).minute. \
        do(logger.info, msg='Switch on the Pump')

# data acquisition and image capture scheduling
schedule.every(grow_cycle.collectImageInterval).minutes. \
    do(logger.info, msg='Get Camera Data')
schedule.every(grow_cycle.collectDataInterval).minutes. \
    do(logger.info, msg='Get Sensor Data')

# schedule sending data to aws
schedule.every(grow_cycle.sendDataToAWSInterval).minute. \
    do(logger.info, msg='Send Sensor Data to AWS')

# schedule sending images to aws S3
schedule.every(grow_cycle.sendImagesToAWSInterval).minute. \
    do(logger.info, msg='Send Images to S3')


while True:
    schedule.run_pending()
