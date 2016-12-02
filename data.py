import cPickle as pickle
import os
current_data = os.listdir('data')
current_data = [data[0 : -4] for data in current_data]
for family in current_data:
	file = open('data/{fam}.txt'.format(fam = family), 'rb')
	data_array = pickle.load(file)
	file.close()
	print(data_array)
	print(family)