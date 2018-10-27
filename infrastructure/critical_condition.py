from lib.lib import *
from infrastructure.state import State
from growCycle import GrowCycle

grow_cycle = GrowCycle()


def check_critical_condition(sensor_data):
    """
    Check critical condition of the sensor data
    :parameter: sensor_data (dict) - sensor_data to check critical condition
    :return: report (dict)
    """
    temperature = sensor_data["temperature"]
    humidity = sensor_data["humidity"]
    waterlevel = sensor_data["waterlevel"]
    ph = sensor_data["ph"]
    ec = sensor_data["ec"]

    checklist = []

    # check temperature condition
    if grow_cycle.tempUL > temperature > grow_cycle.tempLL:
        checklist.append("OK")
    else:
        if temperature > grow_cycle.tempUL:
            checklist.append("UP")
        else:
            checklist.append("LOW")

    # check humidity condition
    if grow_cycle.humidityUL > humidity > grow_cycle.humidityLL:
        checklist.append("OK")
    else:
        if humidity > grow_cycle.humidityUL:
            checklist.append("UP")
        else:
            checklist.append("LOW")

    # check waterlevel condition
    if grow_cycle.waterlevelUL > waterlevel > grow_cycle.waterlevelLL:
        checklist.append("OK")
    else:
        if waterlevel > grow_cycle.tempUL:
            checklist.append("UP")
        else:
            checklist.append("LOW")

    # check Ph condition
    if grow_cycle.phUL > ph > grow_cycle.phLL:
        checklist.append("OK")
    else:
        if ph > grow_cycle.phUL:
            checklist.append("UP")
        else:
            checklist.append("LOW")

    # check EC condition
    if grow_cycle.ecUL > ec > grow_cycle.ecLL:
        checklist.append("OK")
    else:
        if ec > grow_cycle.ecUL:
            checklist.append("UP")
        else:
            checklist.append("LOW")

    return checklist


def track_critical_condition(cc_checklist):
    """
    Track a critical condition
    :parameter cc_checklist (string) : checklist of the critical sensor data
    :return: ret(boolean)
    """


    return
