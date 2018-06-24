import numpy as numpy
import csv
import tensorflow as tf
#BA predictor

input_dict={}
with open('../baseballdatabank/core/Batting.csv','r') as csvfile:

	readCSV=csv.reader(csvfile,delimiter=',')
	for row in readCSV:
		if(row[0]!='playerID'):
			if(int(row[1])>2000):
				if(row[0] in input_dict):
					if(float(int(row[6]))!=0):	
						input_dict.get(row[0]).append((int(row[8]))/float(int(row[6])))
				else:
					if(float(int(row[6]))!=0):				
						input_dict[row[0]]=[int(row[8])/float(int(row[6]))]			
inputList=list()
outputList=list()
for k in input_dict:
	size=len(input_dict.get(k))
	if(size>=4):
		l=list()
		
		outputList.append([input_dict.get(k)[size-1]])
		l.append(input_dict.get(k)[size-4])	
		l.append(input_dict.get(k)[size-3])
		l.append(input_dict.get(k)[size-2])
		inputList.append(l)		


#hyperparams
num_hidden_per_layer=25
num_out=1
num_in=3
num_epochs=130
input_label=tf.placeholder(tf.float32)
output_label=tf.placeholder(tf.float32)

first_weight=tf.Variable(tf.random_uniform([num_in,num_hidden_per_layer],-1,1))
second_weight=tf.Variable(tf.random_uniform([num_hidden_per_layer,num_hidden_per_layer],-1,1))
third_weight=tf.Variable(tf.random_uniform([num_hidden_per_layer,num_hidden_per_layer],-1,1))
fourth_weight=tf.Variable(tf.random_uniform([num_hidden_per_layer,num_out],-1,1))

first_hidden_layer=tf.sigmoid(tf.matmul(input_label,first_weight))
second_hidden_layer=tf.sinh(tf.matmul(first_hidden_layer,second_weight))
third_hidden_layer=tf.sigmoid(tf.matmul(second_hidden_layer,third_weight))
dropout=tf.layers.dropout(inputs=third_hidden_layer)
output_layer=tf.sigmoid(tf.matmul(dropout,fourth_weight))

loss=tf.reduce_mean(output_layer-output_label)
opt=tf.train.GradientDescentOptimizer(.001).minimize(loss)

init=tf.initialize_all_variables()

with tf.Session() as sess:
	sess.run(init)
	err=sess.run(loss, feed_dict={input_label:inputList, output_label:outputList})
	i=0
	while(abs(err)>.1):
		sess.run(opt, feed_dict={input_label:inputList, output_label:outputList})
		err=sess.run(loss, feed_dict={input_label:inputList, output_label:outputList})
		i=i+1
		if(i%100==0):
			print("Err:",err)
			print("I:",i) 
	print("Test Avg:",sess.run(output_layer,feed_dict={input_label:[[.302,.287,.288]]}))
	print("Total Loss:",err)
print("Done")

