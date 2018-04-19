# Karoo GP Pipeline
# by Kai Staats; see LICENSE.md
# see LICENSE.md
# version 2018 04/19

import os
import csv
import sys
import numpy as np
import sympy as sp

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
This script is currently designed to work with binary classification only. It can be readily modified to work with
multiclass classifiction by adding upper and lower thresholds for each additional classification bin (below).

Once you have applied Karoo GP and are satisified with the quality of the evolved multivariate expression, you may be
ready to move that function into the real world. This script gives you a working foundation to do just that, by pasting
the Sympified (or raw) multivariate expression (e.g. a**2 + 2b * -3c) into the supplied interface. The script then 
executes the supplied function against the data, row by row, and talies the result into one of two bins (for the 
default binary classification). You can readily extract the ID numbers from each bin and determine how the each data
point has been classified.

	python karoo_pipeline.py [path/dataset.csv]
	
* no sample expression or data provided at this time
'''

### USER INTERACTION ###

if len(sys.argv) == 1: print '\n\t\033[31mERROR! You have not assigned an input file. Try again ...\033[0;0m'; sys.exit()
elif len(sys.argv) > 2: print '\n\t\033[31mERROR! You have assigned too many command line arguments. Try again ...\033[0;0m'; sys.exit()
else: filename = sys.argv[1]

os.system('clear')
		
print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******       ******   **'
print '\t **  **   **    **  **   **  **    **  **    **     **    **  **'
print '\t ** **    **    **  **   **  **    **  **    **     **    **  **'
print '\t ****     ********  ******   **    **  **    **     *******   **'
print '\t ** **    **    **  ** **    **    **  **    **     **        **'
print '\t **  **   **    **  **  **   **    **  **    **     **        **'
print '\t **   **  **    **  **   **  **    **  **    **     **        **'
print '\t **    ** **    **  **    **  ******    ******      **        ******'
print '\033[0;0m'
print '\t\033[36m Apply your evolved GP expression to a realworld pipeline - by Kai Staats\033[0;0m\n'

while True:
	try:
		algo_paste = raw_input('\t Enter the Sympified expression from Karoo GP: ')
		if algo_paste == '': raise ValueError()
		break
	except ValueError: print '\n\t\033[32m An empty expression is not going to get you very far. Try again ...\n\033[0;0m'
	except KeyboardInterrupt: sys.exit()

while True:
	try:
		function = raw_input('\t Select (c)lassification or (r)egression? (default c): ')
		if function not in ['c','r','']: raise ValueError()
		function = function or 'c'; break
	except ValueError: print '\t\033[32m Select from the options given. Try again ...\n\033[0;0m'
	except KeyboardInterrupt: sys.exit()

#while True:
#	try:
#		print_out = raw_input('\n\t Print the results to screen? y/n (default n): ')
#		if print_out not in ['y','n','']: raise ValueError()
#		print_out = print_out or 'n'; break
#	except ValueError: print '\033[32mSelect from the options given. Try again ...\n\033[0;0m'

precision = 6 # set the number of floating points


### LOAD DATA ###

data = np.loadtxt(filename, delimiter = ',', dtype = str) # load the data
header = data[0] # store the header for each column
data = np.delete(data,0,0) # delete the header from the data
data = data.astype(np.float) # convert the remaining array from string to float

data_rows = data.shape[0]
data_cols = data.shape[1]
data_dict = {} # prepare an empty dictionary
data_dict_array = np.array([]) # prepare an empty array to hold the dictionaries

for row in range(0, data_rows): # increment through each row of data
	for col in range(0, data_cols): # increment through each column
		data_dict.update( {header[col]:data[row,col]} ) # add a row of data into a dictionary	
		
	data_dict_array = np.append(data_dict_array, data_dict.copy()) # add a dictionary of data into the array
	

def fx_eval_subs(datum, algo_paste):

	'''
	Evaluation of the raw expression into a sympified expression was already done in Karoo GP. Therefore, we need only 
	assign each feature (column) with an associated data point (row) from the pipeline data, and then process.
	'''
	
	# If using iPython, after the pipeline is executed, you can extract any given feature value from any given row:
	#
	#		data_dict_array[row]['key']
	# 
	# ... where 'key' is a column header (feature variable)
	
	algo_sym = sp.sympify(algo_paste) # string converted to a functional expression
	subs = algo_sym.subs(datum) # process the expression against the datum
	if str(subs) == 'zoo': # result = 1 # TEST & DEBUG: print 'divide by zero', result; self.fx_karoo_pause(0)
		print '\n\t\033[31mERROR! Divide by zero\033[0;0m'; sys.exit()
		
	else: result = round(float(subs), precision) # force 'result' to the set number of floating points
		
	return result
	

class_0 = []
class_1 = []
regress = []

### CONDUCT A CLASSIFICATION RUN ###

if function == 'c':

	for row in range(0, data_rows):
		result = fx_eval_subs(data_dict_array[row], algo_paste) # process the expression against the test data
	
		if result <= 0: # test for class 0
			if header[0] == 'id': class_0.append([data_dict_array[row]['id']]) # record the ID if available
			else: class_0.append(row) # else record the .csv row number
			print '\t\033[36m data row', row, 'predicts class:\033[1m 0 as', result, '<=', 0, '\033[0;0m'
		
		elif result > 0: # test for class 1
			if header[0] == 'id': class_1.append([data_dict_array[row]['id']]) # record the ID if available		
			else: class_1.append(row) # else record the .csv row number
			print '\t\033[36m data row', row, 'predicts class:\033[1m 1 as', result, '>', 0, '\033[0;0m'
		
		else: print 'Whoa! The result is neither <= 0 nor > 0. The universe will implode in 5 ... 4 ... 3 ...'; sys.exit()
	

### CONDUCT A REGRESSION RUN ###

else:

	for row in range(0, data_rows):
		result = fx_eval_subs(data_dict_array[row], algo_paste) # process the expression against the test data
		regress.append(result) # else record the .csv row number
		print '\t\033[36m data row', row, 'produces:\033[1m', result, '\033[0;0m'
		

### SAVE THE OUTPUT ###

if function == 'c':

	print '\n\t Writing', len(class_1), 'class 1 to disk'
	target = open('class_1.csv', 'w'); target.close() # initialise class 1 .csv file
	with open('class_1.csv', 'a') as csv_file:
		target = csv.writer(csv_file, delimiter=',')
		#target.writerows([['IDs for class 1 (label 1)']])
		target.writerows([class_1])

	print '\n\t Writing', len(class_0), 'class 0 to disk'
	target = open('class_0.csv', 'w'); target.close() # initialise class 0 .csv file
	with open('class_0.csv', 'a') as csv_file:
		target = csv.writer(csv_file, delimiter=',')
		#target.writerows([['IDs for class 0 (label 0)']])
		target.writerows([class_0])


else:

	print '\n\t Writing', len(class_1), 'output to disk'
	target = open('regress.csv', 'w'); target.close() # initialise regression file
	with open('regress.csv', 'a') as csv_file:
		target = csv.writer(csv_file, delimiter='\n')
		target.writerows([regress])


