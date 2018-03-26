# Karoo Dataset Sort
# by Kai Staats, MSc UCT / AIMS and Arun Kumar, PhD
# version 1.0

import os
import sys
import numpy as np

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
In machine learning, it is often the case that your engaged dataset is derived from a larger parent. In constructing 
the subset, if we grab a series of datapoints (rows in a .csv) from the larger dataset in sequential order, only from 
the top, middle, or bottom, we will likely bias the new dataset and incorrectly train the machine learning algorithm. 
Therefore, it is imperative that we engage a random function, guided only by the number of data points for each class.
'''

### USER INTERACTION ###
if len(sys.argv) == 1: print '\n\t\033[31mERROR! You have not assigned an input file. Try again ...\033[0;0m'; sys.exit()
elif len(sys.argv) > 2: print '\n\t\033[31mERROR! You have assigned too many command line arguments. Try again ...\033[0;0m'; sys.exit()
else: filename = sys.argv[1]

os.system('clear')
		
print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******       ******    ******    *****   ******'
print '\t **  **   **    **  **   **  **    **  **    **     **    **  **    **  **   **    **'
print '\t ** **    **    **  **   **  **    **  **    **     **        **    **  **   **    **'
print '\t ****     ********  ******   **    **  **    **      ******   **    **  ******     **'
print '\t ** **    **    **  ** **    **    **  **    **           **  **    **  ** **      **'
print '\t **  **   **    **  **  **   **    **  **    **     **    **  **    **  **  **     **'
print '\t **   **  **    **  **   **  **    **  **    **     **    **  **    **  **   **    **'
print '\t **    ** **    **  **    **  ******    ******       ******    ******   **    **   **'
print '\033[0;0m'
print '\t\033[36m Data Prep for Machine Learning in Python - by Kai Staats, version 0.3\033[0;0m'

menu = range(1,100001)
while True:
	try:
		samples = raw_input('\n\tEnter number of desired datapoints per class (default 100): ')
		if samples not in str(menu) or samples == '0': raise ValueError()
		elif samples == '': samples = 100
		samples = int(samples); break
	except ValueError: print '\n\t\033[32mEnter a number from 10 including 100,000. Try again ...\033[0;0m'


### LOAD DATA ###
print '\n\tLoading dataset:\033[36m', filename, '\033[0;0m'

data = np.loadtxt(filename, delimiter=',', dtype = str)
header = data[0]
data = np.delete(data,0,0)

labels = len(np.unique(data[:,-1]))


### SORT DATA by LABEL ###
data_out = np.empty((1, len(data[0]))) # initiate an empty array with the same number of columns as the original data

for label in range(labels):
	rows_list = np.where(data[:,-1] == str(label)) # list all rows which end in the current label	
	rows_select = np.random.choice(rows_list[0], samples, replace = False) # randomly select rows from list
	data_out = np.append(data_out, data[rows_select], axis = 0)

data_out = np.delete(data_out,0,0) # delete the top, empty row


### SAVE SORTED DATASET ###
data_out = np.vstack((header, data_out)) # re-attach the data to the header

file_tmp = filename.split('.')[0]
np.savetxt(file_tmp + '-SORT.csv', data_out, delimiter = ',', fmt='%s')

print '\n\tThe sorted dataset has been written to the file:\033[36m', file_tmp + '-SORT.csv', '\033[0;0m'


