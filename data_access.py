import os
from datetime import datetime

from cluster import connect_to_cluster, disconnect_from_cluster
from models import CurrencyPair, CurrencyPairValue
from currencies import CURRENCIES

FILE_NAME = '/home/kacper/apps/forex_data/AUDCAD_Candlestick_1_D_BID_17.11.1992-24.12.2016.csv'
DATA_PATH = '/home/kacper/apps/forex_data/'


def get_currency_pair_from_file_name(file_name):
	base = file_name[0:3]
	counter = file_name[3:6]
	return base, counter

def get_data_file_names(dirpath='/home/kacper/apps/forex_data'):
	return os.listdir(dirpath)

def get_all_currency_pairs():
	all_currencies = []
	all_files = get_data_file_names()
	for f in all_files:
		base, counter = get_currency_pair_from_file_name(f)
		if base in CURRENCIES and counter in CURRENCIES:
			all_currencies.append((base, counter))
	return all_currencies

def open_csv_file(file_name):
	with open(os.path.join(DATA_PATH, file_name), 'r') as f:
		return f.readlines()

def get_currency_data_from_cass(base, counter, date_low=None, date_high=None, limit=100):

	# format dates as 2016-12-01
	
	cluster, session = connect_to_cluster()
	cql_query = "SELECT * FROM currency_pair_value WHERE base = '{}' AND counter = '{}'".format(base.upper(), counter.upper())
	if date_low:
		cql_query += " AND date >= '{}'".format(date_low)
	if date_high:
		cql_query += " AND date <= '{}'".format(date_high)
	cql_query += " LIMIT {} ALLOW FILTERING".format(limit)
	rows = map(lambda x: x, session.execute(cql_query))
	disconnect_from_cluster(cluster)
	return rows

def get_num_of_data_points(base, counter):
	cluster, session = connect_to_cluster()
	cql_query = "SELECT count(*) FROM currency_pair_value WHERE base = '{}' AND counter = '{}'".format(base.upper(), counter.upper())
	count = session.execute(cql_query)
	disconnect_from_cluster(cluster)
	return count[0].count

if __name__ == "__main__":
	a = get_currency_data_from_cass(base="EUR", counter="USD")
	print(len(a))



