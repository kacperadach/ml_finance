import tensorflow as tf

from batch import CurrencyBatchManager

batch_size = 10
input_days = 30
look_ahead_days = 3

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 2

x = tf.placeholder('float', [input_days, 4])
y = tf.placeholder('float')

def neural_network_model(data):

	hidden_1_layer = {'weights': tf.Variable(tf.random_normal([4, n_nodes_hl1])),
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
	print(prediction)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	hm_epochs = 10

	batch_manager = CurrencyBatchManager(batch_size=input_days, days_ahead=10)

	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())

		for epoch in range(hm_epochs):
			epoch_loss = 0
			for _ in range(batch_manager.hm_batches()):
				epoch_x, epoch_y = batch_manager.get_next_batch()
				print(epoch_y)
				_, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y})
				epoch_loss += c
			print('Epoch {} completed out of {}, loss: {}'.format(epoch+1, hm_epochs, epoch_loss))
			print('epoch_y = {}'.format(epoch_y))

		# correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		# accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		# print('Accuracy: {}'.format(accuracy.eval({x: mnist.test.images, y: mnist.test.labels})))

train_neural_network(x)