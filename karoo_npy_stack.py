# Karoo Numpy Stack
# by Kai Staats, MSc and Arun Kumar, PhD
# see LICENSE.md
# version 2018 03/26

import os
import sys
import numpy as np 
from scipy.misc import imread

'''
This script prepares a Numpy binary from a set of directory of images. This is terribly useful for processing of
images by Machine Learning algorithms such as a Convolutional Neural Network (CNN) in that the speed at which the 
Machine Learing algorthm can process a Numpy binary is far greater than processing the images individually, and it 
makes them that much more portable.

The current implementation of this script is designed to prepare test images for a CNN conducting Semantic Segementation
on b/w images. It currently works only with the R channel of RGB images, so if your images are in color, two of those 
channels will be lost. A near future version of this script will certainly be more flexible.

	python karoo_npy_stack.py sample_npy_stack/ sample.npy

The original images are left unaltered.	
'''

### USER INTERACTION ###

if len(sys.argv) < 3: print '\n\t\033[31mERROR!\033[0;0m You have assigned too few arguments.\n\n\t[path_to]/[images] [output_image_name].npy. Try again ...\n'; sys.exit()
elif len(sys.argv) > 3: print '\n\t\033[31mERROR!\033[0;0m You have assigned too many arguments.\n\n\t[path_to]/[images] [output_image_name].npy. Try again ...\n'; sys.exit()

os.system('clear')
		
print '\n\033[36m\033[1m'
print '\t **   **   ******    *****    ******    ******      **    **   ******  **    **'
print '\t **  **   **    **  **   **  **    **  **    **     ***   **  **    **  **  **'
print '\t ** **    **    **  **   **  **    **  **    **     ****  **  **    **   ****'
print '\t ****     ********  ******   **    **  **    **     ** ** **  *******     **'
print '\t ** **    **    **  ** **    **    **  **    **     **  ****  **          **'
print '\t **  **   **    **  **  **   **    **  **    **     **   ***  **          **'
print '\t **   **  **    **  **   **  **    **  **    **     **    **  **          **'
print '\t **    ** **    **  **    **  ******    ******      **    **  **          **'
print '\033[0;0m'
print '\t\033[36m Save a stack of images as a Numpy binary - by Arun Aniyan and Kai Staats\033[0;0m'
print ''

### LOAD THE DATA ###

dirname = sys.argv[1] # directory with images
file_out = sys.argv[2] # output filename

dir_list = os.listdir(dirname)
dir_list.sort()

image_x = len(imread(dirname + dir_list[0])) # width of image
image_y = len(imread(dirname + dir_list[1])) # height of image
img_array = np.empty([int(len(dir_list)), int(image_x), int(image_y)])


### GENERATE THE IMAGE ARRAY

i = 0
print '\tLoading images (arrays) ...'

for file_in in dir_list:
	img = imread(str(dirname) + '/' + file_in)
	if len(img.shape) == 3 and img.shape[2] == 3: img_array[i,:,:] = img[:,:,0] # grab the last of the 3-channel (RGB) images
	elif len(img.shape) == 3 and img.shape[2] == 2: img_array[i,:] = img[:,0] # grab the last of the 2-channel (some PNGs) images
	else: img_array[i] = img # for single channel (index'd BMP) images
	i = i + 1
	
if img_array.max() > 1: # the image (array) contains values other than 0 or 1
	print '\n\tOne or more images (arrays) has values other than 1 (black) or 0 (white).'
	
	while True:
		try:
			convert = raw_input('\n\tDo you want to convert values of 255 to -1 and 0 to 1? (y or n): ')
			if convert not in ('y','n',''): raise ValueError()
			if convert == 'n': break
			elif convert == 'y':
				img_array[img_array == 0] = 1; img_array[img_array == 255] = -1
				print '\n\t\033[36mValues of 255 are converted to -1, and values of 0 to 1\033[0;0m'; break
				
		except ValueError: print '\n\t\033[32m Select from the options given, (y)es or (n)o. Try again ...\n\033[0;0m'
		except KeyboardInterrupt: sys.exit()
		
# else: # we are working with a binary (0 or 1) image (array)


### SAVE THE MODIFIED DATA ###

print '\n\tSaving Numpy array file:', file_out

np.save(file_out, img_array)


