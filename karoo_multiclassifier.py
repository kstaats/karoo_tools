# Karoo Multiclass Classifer Test
# by Kai Staats, MSc
# see LICENSE.md
# version 2018 03/26

import os
import numpy as np
from numpy import arange

np.set_printoptions(linewidth = 320) # set the terminal to print 320 characters before line-wrapping in order to view Trees

'''
This is a toy script, designed to allow you to play with multiclass classification using the same underlying function
as employed by Karoo GP. Keep in mind that a linear multiclass classifier such as this is suited only for data which
itself has a linear (eg: time series) component, else GP will struggle to force the data to fit.

	python karoo_multiclassifier
	
'''

### USER INTERACTION ###

os.system('clear')

print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******       ******   **      ******    ******    ****** '
print '\t **  **   **    **  **   **  **    **  **    **     **    **  **     **    **  **    **  **    **'
print '\t ** **    **    **  **   **  **    **  **    **     **    **  **     **    **  **        **'
print '\t ****     ********  ******   **    **  **    **     **        **     ********   ******    ******'
print '\t ** **    **    **  ** **    **    **  **    **     **        **     **    **        **        **'
print '\t **  **   **    **  **  **   **    **  **    **     **    **  **     **    **  **    **  **    **'
print '\t **   **  **    **  **   **  **    **  **    **     **    **  **     **    **  **    **  **    **'
print '\t **    ** **    **  **    **  ******    ******       ******    ***** **    **   ******    ******'
print '\033[0;0m'
print '\t\033[36m A multi-classifier demonstration - by Kai Staats\033[0;0m\n'

while True:
	try:
		skew_sel = raw_input('\t Skew the data across the origin? y/n (default y): ')
		if skew_sel not in ['y','n','']: raise ValueError()
		skew_sel = skew_sel or 'y'; break
	except ValueError: print '\n\t\033[32m Select from the options given. Try again ...\033[0;0m'

while True:
	try:
		class_type = raw_input('\t Select (i)nfinite or (f)inite wing bins (default i): ')
		if class_type not in ['i','f','']: raise ValueError()
		class_type = class_type or 'i'; break
	except ValueError: print '\n\t\033[32m Select from the options given. Try again ...\033[0;0m'

menu = range(1,101)
while True:
	try:
		class_labels = raw_input('\t Enter the number of class labels / solutions (default 4): ')
		if class_labels not in str(menu) and class_labels not in '': raise ValueError()
		if class_labels == '0': class_labels = 1; break
		class_labels = class_labels or 4; class_labels = int(class_labels); break
	except ValueError: print '\n\t\033[32m Enter a number from 3 including 100. Try again ...\033[0;0m'


### PROCESS AND OUTPUT TO SCREEN - WITH SKEW ###

if skew_sel == 'y':
	
	skew = (class_labels / 2) - 1
	min_val = 0 - skew - 1 # add a data point to the left
	
	if class_labels & 1: max_val = 0 + skew + 3 # add a data point to the right if odd number of class labels
	else: max_val = 0 + skew + 2 # add a data point to the right if even number of class labels
	
	print '\n\t solutions =', range(class_labels)
	print '\t results = [', min_val, '...', max_val,']'
	print '\t skew =', skew, '\n'
	
	if class_type == 'i':
		for result in arange(min_val, max_val, 0.5):
			for solution in range(class_labels):
			
				if solution == 0 and result <= 0 - skew: # check for the first class
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas\033[1m', result, '\033[0;0m\033[36m<=', 0 - skew, '\033[0;0m'
					
				elif solution == class_labels - 1 and result > solution - 1 - skew: # check for the last class
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas\033[1m', result, '\033[0;0m\033[36m>', solution - 1 - skew, '\033[0;0m'
					
				elif solution - 1 - skew < result <= solution - skew: # check for class bins between first and last
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas', solution - 1 - skew, '<\033[1m', result, '\033[0;0m\033[36m<=', solution - skew, '\033[0;0m'
					
				else: fitness = 0 #; print '\t\033[36m no match for', result, 'in class', solution, '\033[0;0m' # no class match
	
	if class_type == 'f':
		for result in arange(min_val, max_val, .5):
			for solution in range(class_labels):
			
				if solution - 1 - skew < result <= solution - skew: # check for discrete, finite class bins
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas', solution - 1 - skew, '<\033[1m', result, '\033[0;0m\033[36m<=', solution - skew, '\033[0;0m'
					
				else: fitness = 0 #; print '\t\033[36m no match for', result, 'in class', solution, '\033[0;0m' # no class match
				

### PROCESS AND OUTPUT TO SCREEN - WITHOUT SKEW ###

else:

	min_val = 0
	max_val = class_labels
	
	print '\n\t solutions =', range(class_labels)
	print '\t results = [', min_val, '...', max_val,']\n'
	
	if class_type == 'i':
		for result in arange(min_val - 1, max_val, 0.5):
			for solution in range(class_labels):
			
				if solution == 0 and result <= 0: # check for the first class
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas\033[1m', result, '\033[0;0m\033[36m<=', 0, '\033[0;0m'
					
				elif solution == class_labels - 1 and result > solution - 1: # check for the last class
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas\033[1m', result, '\033[0;0m\033[36m>', solution - 1, '\033[0;0m'
					
				elif solution - 1 < result <= solution: # check for classes between first and last
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas', solution - 1, '<\033[1m', result, '\033[0;0m\033[36m<=', solution, '\033[0;0m'
					
				else: fitness = 0 #; print '\t\033[36m no match for', result, 'in class', solution, '\033[0;0m' # no class match
	
	if class_type == 'f':
		for result in arange(min_val, max_val, .5):
			for solution in range(class_labels):
			
				if solution - 1 < result <= solution: # check for discrete, finite class bins
					fitness = 1; print '\t\033[36m\033[1m class', solution, '\033[0;0m\033[36mas', solution - 1, '<\033[1m', result, '\033[0;0m\033[36m<=', solution, '\033[0;0m'
					
				else: fitness = 0 #; print '\t\033[36m no match for', result, 'in class', solution, '\033[0;0m' # no class match


