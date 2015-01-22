import os
import sys
import logging
from logging.handlers import RotatingFileHandler

import time
from datetime import datetime,date

class Log():

	def __init__(self, name):
		# Create the logger
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)

		# The format for the out
		formatter = logging.Formatter('%(asctime)s [ %(levelname)s ] : %(message)s')

		# Get the current date
		today_date = datetime.now()
		# Create the name with current date
		name = 'log_' + today_date.strftime("%Y%m%d_%H%M%S") + '.log'

		# The file log output
		file_handler = RotatingFileHandler(name, 'w', 1000000, 1)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

		# The steam output
		steam_handler = logging.StreamHandler()
		steam_handler.setLevel(logging.DEBUG)
		steam_handler.setFormatter(formatter)
		logger.addHandler(steam_handler)

		self.logger = logger
