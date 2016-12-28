from datetime import datetime

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import ValidationError

from data_access import get_data_file_names, open_csv_file, get_currency_pair_from_file_name
from models import CurrencyPair, CurrencyPairValue

# CQLENG_ALLOW_SCHEMA_MANAGEMENT

FILE_NAME = 'AUDCAD_Candlestick_1_D_BID_17.11.1992-24.12.2016.csv'

def start_connection():
	connection.setup(['127.0.0.1'], "temp", protocol_version=3)
	sync_table(CurrencyPair)
	sync_table(CurrencyPairValue)

def map_data_from_file(file_name):
	try:
		lines = open_csv_file(file_name)
		base, counter = get_currency_pair_from_file_name(file_name)
		print('Mapping data for currency pair: {}/{}'.format(base, counter))
		curPair = CurrencyPair.create(base=base, counter=counter)
		for l in lines[1:]:
			l = l.split(',')
			value_date = datetime.strptime(l[0].split(' ')[0], '%d.%m.%Y')
			CurrencyPairValue.create(
				base=base,
				counter=counter, 
				date=value_date, 
				open=float(l[1]), 
				high=float(l[2]), 
				low=float(l[3]), 
				close=float(l[4]), 
				volume=float(l[5].strip('\r\n'))
			)
	except ValidationError:
		print('Not mapping for currency pair: {}/{}'.format(base, counter))

def map_all_files():
	all_files = get_data_file_names()
	for file_name in all_files:
		map_data_from_file(file_name)

if __name__ == "__main__":
	start_connection()
	map_all_files()

