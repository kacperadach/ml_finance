import os
from datetime import datetime

from cluster import connect_to_cluster, disconnect_from_cluster
from models import CurrencyPair, CurrencyPairValue


FILE_NAME = '/home/kacper/apps/forex_data/AUDCAD_Candlestick_1_D_BID_17.11.1992-24.12.2016.csv'
DATA_PATH = '/home/kacper/apps/forex_data/'

def get_currency_pair_from_file_name(file_name):
	base = file_name[0:3]
	counter = file_name[3:6]
	return base, counter

def get_data_file_names(dirpath='/home/kacper/apps/forex_data'):
	return os.listdir(dirpath)

def open_csv_file(file_name):
	with open(os.path.join(DATA_PATH, file_name), 'r') as f:
		return f.readlines()

def get_currency_data_from_cass(base, counter):
	session = connect_to_cluster()
	cql_query = "SELECT * FROM currency_pair_value WHERE base = '{}' AND counter = '{}' ALLOW FILTERING".format(base.upper(), counter.upper())
	rows = session.execute(cql_query)
	return rows

if __name__ == "__main__":
	a = get_currency_data_from_cass(base="EUR", counter="USD")
	print(len(a))



