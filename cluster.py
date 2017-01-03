from cassandra.cluster import Cluster

# cluster = Cluster(['127.0.0.1'])

def connect_to_cluster(keyspace='temp'):
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect(keyspace)
	return cluster, session

def disconnect_from_cluster(cluster):
	Cluster.shutdown(cluster)

class CassandraConnector(object):

	def __init__(self, ip_addr_list, keyspace):
		self.keyspace = keyspace
		self.cluster = Cluster(ip_addr_list)
		self.session = self.cluster.connect(self.keyspace)

	def reconnect(self):
		self.cluster.connect(self.keyspace)
	
	def disconnect_from_cluster(cluster):
		Cluster.shutdown(self.cluster)


