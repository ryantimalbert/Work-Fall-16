import cPickle as pickle
import os
import numpy
current_data = os.listdir('data')
current_data = [data[0 : -4] for data in current_data]
total = []
families = []
for family in current_data:
	file = open('data/{fam}.txt'.format(fam = family), 'rb')
	data_array = pickle.load(file)
	file.close()
	if 'eae' in family:
		families.append(data_array[0])
	total.append(data_array[0])
print(numpy.mean(total))
print(numpy.std(total))
print(numpy.mean(families))
print(numpy.std(families))