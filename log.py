import functools
import datetime

def logging(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		file = open("log.txt","a")
		file.write('LOG: "%s" :Running job "%s" \n' % (datetime.datetime.now(),func.__name__))
		result = func(*args, **kwargs)
		file.write('LOG: "%s" :Job "%s" completed \n' % (datetime.datetime.now(),func.__name__))
		return result
	return wrapper


if __name__ == '__main__':
		logging()	