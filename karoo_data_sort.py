# Karoo Data Sort
# by Kai Staats, MSc and Arun Kumar, PhD
# see LICENSE.md
# version 2018 03/26

import os
import sys
import numpy as np

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
In machine learning, it is often the case that your engaged dataset is derived from a larger parent. In constructing 
a subset, if we grab a series of datapoints (rows in a .csv) from the larger dataset in sequential order, only from 
the top, middle, or bottom, we will likely bias the new dataset and incorrectly train the machine learning algorithm. 
Therefore it is imperative that we engage a random function, guided only by the number of data points for each class.
 
	python karoo_data_sort.py sample.csv

As this sample contains only 20 total rows, select just 5 as the output and it will produce a sorted .csv with 5 of 
each class, 50% of the original file.

The original dataset is left unaltered.	
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
print '\t\033[36m Data Prep for Machine Learning in Python - by Kai Staats\033[0;0m\n'

# the UI usually goes here, but in this case we need to know the number of rows in the dataset

### LOAD THE DATA ###

print '\t Loading dataset:\033[36m', filename, '\033[0;0m\n'
data = np.loadtxt(filename, delimiter = ',', dtype = str)
header = data[0]
data = np.delete(data,0,0)
labels = len(np.unique(data[:,-1]))

menu = range(1,len(data)/2)
while True:
	try:
		samples = raw_input('\t Enter number of desired datapoints per class (default %s): ' % str(len(data)/2)) 
		if samples not in str(menu) or samples == '0': raise ValueError()
		elif samples == '': samples = len(data)/2
		samples = int(samples); break
	except ValueError: print '\n\t\033[32m Enter a number from 1 including %s. Try again ... \033[0;0m' % str(len(data)/2)


### SORT DATA BY LABEL ###

data_out = np.empty((1, data.shape[1])) # build an empty array with the same number of columns as the original data

for label in range(labels):
	rows_list = np.where(data[:,-1] == str(label)) # list all rows which end in the current label	
	rows_select = np.random.choice(rows_list[0], samples, replace = False) # randomly select rows from list
	data_out = np.append(data_out, data[rows_select], axis = 0)

data_out = np.delete(data_out,0,0) # delete the top, empty row


### SAVE THE MODIFIED DATA ###

data_out = np.vstack((header, data_out)) # re-attach the header to the data
file_tmp = filename.split('.')[0]
np.savetxt(file_tmp + '-SORT.csv', data_out, delimiter = ',', fmt='%s')

print '\n\t The sorted dataset has been written to the file:\033[36m', file_tmp + '-SORT.csv', '\033[0;0m'


