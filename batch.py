from data_access import get_currency_data_from_cass, get_num_of_data_points

import numpy as np

BASE = 'EUR'
COUNTER = 'NOK'

INPUT_DAYS = 30
LOOK_AHEAD_DAYS = 3

class CurrencyBatchManager(object):

	def __init__(self, batch_size, input_days, look_ahead_days):
		self.batch_size = batch_size
		self.input_days = input_days
		self.look_ahead_days = look_ahead_days
		self.start_date = None

	def get_next_batch(self):
		batch_x, batch_y = np.array(), np.array()
		for _ in range(self.batch_size):
			data = get_currency_data_from_cass(BASE, COUNTER, date_low=self.last_date, limit=self.input_days+self.look_ahead_days)
			x = np.array(data[0:self.input_days-1])
			y = np.array([0, 1]) if data[self.input_days+self.look_ahead_days-1].close > past_price else np.array([1, 0])
			self.start_date = str(data[1].date)
			np.append(batch_x, x)
			np.append(batch_y, y)
		return batch_x, batch_y

	def hm_batches(self):
		return int((get_num_of_data_points(BASE, COUNTER) - (self.input_days + self.look_ahead_days))/ self.batch_size)

	# def get_test_batch(self, size):
