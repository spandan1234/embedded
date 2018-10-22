from lib import *

growcycle = GrowCycle()
currentWeek = growcycle.getCurrentWeek()
estimatedHarvest = growcycle.estimatedHarvest
growcycle.schedCurrentWeek(currentWeek)

while(datetime.date.today() <= estimatedHarvest):
    while(growcycle.getCurrentWeek() == currentWeek):
        schedule.run_pending()
        time.sleep(1)
    currentWeek = growcycle.getCurrentWeek()
    growcycle.schedCurrentWeek(currentWeek)
