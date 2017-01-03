from data_access import get_currency_data_from_cass, get_num_of_data_points

import numpy as np
from IPython.core.debugger import Tracer

BASE = 'EUR'
COUNTER = 'NOK'

class CurrencyBatchManager(object):

	def __init__(self, batch_size, input_days, look_ahead_days, test_percentage):
		self.batch_size = batch_size
		self.input_days = input_days
		self.look_ahead_days = look_ahead_days
		self.test_percentage = test_percentage
		self.train_percentage = 1 - test_percentage
		self.start_date = None

	def get_next_batch(self):
		try:
			batch_x, batch_y = [], []
			for _ in range(self.batch_size):
				data = get_currency_data_from_cass(BASE, COUNTER, date_low=self.start_date, limit=self.input_days+self.look_ahead_days)
				x = np.array([[x.open, x.close, x.high, x.low] for x in data[0:self.input_days]])
				x = reduce(lambda x,y: np.append(x,y), x)
				y = np.array([0, 1]) if data[self.input_days+self.look_ahead_days-1].close > data[self.input_days-1].close else np.array([1, 0])
				self.start_date = str(data[1].date)
				batch_x.append(x)
				batch_y.append(y)
			batch_x = np.array(batch_x)
			batch_y = np.array(batch_y)
			return batch_x, batch_y
		except:
			Tracer()()


	def hm_batches(self):
		return int(self.train_percentage * int((get_num_of_data_points(BASE, COUNTER) - (self.input_days + self.look_ahead_days))/ self.batch_size))

	def get_test_batch(self):
		x, y = self.get_next_batch()
		return x, y