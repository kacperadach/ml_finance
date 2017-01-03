import tensorflow as tf

from batch import CurrencyBatchManager

from IPython.core.debugger import Tracer

batch_size = 10
input_days = 30
data_per_day = 4
look_ahead_days = 3
test_percentage = 0.05

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 2

hm_epochs = 1

x = tf.placeholder('float', [None, input_days * data_per_day])
y = tf.placeholder('float')

def neural_network_model(data):

	hidden_1_layer = {'weights': tf.Variable(tf.random_normal([input_days * data_per_day, n_nodes_hl1])),
						'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

	hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
						'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

	hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
						'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}

	output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
						'biases': tf.Variable(tf.random_normal([n_classes]))}

	l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
	l1 = tf.nn.relu(l1)

	l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
	l2 = tf.nn.relu(l2)

	l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
	l3 = tf.nn.relu(l3)

	output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']
	return output

def train_neural_network(x):
	prediction = neural_network_model(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	batch_manager = CurrencyBatchManager(
		batch_size=input_days, 
		input_days=input_days, 
		look_ahead_days=look_ahead_days,
		test_percentage=test_percentage
	)

	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())

		for epoch in range(hm_epochs):
			print('Epoch {}'.format(epoch))
			epoch_loss = 0
			for batch_num in range(batch_manager.hm_batches()):
				print('Batch {}'.format(batch_num))
				epoch_x, epoch_y = batch_manager.get_next_batch()
				_, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y})
				epoch_loss += c
			print('Epoch {} completed out of {}, loss: {}'.format(epoch+1, hm_epochs, epoch_loss))


		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		test_x, test_y = batch_manager.get_test_batch()
		print('Accuracy: {}'.format(accuracy.eval({x: test_x, y: test_y})))

train_neural_network(x)