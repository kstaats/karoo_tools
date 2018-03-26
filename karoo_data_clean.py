# Karoo Dataset Clean by Column
# by Kai Staats, MSc
# version 0.2

import os
import sys
import numpy as np

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
CLEAN COLUMN
This script loads your a .csv dataset which is assumed to have both a header and right-most labels (solutions) column, 
both of which are preserved. You, the user, provide the value you seek to remove from the dataset, and the threshhold 
(quantity) which should invoke said removal. A '0' threashold removes an entire column if even just one instance of 
the value is found. A '100' threshold removes the column only if every single row contains the given value.

CLEAN ROW
This script loads your a .csv dataset which is assumed to have both a header and right-most labels (solutions) column, 
both of which are preserved. You, the user, provide the value you seek to remove from the dataset. Any row which 
contains this value is automically removed from the dataset.
'''

### USER INTERACTION ###
if len(sys.argv) == 1: print '\n\t\033[31mERROR! You have not assigned an external data file. Try again ...\033[0;0m'; sys.exit()
elif len(sys.argv) > 2: print '\n\t\033[31mERROR! You have assigned too many command line arguments. Try again ...\033[0;0m'; sys.exit()
else: filename = sys.argv[1] # you have loaded an external data file

os.system('clear')
		
print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******       ******   **      ******   ******   **    **'
print '\t **  **   **    **  **   **  **    **  **    **     **    **  **     **       **    **  ***   **'
print '\t ** **    **    **  **   **  **    **  **    **     **    **  **     **       **    **  ****  **'
print '\t ****     ********  ******   **    **  **    **     **        **     *****    ********  ** ** **'
print '\t ** **    **    **  ** **    **    **  **    **     **        **     **       **    **  **  ****'
print '\t **  **   **    **  **  **   **    **  **    **     **    **  **     **       **    **  **   ***'
print '\t **   **  **    **  **   **  **    **  **    **     **    **  **     **       **    **  **    **'
print '\t **    ** **    **  **    **  ******    ******       ******    *****  ******  **    **  **    **'
print '\033[0;0m'
print '\t\033[36m Data Prep for Machine Learning in Python - by Kai Staats, version 0.3\033[0;0m'

menu = ['c','r','']
while True:
	try:
		clean = raw_input('\n\tClean your data by (c)olumn or by (r)ow (default r): ')
		if clean not in menu: raise ValueError()
		clean = clean or 'r'; break
	except ValueError: print '\t\033[32m Select from the options given. Try again ...\n\033[0;0m'
	except KeyboardInterrupt: sys.exit()
	
value = raw_input('\n\tEnter the value you seek in the data (default nan): '); value = value or 'nan'

menu = ['s','f','']
while True:
	try:
		d_type = raw_input('\n\tAre you seeking a (s)tring or a (f)loat? (default s): ')
		if d_type not in menu: raise ValueError()
		d_type = d_type or 's'; break
	except ValueError: print '\t\033[32m Select from the options given. Try again ...\n\033[0;0m'
	except KeyboardInterrupt: sys.exit()

del_list = []


### LOAD DATA ###
print '\n\tLoading dataset:\033[36m', filename, '\033[0;0m'

data = np.loadtxt(filename, delimiter=',', dtype = str)
header = data[0]
data = np.delete(data,0,0)

if d_type == 's': data = data.astype(str); value = str(value)
else: data = data.astype(float); value = float(value)

cols = len(data[0]) - 1 # count columns, but exclude the right-most labels column
rows = len(data) # count rows
print '\n\tThis dataset has\033[36m', cols, '\033[0;0mcolumns (not including labels) and\033[36m', rows, '\033[0;0mrows.'

pause = raw_input('\n\tPress ENTER to continue ...\n')


### COUNT MATCHES ###

if clean == 'r': # clean rows

	for n in range(rows):
		for m in range(cols):
			if data[n][m] == value: del_list.append(n)
				
	if del_list == []: print '\tNo rows contain the value:\033[36m', value, '\033[0;0m'; sys.exit()
	else: # at least one row contains the given value
		print '\tThe following\033[36m', len(del_list), '\033[0;0mrows will be removed from the new dataset:\n\n\t\033[36m', del_list, '\033[0;0m'
		data_clean = np.delete(data, del_list, axis = 0) # remove the designated rows
		header_clean = header
		

elif clean == 'c': # clean columns
	o = np.zeros(cols) # initiate a 1D array with the same x dimension as the original data
	
	for n in range(cols):
		for m in range(rows):
			if data[m][n] == value: o[n] = o[n] + 1
			
		# print '\t column\033[36m', n, '\033[0;0mcontains\033[36m', int(o[n]), '\033[0;0mof the value:\033[36m', value, '\033[0;0m'
		
	if np.sum(o) == 0: print '\tNo columns contain the value:\033[36m', value, '\033[0;0m'; sys.exit() # changed .any to .sum 20170929
	else: # at least one column contains the given value
	
		menu = range(0,101)
		while True:
			try:
				threshold = raw_input('\tWhat is the minimum percental for removal of a column? (default 0): ')
				if threshold not in str(menu): raise ValueError()
				elif threshold == '': threshold = 0
				threshold = int(threshold); break
			except ValueError: print '\t\033[32m Enter a number from 0 including 100. Try again ...\n\033[0;0m'
			except KeyboardInterrupt: sys.exit()
		
		for n in range(cols):
			if o[n] != 0 and float(o[n])/rows >= float(threshold)/100:
				del_list.append(n)

		if del_list == []: print '\n\tNo columns contain\033[36m', str(threshold) + '%', '\033[0;0mof the value:\033[36m', value, '\033[0;0m'; sys.exit()	
		else:
			print '\n\tThe following columns are removed from the new dataset:\n\n\t\033[36m', del_list, '\033[0;0m'
			data_clean = np.delete(data, del_list, axis = 1)
			header_clean = np.delete(header, del_list, axis = 0)
			

### SAVE REDUCED DATASET ###
data_out = np.vstack((header_clean, data_clean)) # re-attach the data to the header
file_tmp = filename.split('.')[0]
np.savetxt(file_tmp + '-CLEAN.csv', data_out, delimiter = ',', fmt='%s')

print '\n\tThe cleaned dataset has been written to the file:\033[36m', file_tmp + '-CLEAN.csv', '\033[0;0m'


