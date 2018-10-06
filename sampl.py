import datetime

curentdate = '2018-06-12'
curentdate= [int(x) for x in curentdate.split('-')]
print(datetime.date.today()-datetime.date(curentdate[0],curentdate[1],curentdate[2]))
current_time = datetime.datetime.now()
light_on_time = current_time.replace(hour=3, minute=0)
print(light_on_time)