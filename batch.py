from data_access import get_currency_data_from_cass, get_num_of_data_points

import numpy as np
from IPython.core.debugger import Tracer

hm_classes = 2


class CurrencyBatchManager(object):

	def __init__(self, base, counter, batch_size, input_days, look_ahead_days, test_percentage):
		self.base = base
		self.counter = counter
		self.batch_size = batch_size
		self.input_days = input_days
		self.look_ahead_days = look_ahead_days
		self.test_percentage = test_percentage
		self.train_percentage = 1 - test_percentage
		self.start_date = None

	def reset(self):
		self.start_date = None

	def change_currency(self, base, counter):
		print("Currency Pair changed to {}/{}".format(base, counter))
		self.base = base
		self.counter = counter
		self.reset()

	def get_next_batch(self):
		batch_x, batch_y = [], []
		for _ in range(self.batch_size):
			data = get_currency_data_from_cass(self.base, self.counter, date_low=self.start_date, limit=self.input_days+self.look_ahead_days)
			x = np.array([[x.open, x.close, x.high, x.low] for x in data[0:self.input_days]])
			x = reduce(lambda x,y: np.append(x,y), x)
			y = np.array([0, 1]) if data[self.input_days+self.look_ahead_days-1].close > data[self.input_days-1].close else np.array([1, 0])
			self.start_date = str(data[0].date)
			batch_x.append(x)
			batch_y.append(y)
		batch_x = np.array(batch_x)
		batch_y = np.array(batch_y)
		return batch_x, batch_y


	def hm_train_batches(self):
		return int(self.train_percentage * int((get_num_of_data_points(self.base, self.counter) - (self.input_days + self.look_ahead_days))/ self.batch_size))

	def hm_test_batches(self):
		return int(self.test_percentage * int((get_num_of_data_points(self.base, self.counter) - (self.input_days + self.look_ahead_days))/ self.batch_size)) 

	def get_test_batch(self):
		test_x = np.zeros((self.hm_test_batches() * self.batch_size, self.input_days * 4))
		test_y = np.zeros((self.hm_test_batches() * self.batch_size, hm_classes))
		x_val, y_val = 0, 0
		for _ in range(self.hm_test_batches()):
			x, y = self.get_next_batch()
			for val in x:
				test_x[x_val] = val
				x_val += 1
			for val in y:
				test_y[y_val] = val
				y_val += 1
		return test_x, test_y
