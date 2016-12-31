from data_access import get_currency_data_from_cass

# def get_next_batch(batch_size):


a = get_currency_data_from_cass('EUR', 'USD')[0:10]
for b in a:
	print(b)
	print('\n')