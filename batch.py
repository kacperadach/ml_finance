from data_access import get_currency_data_from_cass, get_num_of_data_points

BASE = 'EUR'
COUNTER = 'NOK'

class CurrencyBatchManager(object):

	def __init__(self, batch_size, days_ahead, start_date=None):
		self.last_date = start_date
		self.batch_size = batch_size
		self.days_ahead = days_ahead

	def get_next_batch(self):
		data = get_currency_data_from_cass(BASE, COUNTER, date_low=self.last_date, limit=self.batch_size)
		past_price = data[self.batch_size-1]
		self.last_date = str(data[self.batch_size-1].date)
		future_price = get_currency_data_from_cass(BASE, COUNTER, date_low=self.last_date, limit=self.days_ahead+1)[self.days_ahead].close
		label = [0, 1] if future_price > past_price else [1, 0]
		return data, label

	def hm_batches(self):
		return int((get_num_of_data_points(BASE, COUNTER) - self.days_ahead)/ self.batch_size)

