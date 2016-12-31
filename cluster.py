from cassandra.cluster import Cluster

def connect_to_cluster(keyspace='temp'):
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect(keyspace)
	return session

def disconnect_from_cluster(cluster):
	cluster.shutdown()
