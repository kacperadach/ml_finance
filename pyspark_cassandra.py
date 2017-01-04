import subprocess
import sys

PYSPARK_CASSANDRA_VERSION = '0.3.5'

def run_spark_script(script_name):
	pyspark_cassandra_str = 'TargetHolding/pyspark-cassandra:{}'.format(PYSPARK_CASSANDRA_VERSION)
	subprocess.call(['spark-submit', '--packages', pyspark_cassandra_str, script_name])

if __name__ == "__main__":
	try:
		run_spark_script(sys.argv[1])
	except IOError:
		print('No script provided')
