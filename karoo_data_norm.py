# Karoo Data Normalisation
# by Kai Staats, MSc
# see LICENSE.md
# version 2018 03/26

import os
import sys
import numpy as np

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
This script works with a dataset to prepare a new, normalised dataset. It does so by comparing all values in each given 
column, finding the maximum and minimum values, and then modifying each value to fall between a high of 1 and low of 0. 
The modified values are written to a new file, the original remaining untouched. This script is often used *after* 
karoo_data_sort.py.

	python karoo_normalise.py sample.csv
	
The original dataset is left unaltered.
'''

### USER INTERACTION ###

if len(sys.argv) == 1: print '\n\t\033[31mERROR! You have not assigned an input file. Try again ...\033[0;0m'; sys.exit()
elif len(sys.argv) > 2: print '\n\t\033[31mERROR! You have assigned too many command line arguments. Try again ...\033[0;0m'; sys.exit()
else: filename = sys.argv[1]

os.system('clear')

print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******      **    **   ******    *****   **       **'
print '\t **  **   **    **  **   **  **    **  **    **     ***   **  **    **  **   **  ***     ***'
print '\t ** **    **    **  **   **  **    **  **    **     ****  **  **    **  **   **  ****   ****'
print '\t ****     ********  ******   **    **  **    **     ** ** **  **    **  ******   ** ** ** **'
print '\t ** **    **    **  ** **    **    **  **    **     **  ****  **    **  ** **    **  ***  **'
print '\t **  **   **    **  **  **   **    **  **    **     **   ***  **    **  **  **   **   *   **'
print '\t **   **  **    **  **   **  **    **  **    **     **    **  **    **  **   **  **       **'
print '\t **    ** **    **  **    **  ******    ******      **    **   ******   **    ** **       **'
print '\033[0;0m'
print '\t\033[36m Data Prep for Machine Learning in Python - by Kai Staats\033[0;0m\n'

menu = range(1,9)
while True:
	try:
		fp = raw_input('\t Enter number of floating points desired in normalised data (default 4): ')
		if fp not in str(menu) and fp not in '': raise ValueError()
		if fp == '0': fp = 1; break
		fp = fp or 4; fp = int(fp); break
	except ValueError: print '\n\t\033[32m Enter a number from 1 including 8. Try again ...\033[0;0m'
	

### LOAD THE DATA ###

print '\n\t\033[36m Loading dataset:', filename, '\033[0;0m'
data = np.loadtxt(filename, delimiter = ',', dtype = str) # load the data
header = data[0] # store the header for each column
data = np.delete(data,0,0) # delete the header from the data
data = data.astype(np.float) # convert the remaining array from string to float


### NORMALISE THE DATA ###

def normalise(array):

	'''
	The formula was derived from stn.spotfire.com/spotfire_client_help/norm/norm_normalizing_columns.htm 
	'''
	
	norm = []
	array_norm = []
	array_min = np.min(array)
	array_max = np.max(array)
	
	for col in range(1, len(array) + 1):
		# norm = float((array[col - 1] - array_min) / (array_max - array_min))
		norm = float(array[col - 1] - array_min) / float(array_max - array_min)
		norm = round(norm, fp) # force to 4 decimal points
		array_norm = np.append(array_norm, norm)
		
	return array_norm
	

data_out = np.zeros(shape = (data.shape[0], data.shape[1])) # build an array that matches the shape of the original

for col in range(data.shape[1] - 1): # count columns, but exclude the right-most labels column so as to not delete labels
	print '\t normalising column:', col
	
	colsum = []
	for row in range(data.shape[0]):
		colsum = np.append(colsum, data[row,col])
		
	data_out[:,col] = normalise(colsum) # add each normalised column of data
	
data_out[:,data.shape[1] - 1] = data[:,data.shape[1] - 1] # add the labels again


### SAVE THE MODIFIED DATA ###

data_out = np.vstack((header, data_out)) # re-attach the header to the data
file_tmp = filename.split('.')[0]
np.savetxt(file_tmp + '-NORM.csv', data_out, delimiter = ',', fmt='%s')

print '\n\t\033[36m The normlised dataset has been written to the file:', file_tmp + '-NORM.csv', '\033[0;0m'


